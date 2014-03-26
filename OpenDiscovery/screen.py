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
from runProcess import runProcess

__version__ = '2.1.0'
class Screen(object):
	"""	A Screening object that can be used to perform docking of ligands to a receptor.

		Instantiates variables variables and runs methods that perform the screening.
	"""

	def __init__(self, parse = False, directory = '', receptor = '', exhaustiveness = '5', driver = 'vina', verbose = False, multiple_confs = False):

		# initialising ivars
		self.options = {}
		self.ligands = {}
		self.minimised = []
		self.results = {}
		self.total = 0
		self.sorted_results = []

		# determining user variables
		if parse:
			self.options = self.parser()
		else:
			self.options['directory'] = directory
			self.options['receptor'] = receptor
			self.options['exhaustiveness'] = exhaustiveness
			self.options['driver'] = driver
			self.options['multiple_confs'] = multiple_confs

		self.protocol_dir = os.path.abspath(os.path.split(sys.argv[0])[0])
		self.ligand_dir = os.path.abspath(os.path.expanduser(self.options['directory']))

		# set up the wrapper for run
		self.cmd = runProcess()
		self.cmd.verbose = verbose



	def run(self):
		# check that all necessary files are present
		self.__checkStart()

		# let's load our state
		self.load()

		if self.options['receptor'] not in self.results:
			self.results[self.options['receptor']] = {}
		self.save()

		# scanning the directory to make sure we detect any additions
		self.__scanDirectory()
		self.total = self.numberOfLigands()

		# at this point we know what ligands are present, and what the highest extension
		# is for all of them. we can now prepare any files for docking that aren't already
		# a pdbqt
		self.convertToPDB()
		self.minimisePDBs()
		self.preparePDBQTs()

		# we should now have a dictionary with all the ligands with an extension of pdbqt
		# we can now perform the screening
		self.performScreening()

		self.extractModels()
		self.gatherResults()

		# Save files
		self.save()

	def load(self):
		""" Loads data from a saved od.json into the current instance. """

		if os.path.isfile(self.ligand_dir + '/od.json'):
			try:
				data = json.load(open(self.ligand_dir + '/od.json'))
				self.ligands = data['ligands']
				self.minimised = data['minimised']
				self.results = data['results']
			except:
				pass

	def save(self):
		""" Saves the current state of the Screen class to od.json. """

		data = {
			'ligands': self.ligands,
			'minimised': self.minimised,
			'results': self.results
		}
		json.dump(data, open(self.ligand_dir + '/od.json', 'wb'), indent=4)

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

	def __scanDirectory(self):
		for cmpnd in glob.glob('{ld}/ligands/*'.format(ld=self.ligand_dir)):
			f = os.path.splitext(os.path.basename(cmpnd))
			lig_name = f[0]
			lig_ext = f[1]

			if lig_name not in self.ligands:
				self.ligands[lig_name] = lig_ext

			if (lig_ext == '.pdb') and self.ligands[lig_name] != '.pdb':
				self.ligands[lig_name] = lig_ext

			if (lig_ext == '.pdbqt') and self.ligands[lig_name] != '.pdbqt':
				self.ligands[lig_name] = lig_ext


	def __header(self):
		""" Simply presents a pretty header to the user. """

		log('')
		log('+------------------------------------+')
		log('|           OPEN DISCOVERY           |')
		log('|          Screening Module          |')
		log('+------------------------------------+')
		log('| Version: {0}                     |'.format(__version__))
		log('| URL:     www.opendiscovery.co.uk   |')
		log('+------------------------------------+')

	def convertToPDB(self):
		""" Converts the ligands into a PDB file using obabel, if currently not a PDB. """

		#self.__header()
		logHeader(self.options['receptor'])
		logHeader('Converting to PDBs')
		for index, cmpnd in enumerate(self.ligands):
			ProgressBar(index+1, self.total)

			extension = self.ligands[cmpnd]
			full_name = self.ligand_dir+'/ligands/'+cmpnd+extension

			if not(self.ligands[cmpnd] == '.pdb' or self.ligands[cmpnd] == '.pdbqt'):
				self.cmd.run('obabel {compound} -O {ld}/ligands/{name}.pdb --gen3d --conformer --systematic -p'.format(compound=full_name, ld=self.ligand_dir, name=cmpnd))
				self.ligands[cmpnd] = '.pdb'

		self.save()

	def minimisePDBs(self):
		""" Minimises the ligand PDBs using obabel. """

		logHeader('Minimising Ligands')
		for index, cmpnd in enumerate(self.ligands):
			ProgressBar(index+1, self.total)

			extension = self.ligands[cmpnd]
			full_name = self.ligand_dir+'/ligands/'+cmpnd+extension

			# logic not right
			if not(cmpnd in self.minimised) and not(self.ligands[cmpnd] == '.pdbqt'):
				self.cmd.run('obminimize -sd -c 1e-5 {ld}/ligands/{name}.pdb'.format(ld=self.ligand_dir, name=cmpnd))
				self.minimised.append(cmpnd)

		self.save()

	def preparePDBQTs(self):
		""" Converts the minimised ligands to PDBQT for Vina use. """

		logHeader('Preparing PDBQTs')
		for index, cmpnd in enumerate(self.ligands):
			ProgressBar(index+1, self.total)

			extension = self.ligands[cmpnd]
			full_name = self.ligand_dir+'/ligands/'+cmpnd+extension

			if self.ligands[cmpnd] == '.pdbqt':
				continue

			if self.ligands[cmpnd] == '.pdb':
				self.cmd.run('obabel {compound} -O {ld}/ligands/{name}.pdbqt'.format(
         		   compound=full_name, ld=self.ligand_dir, name=cmpnd))
				self.ligands[cmpnd] = '.pdbqt'

		self.save()

	def performScreening(self):
		""" Use the docking driver to perform the actually docking. """

		logHeader('Perform Screening')
		for index, cmpnd in enumerate(self.ligands):
			ProgressBar(index+1, self.total)

			full_name = self.ligand_dir+'/ligands/'+cmpnd+'.pdbqt'

			#if cmpnd not in self.results[self.options['receptor']]:
			if self.options['driver'].lower() == 'vina':
				Vina(self, cmpnd, self.cmd.verbose, self.options['multiple_confs']).run()
				#pass
			else:
				sys.exit()


	def extractModels(self):
		""" Extracts separate models from a multi-model PDB/PDBQT file. Uses an awk script. """

		logHeader('Extracting Models')

		# if we have multiple confs, make array of all of them
		# self.confs = []
		lf = []
		if self.options['multiple_confs'] == True:
			self.confs = []
			for conf in glob.glob(self.ligand_dir + "/confs/" + self.options['receptor'] + "*"):
				self.confs.append(self._getFileNameFromPath(conf))

			# so we have confs, receptor, ligands arrays
			# we need to loop over results-X/conf/*/ to get all ligand folders
			for screened in glob.glob(self.ligand_dir + "/results-" + self.options['receptor'] + "/*/*.pdbqt"):
				lf.append(screened)
		else:
			for screened in glob.glob(self.ligand_dir + "/results-" + self.options['receptor'] + "/*.pdbqt"):
				lf.append(screened)

		# for each ligand, we need to run the awk script to extract the energy
		for index, l in enumerate(lf):
			os.chdir(os.path.abspath(os.path.join(l, os.pardir)))
			lig_name = self._getFileNameFromPath(l)

			# extract modes
		 	self.cmd.run('awk -f {pd}/OpenDiscovery/lib/extract.awk < {results}'.format(pd=self.protocol_dir, results=lig_name + ".pdbqt"))

		 	# make new folder for them
		 	makeFolder(lig_name)

		 	for mode in glob.glob('mode_*.pdb'):
		 		os.rename(mode, '{0}/{0}_{1}'.format(lig_name, mode))

		 	try:
		 		os.rename(lig_name+".txt", lig_name+"/"+lig_name+".txt")
		 		os.rename(lig_name+".pdbqt", lig_name+"/"+lig_name+".pdbqt")
		 	except:
		 		pass

			os.chdir(self.protocol_dir)


	def gatherResults(self):
		""" Extracts the energy information from vina logs, and adds it to a sorted csv. """

		logHeader('Gathering Results')
		self.results[self.options['receptor']] = {}

		results_folder = []
		if self.options['multiple_confs'] == True:
			for conf_file in glob.glob(self.ligand_dir + "/confs/"+self.options['receptor']+"*"):
				short = os.path.splitext(os.path.basename(conf_file))[0]
				results = self.ligand_dir + "/results-" + self.options['receptor'] + "/" + short
				results_folder.append(results)
				self.results[self.options['receptor']][short] = {}

		else:
			results_folder.append(self.ligand_dir + "/results-" + self.options['receptor'])

	  	for rf in results_folder:
	  		short = os.path.splitext(os.path.basename(rf))[0]
			open(rf+'/summary.csv', 'w').close()
			for index, result in enumerate(glob.glob(rf+'/*/')):
			    lig_name = os.path.basename(os.path.normpath(result))
			    conf_file = os.path.basename(os.path.abspath(os.path.join(result, os.pardir)))
			    with open('{0}/{1}.txt'.format(result, lig_name)) as file:
			        for line in file:
			            if line.find('0.000') != -1:
			                energy = line.split()[1]
			                with open(rf+'/summary.csv', 'a') as summary:
			                    summary.write('{0},{1}\n'.format(lig_name, float(energy)))
				ProgressBar(index+1, self.total)

				if self.options['multiple_confs'] == True:
				 	self.results[self.options['receptor']][conf_file][lig_name] = energy
				else:
				 	self.results[self.options['receptor']][lig_name] = energy



	def writeCompleteSummary(self):
		receptors = []
		results = []
		ligands = []
		res = []
		for r in self.results:
			receptors.append(r)
			results.append(self.results[r])

		if self.options['multiple_confs'] == True:
			# results are in 'results' => receptor => conf => ligand
			# let's make a summary file per receptor
			print 'cannot merge results for >2 dimensions'
		else:
			for l in self.ligands:
				x = l
				asdf = (l,)
				for rec in receptors:
					y = self.results[rec][l]
					x = x + ", " + y
					asdf = asdf + (y,)

				ligands.append(asdf)

			for i in ligands:
				res.append(i)


			with open(self.ligand_dir + '/od_complete.csv','w') as f:
			    f_csv = csv.writer(f)
			    f_csv.writerow(["Ligands"] + receptors)
			    f_csv.writerows(ligands)


	def plot(self):
		import numpy as np
		import matplotlib.pyplot as plt
		import pandas as pd

		receptors = []
		for r in self.results:
			receptors.append(r)

		data = pd.read_csv(self.ligand_dir + '/od_complete.csv', index_col=0).sort_index()
		fig, ax = plt.subplots()
		heatmap = ax.pcolor(data, cmap=plt.cm.autumn)

		ax.set_yticks(np.arange(data.shape[0]) + 0.5, minor=False)
		ax.set_xticks(np.arange(data.shape[1]) + 0.5, minor=False)

		ax.invert_yaxis()
		ax.xaxis.tick_top()

		# Set the labels
		ax.set_xticklabels(receptors, minor=False)
		ax.set_yticklabels(data.index, minor=False)

		#plt.xticks(rotation=45)
		plt.colorbar(heatmap)

		plt.savefig(self.ligand_dir+"/heatmap.pdf")

		print '\n'

	def numberOfLigands(self):
		""" Utility function to return the number of ligands to convert. """

		return len(self.ligands)

	def _getFileNameFromPath(self, path):
		return os.path.splitext(os.path.basename(path))[0]


class ScreenTests(object):
	""" A class intended for testing. """

	def __init__(self, args):
		self.passed = args

	def checkSetup(self):
		return self.passed

