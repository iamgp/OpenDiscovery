# -*- coding: utf-8 -*-
from . import *
from pyPDB import pyPDB
from Vina import *
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
	def __init__(self, parse = False, directory = '', receptor = '', exhaustiveness = '', driver = ''):
		# Variables

		self.options = {}
		if parse:
			self.options = self.parser()
		else:
			self.options['directory'] = directory
			self.options['receptor'] = receptor
			self.options['exhaustiveness'] = exhaustiveness
			self.options['driver'] = driver

		self.protocolDir = os.path.abspath(os.path.split(sys.argv[0])[0])
		self.ligandDir = os.path.abspath(os.path.expanduser(self.options['directory']))
		self.ligands = {}
		self.minimised = []
		self.pdbqt = []
		self.results = {}
		self.total = 0
		self.sortedResults = []

		# let's see if there's an od.json file
		self.load()

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
		self.save()

	def save(self):
		data = {
			'ligands': self.ligands,
			'minimised': self.minimised,
			'pdbqt': self.pdbqt,
			'results': self.results
		}
		json.dump(data, open(self.ligandDir + '/od.json', 'wb'))

	def load(self):
		if os.path.isfile(self.ligandDir + '/od.json'):
			try:
				data = json.load(open(self.ligandDir + '/od.json'))
				self.ligands = data['ligands']
				self.minimised = data['minimised']
				self.pdbqt = data['pdbqt']
				self.results = data['results']
			except:
				pass

	def parser(self):
		import argparse
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
		i = 0
		log_header('Converting Files')
		for cmpnd in self.ligands:
			i = i + 1
			ProgressBar(i, self.total)

			extension = self.ligands[cmpnd]
			full_name = self.ligandDir+'/ligands/'+cmpnd+extension

			if self.ligands[cmpnd] != '.pdb':
				subprocess.call('obabel {compound} -O {ld}/ligands/{name}.pdb --gen3d --conformer --systematic -p'.format(compound=full_name, ld=self.ligandDir, name=cmpnd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				self.ligands[cmpnd] = '.pdb'

		self.save()

	def _minimise(self):
		i = 0
		log_header('Minimising Ligands')
		for cmpnd in self.ligands:
			i = i + 1
			ProgressBar(i, self.total)

			extension = self.ligands[cmpnd]
			full_name = self.ligandDir+'/ligands/'+cmpnd+extension

			if cmpnd not in self.minimised:
				subprocess.call('obminimize -sd -c 1e-5 {ld}/ligands/{name}.pdb'.format(ld=self.ligandDir, name=cmpnd),stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				self.minimised.append(cmpnd)

		self.save()

	def _preparePDBQT(self):
		i = 0
		log_header('Preparing PDBQTs')
		for cmpnd in self.ligands:
			i = i + 1
			ProgressBar(i, self.total)

			extension = self.ligands[cmpnd]
			full_name = self.ligandDir+'/ligands/'+cmpnd+extension

			if cmpnd not in self.pdbqt:
				subprocess.call('obabel {compound} -O {ld}/ligands/{name}.pdbqt'.format(
         		   compound=full_name, ld=self.ligandDir, name=cmpnd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				self.pdbqt.append(cmpnd)

		self.save()

	def _performScreening(self):
		log_header('Perform Screening')
		i = 0
		for cmpnd in self.pdbqt:
			i = i + 1
			ProgressBar(i, self.total)

			full_name = self.ligandDir+'/ligands/'+cmpnd+'.pdbqt'

			if cmpnd not in self.results:
				if self.options['driver'].lower() == 'vina':
					docking = Vina(self, cmpnd)
				else:
					sys.exit()

				docking.run()
				self.results[cmpnd] = 0


	def _extractModels(self):
		log_header('Extracting Models')
		i = 0
		for cmpnd in self.results:
			full_name = self.ligandDir+'/ligands/'+cmpnd+'.pdbqt'

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
			ProgressBar(i, self.total)

	def _gatherResults(self):
		log_header('Gathering Results')
		i = 0

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
		    self.results[b] = energy

		    i = i + 1
		    ProgressBar(i, self.total)

		with open(results_folder+'/summary.csv', 'w') as file:
			for line in sortedlist:
				file.write(line[0] + ', ' + line[1] + '\n')

		self.sortedResults = sortedlist

