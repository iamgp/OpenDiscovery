import sys, os, errno, subprocess, glob
from runProcess import runProcess
import pkg_resources

def makeFolder(path):
    """Attempts folder creation

        Tries to create a folder. Raises an exception if one exists already.
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


class Vina(object):
	"""Vina driver. Sets up locations of files. """

	def __init__(self, screen, ligand, conf):

		#set up ivars
		self.locations = {}
		self.cmd = runProcess()
		self.cmd.verbose = screen.options['verbose']
		self.screen, self.ligand, self.conf = screen, ligand, conf

		# we need to figure out:
		# 	receptor - self.screen.options['receptor']
		# 	ligand   - self.ligand
		# 	conf 	 - self.conf
		# 	results_loc - determine by LD/results-*RECEPTOR*/*CONF*/*LIGAND*.pdbqt
		# 	log 	 - determine by LD/results-*RECEPTOR*/*LIGAND*.txt

		# lets determine platform
		if 'linux' in sys.platform:
			#self.locations['vina'] = screen.protocol_dir + "/OpenDiscovery/lib/vina-linux/vina"
			self.locations['vina'] = pkg_resources.resource_filename('OpenDiscovery', 'lib/vina-linux/vina')
		elif 'darwin' in sys.platform:
			#self.locations['vina'] = screen.protocol_dir + "/OpenDiscovery/lib/vina-osx/vina"
			self.locations['vina'] = pkg_resources.resource_filename('OpenDiscovery', 'lib/vina-osx/vina')

		self.locations['receptor'] = screen.ligand_dir + "/receptors/" + screen.options['receptor'] + ".pdbqt"
		self.locations['ligand']   = screen.ligand_dir + "/ligands/"   + self.ligand                + ".pdbqt"
		self.locations['config']   = screen.ligand_dir + "/confs/"      + self.conf                  + ".txt"

		self.locations['results_folder'] = screen.ligand_dir + "/results-"   + screen.options['receptor'] + "/"
		self.locations['conf_folder'] = self.locations['results_folder'] + self.conf + "/"

		self.locations['results']  = self.locations['conf_folder']     + ligand        + ".pdbqt"
		self.locations['log']      = self.locations['conf_folder']     + ligand        + ".txt"

	def run(self):
		""" Actually calls the vina binary. """
		try:
			# if we have a result already, don't repeat it!!
			if self.ligand in self.screen.results[self.screen.options['receptor']][self.conf]:
				pass
		except:

			makeFolder(self.locations['results_folder'])
			makeFolder(self.locations['conf_folder'])

			self.screen.results[self.screen.options['receptor']][self.conf] = 0

			self.cmd.run('{vina} --receptor {receptor} --ligand {ligand} --config {conf} --out {results} --log {log} --exhaustiveness {exhaustiveness}'.format(
				vina=self.locations['vina'], receptor=self.locations['receptor'], ligand=self.locations['ligand'],
				conf=self.locations['config'], results=self.locations['results'], log=self.locations['log'],
				exhaustiveness=self.screen.options['exhaustiveness']))
