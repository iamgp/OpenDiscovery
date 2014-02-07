# -*- coding: utf-8 -*-
from . import *
import os
import sys
import subprocess
import glob
import json
import shutil
import csv
import operator
from Vina import *
#from pyPDB import pyPDB

__version__ = '2.0.6'
class Screen(object):
	"""	A Screening object that can be used to perform docking of ligands to a receptor.

		Instantiates variables variables and runs methods that perform the screening.
	"""

	def __init__(self, parse = False, directory = '', receptor = '', exhaustiveness = '', driver = ''):
		self.options = {}
		if parse:
			self.options = self.parser()
		else:
			self.options['directory'] = directory
			self.options['receptor'] = receptor
			self.options['exhaustiveness'] = exhaustiveness
			self.options['driver'] = driver

		self.protocol_dir = os.path.abspath(os.path.split(sys.argv[0])[0])
		self.ligand_dir = os.path.abspath(os.path.expanduser(self.options['directory']))
		self.ligands = {}
		self.minimised = []
		self.pdbqt = []
		self.results = {}
		self.total = 0
		self.sorted_results = []

		# let's see if there's an od.json file
		self.load()

		# Actions
		self.__checkStart()
		self.convertFiles()
		self.minimise()
		self.preparePDBQT()
		self.performScreening()
		self.extractModels()
		self.gatherResults()

		# Save files
		self.save()

	def save(self):
		""" Saves the current state of the Screen class to od.json. """

		data = {
			'ligands': self.ligands,
			'minimised': self.minimised,
			'pdbqt': self.pdbqt,
			'results': self.results
		}
		json.dump(data, open(self.ligand_dir + '/od.json', 'wb'))

	def load(self):
		""" Loads data from a saved od.json into the current instance. """

		if os.path.isfile(self.ligand_dir + '/od.json'):
			try:
				data = json.load(open(self.ligand_dir + '/od.json'))
				self.ligands = data['ligands']
				self.minimised = data['minimised']
				self.pdbqt = data['pdbqt']
				self.results = data['results']
			except:
				pass

	def parser(self):
		""" Presents an argparse interface to the user. """

		import argparse
		parser = argparse.ArgumentParser(description='Open Discovery Screening Protocol')
		parser.add_argument('-d', '--directory',help='Path to the ligand directory. Required!', required=True)
		parser.add_argument('-e', '--exhaustiveness',help='Exhaustiveness. Default = 20.', type=int, default=20)
		parser.add_argument('-r', '--receptor', help='Receptor Name. Must be located within the receptor folder. Default = receptor.', default='receptor')
		return vars(parser.parse_args())

	def __checkStart(self):
		""" Checks if all is well before continuing the screening.

			Looks for a ligands folder. Also determines current state of the ligands.
		"""

		if os.path.isdir(self.ligand_dir+"/ligands") != True:
			log("There is no ligand directory", colour="red")
			sys.exit()
		else:
			for cmpnd in glob.glob('{ld}/ligands/*'.format(ld=self.ligand_dir)):
				f = os.path.splitext(os.path.basename(cmpnd))

				if f[0] not in self.ligands:
					self.ligands[f[0]] = f[1]

				if (f[1] == '.pdb') and self.ligands[f[0]] != '.pdb':
					self.ligands[f[0]] = f[1]

		self.total = self.numberOfLigands()

	def __header(self):
		""" Simply presents a pretty header to the user. """

		log('')
		log('+------------------------------------+')
		log('|           OPEN DISCOVERY           |')
		log('|          Screening Module          |')
		log('+------------------------------------+')
		log('| Version: {0}                    |'.format(__version__))
		log('| URL:     www.opendiscovery.co.uk   |')
		log('+------------------------------------+')

	def convertFiles(self):
		""" Converts the ligands into a PDB file using obabel, if currently not a PDB. """

		self.__header()
		logHeader('Converting Files')
		for index, cmpnd in enumerate(self.ligands):
			ProgressBar(index+1, self.total)

			extension = self.ligands[cmpnd]
			full_name = self.ligand_dir+'/ligands/'+cmpnd+extension

			if self.ligands[cmpnd] != '.pdb':
				subprocess.call('obabel {compound} -O {ld}/ligands/{name}.pdb --gen3d --conformer --systematic -p'.format(compound=full_name, ld=self.ligand_dir, name=cmpnd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				self.ligands[cmpnd] = '.pdb'

		self.save()

	def minimise(self):
		""" Minimises the ligand PDBs using obabel. """

		logHeader('Minimising Ligands')
		for index, cmpnd in enumerate(self.ligands):
			ProgressBar(index+1, self.total)

			extension = self.ligands[cmpnd]
			full_name = self.ligand_dir+'/ligands/'+cmpnd+extension

			if cmpnd not in self.minimised:
				subprocess.call('obminimize -sd -c 1e-5 {ld}/ligands/{name}.pdb'.format(ld=self.ligand_dir, name=cmpnd),stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				self.minimised.append(cmpnd)

		self.save()

	def preparePDBQT(self):
		""" Converts the minimised ligands to PDBQT for Vina use. """

		logHeader('Preparing PDBQTs')
		for index, cmpnd in enumerate(self.ligands):
			ProgressBar(index+1, self.total)

			extension = self.ligands[cmpnd]
			full_name = self.ligand_dir+'/ligands/'+cmpnd+extension

			if cmpnd not in self.pdbqt:
				subprocess.call('obabel {compound} -O {ld}/ligands/{name}.pdbqt'.format(
         		   compound=full_name, ld=self.ligand_dir, name=cmpnd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				self.pdbqt.append(cmpnd)

		self.save()

	def performScreening(self):
		""" Use the docking driver to perform the actually docking. """

		logHeader('Perform Screening')
		for index, cmpnd in enumerate(self.pdbqt):
			ProgressBar(index+1, self.total)

			full_name = self.ligand_dir+'/ligands/'+cmpnd+'.pdbqt'

			if cmpnd not in self.results:
				if self.options['driver'].lower() == 'vina':
					docking = Vina(self, cmpnd)
				else:
					sys.exit()

				docking.run()
				self.results[cmpnd] = 0


	def extractModels(self):
		""" Extracts separate models from a multi-model PDB/PDBQT file. Uses an awk script. """

		logHeader('Extracting Models')
		for index, cmpnd in enumerate(self.results):
			full_name = self.ligand_dir+'/ligands/'+cmpnd+'.pdbqt'

			results_folder = self.ligand_dir + "/results"
			results_location = self.ligand_dir + "/results/" + cmpnd + ".pdbqt"

			os.chdir(results_folder)

			subprocess.call('awk -f {pd}/OpenDiscovery/lib/extract.awk < {results}'.format(
				pd=self.protocol_dir, results=results_location), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

			makeFolder(cmpnd)

			for mode in glob.glob('mode_*.pdb'):
				os.rename(mode, '{0}/{0}_{1}'.format(cmpnd, mode))

			try:
				os.rename(cmpnd+".txt", cmpnd+"/"+cmpnd+".txt")
				os.rename(cmpnd+".pdbqt", cmpnd+"/"+cmpnd+".pdbqt")
			except:
				pass

			ProgressBar(index+1, self.total)

			os.chdir(self.protocol_dir)

	def gatherResults(self):
		""" Extracts the energy information from vina logs, and adds it to a sorted csv. """

		logHeader('Gathering Results')

		results_folder = self.ligand_dir + "/results"
		open(results_folder+'/summary.csv', 'w').close()
		for index, result in enumerate(glob.glob(results_folder+'/*/')):
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

		    ProgressBar(index+1, self.total)

		with open(results_folder+'/summary.csv', 'w') as file:
			for line in sortedlist:
				file.write(line[0] + ', ' + line[1] + '\n')

		self.sorted_results = sortedlist

	def numberOfLigands(self):
		""" Utility function to return the number of ligands to convert. """

		return len(self.ligands)


class ScreenTests(object):
	""" A class intended for testing. """

	def __init__(self, args):
		self.passed = args

	def checkSetup(self):
		return self.passed
