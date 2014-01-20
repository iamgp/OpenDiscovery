# -*- coding: utf-8 -*-
from . import *
from pyPDB import pyPDB
import argparse
import os
import sys
import subprocess
import glob
import json
import shutil
import csv
import operator

__VERSION__ = "2.0.0a"

class Screen(object):
	"""docstring for Screen"""
	def __init__(self):
		# Variables
		self.options = self.parser()
		self.protocolDir = os.path.abspath(os.path.split(sys.argv[0])[0])
		self.ligandDir = os.path.abspath(self.options['directory'])
		self.ligands = {}
		self.minimised = []
		self.pdbqt = []
		self.results = {}
		self.total = 0
		self.sortedResults = []

		# let's see if there's an od.json file
		if os.path.isfile(self.ligandDir + '/od.json'):
			data = json.load(open(self.ligandDir + '/od.json'))
			self.ligands = data['ligands']
			self.minimised = data['minimised']
			self.pdbqt = data['pdbqt']
			self.results = data['results']

		# Actions
		self._checkStart()
		self._convertFiles()
		self._minimise()
		self._preparePDBQT()
		self._performScreening()
		self._extractModels()
		self._gatherResults()
		print '\n\n'

		# Save files
		data = { 'ligands': self.ligands, 'minimised': self.minimised, 'pdbqt': self.pdbqt, 'results': self.results }
		json.dump(data, open(self.ligandDir + '/od.json', 'wb'))

	def parser(self):
		parser = argparse.ArgumentParser(description='Open Discovery Screening Protocol')
		parser.add_argument('-d', '--directory',help='Path to the ligand directory. Required!', required=True)
		parser.add_argument('-e', '--exhaustiveness',help='Exhaustiveness. Default = 20.', type=int, default=20)
		parser.add_argument('-r', '--receptor', help='Receptor Name. Must be located within the receptor folder. Default = receptor.', default='receptor')
		return vars(parser.parse_args())

	def _checkStart(self):
		if os.path.isdir(self.ligandDir+"/ligands") != True:
			log("There is no ligand directory", colour="red")
			sys.exit()
		else:
			for cmpnd in glob.glob('{ld}/ligands/*'.format(ld=self.ligandDir)):
				f = os.path.splitext(os.path.basename(cmpnd))

				if f[0] not in self.ligands:
					self.ligands[f[0]] = f[1]

				if (f[1] == '.pdb') and self.ligands[f[0]] != '.pdb':
					self.ligands[f[0]] = f[1]

		self.total = self.numberOfLigands()

	def _header(self):
		log('')
		log('+------------------------------------+')
		log('|           OPEN DISCOVERY           |')
		log('|          Screening Module          |')
		log('+------------------------------------+')
		log('| Version: {0}                    |'.format(__VERSION__))
		log('| URL:     www.opendiscovery.co.uk   |')
		log('+------------------------------------+')

	def numberOfLigands(self):
		return len(self.ligands)

	def _convertFiles(self):
		self._header()
		i = 1
		log_header('Converting Files')
		for cmpnd in self.ligands:
			extension = self.ligands[cmpnd]
			full_name = self.ligandDir+'/ligands/'+cmpnd+extension

			ProgressBar(i, self.total)

			if self.ligands[cmpnd] != '.pdb':
				subprocess.call('obabel {compound} -O {ld}/ligands/{name}.pdb --gen3d --conformer --systematic -p'.format(compound=full_name, ld=self.ligandDir, name=cmpnd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				self.ligands[cmpnd] = '.pdb'

			i = i + 1

	def _minimise(self):
		i = 1
		log_header('Minimising Ligands')
		for cmpnd in self.ligands:
			extension = self.ligands[cmpnd]
			full_name = self.ligandDir+'/ligands/'+cmpnd+extension

			ProgressBar(i, self.total)

			if cmpnd not in self.minimised:
				subprocess.call('obminimize -sd -c 1e-5 {ld}/ligands/{name}.pdb'.format(ld=self.ligandDir, name=cmpnd),stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				self.minimised.append(cmpnd)

			i = i + 1

	def _preparePDBQT(self):
		i = 1
		log_header('Preparing PDBQTs')
		for cmpnd in self.ligands:
			extension = self.ligands[cmpnd]
			full_name = self.ligandDir+'/ligands/'+cmpnd+extension
			ProgressBar(i, self.total)

			if cmpnd not in self.pdbqt:
				subprocess.call('obabel {compound} -O {ld}/ligands/{name}.pdbqt'.format(
         		   compound=full_name, ld=self.ligandDir, name=cmpnd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				self.pdbqt.append(cmpnd)

			i = i + 1

	def _performScreening(self):
		#TODO: add other docking software support
		log_header('Perform Screening')
		i = 1
		for cmpnd in self.pdbqt:
			full_name = self.ligandDir+'/ligands/'+cmpnd+'.pdbqt'
			ProgressBar(i, self.total)

			if cmpnd not in self.results:

				if 'linux' in sys.platform:
					vina_location = self.protocolDir + "/lib/vina-linux/vina"
				elif 'darwin' in sys.platform:
					vina_location = self.protocolDir + "/lib/vina-osx/vina"

				receptor_location = self.ligandDir + "/receptor/" + self.options['receptor'] + ".pdbqt"
				ligand_location = self.ligandDir + "/ligands/" + cmpnd + ".pdbqt"
				config_location = self.ligandDir + "/receptor/" + self.options['receptor'] + ".txt"
				#print config_location
				results_location = self.ligandDir + "/results/" + cmpnd + ".pdbqt"
				log_location = self.ligandDir + "/results/" + cmpnd + ".txt"

				make_folder(self.ligandDir + "/results")

				subprocess.call('{vina} --receptor {receptor} --ligand {ligand} --config {conf} --out {results} --log {log} --exhaustiveness {exhaustiveness}'.format(
					vina=vina_location, receptor=receptor_location, ligand=ligand_location,
					conf=config_location, results=results_location, log=log_location,
					exhaustiveness=self.options['exhaustiveness']), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				self.results[cmpnd] = 0
			i = i + 1


	def _extractModels(self):
		log_header('Extracting Models')
		i = 1
		for cmpnd in self.results:
			full_name = self.ligandDir+'/ligands/'+cmpnd+'.pdbqt'
			ProgressBar(i, self.total)

			results_folder = self.ligandDir + "/results"
			results_location = self.ligandDir + "/results/" + cmpnd + ".pdbqt"

			os.chdir(results_folder)

			subprocess.call('awk -f {pd}/lib/extract.awk < {results}'.format(
				pd=self.protocolDir, results=results_location), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

			make_folder(cmpnd)

			for mode in glob.glob('mode_*.pdb'):
				os.rename(mode, '{0}/{0}_{1}'.format(cmpnd, mode))

			try:
				os.rename(cmpnd+".txt", cmpnd+"/"+cmpnd+".txt")
				os.rename(cmpnd+".pdbqt", cmpnd+"/"+cmpnd+".pdbqt")
			except:
				pass

			i = i + 1

	def _gatherResults(self):
		log_header('Gathering Results')
		i = 1

		results_folder = self.ligandDir + "/results"
		open(results_folder+'/summary.csv', 'w').close()
		for result in glob.glob(results_folder+'/*/'):
		    b = os.path.basename(os.path.normpath(result))
		    with open('{0}/{1}.txt'.format(result, b)) as file:
		        for line in file:
		            if line.find('0.000') != -1:
		                energy = line.split()[1]

		                with open(results_folder+'/summary.csv', 'a') as summary:
		                    summary.write('{0},{1}\n'.format(b, float(energy)))

		    reader = csv.reader(open(results_folder+'/summary.csv'))
		    sortedlist = sorted(reader, key=operator.itemgetter(1), reverse=True)
		    ProgressBar(i, self.total)

		    self.results[b] = energy
		    i = i + 1


		with open(results_folder+'/summary.csv', 'w') as file:
			for line in sortedlist:
				file.write(line[0] + ', ' + line[1] + '\n')

		self.sortedResults = sortedlist
