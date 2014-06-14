import sys, os, errno, subprocess, glob
from runProcess import runProcess

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

	def __init__(self, screen, cmpnd, verbose = False, multiple_confs = False):
		self.locations = {}
		self.screen = screen
		self.cmd = runProcess()
		self.cmd.verbose = verbose
		self.multiple_confs = multiple_confs
		self.cmpnd = cmpnd

		if 'linux' in sys.platform:
			self.locations['vina'] = screen.protocol_dir + "/OpenDiscovery/lib/vina-linux/vina"
		elif 'darwin' in sys.platform:
			self.locations['vina'] = screen.protocol_dir + "/OpenDiscovery/lib/vina-osx/vina"

		self.locations['receptor'] = screen.ligand_dir + "/receptors/" + screen.options['receptor'] + ".pdbqt"
		self.locations['ligand'] = screen.ligand_dir + "/ligands/" + cmpnd + ".pdbqt"
		self.locations['config'] = screen.ligand_dir + "/receptors/" + screen.options['receptor'] + ".txt"
		self.locations['results'] = screen.ligand_dir + "/results-"+screen.options['receptor']+"/" + cmpnd + ".pdbqt"
		self.locations['log'] = screen.ligand_dir + "/results-"+screen.options['receptor']+"/" + cmpnd + ".txt"

		if not multiple_confs:
			makeFolder(screen.ligand_dir + "/results-"+screen.options['receptor'])

	def run(self):
		""" Actually calls the vina binary. """
		if self.multiple_confs:
			for conf_file in glob.glob(self.screen.ligand_dir + "/confs/" + self.screen.options['receptor'] + "*"):
				conf_name = os.path.splitext(os.path.basename(conf_file))[0]
				try:
					if self.cmpnd in self.screen.results[self.screen.options['receptor']][conf_name]:
						pass
				except:
					self.locations['config'] = conf_file
					conf_name = os.path.splitext(os.path.basename(conf_file))[0]

					_receptor_folder = self.screen.ligand_dir + "/results-" +self.screen.options['receptor'] + "/"
					_conf_folder = _receptor_folder + "/" + conf_name + "/"
					_results_location = _conf_folder + self.cmpnd + ".pdbqt"
					_log_location =  _conf_folder + self.cmpnd + ".txt"

					self.locations['results'] = _results_location
					self.locations['log'] = _log_location

					makeFolder(_receptor_folder)
					makeFolder(_conf_folder)

					self.screen.results[self.screen.options['receptor']][conf_name] = 0

					self.cmd.run('{vina} --receptor {receptor} --ligand {ligand} --config {conf} --out {results} --log {log} --exhaustiveness {exhaustiveness}'.format(
						vina=self.locations['vina'], receptor=self.locations['receptor'], ligand=self.locations['ligand'],
						conf=self.locations['config'], results=self.locations['results'], log=self.locations['log'],
						exhaustiveness=self.screen.options['exhaustiveness']))

		else:
			if self.cmpnd not in self.screen.results[self.screen.options['receptor']]:
				self.cmd.run('{vina} --receptor {receptor} --ligand {ligand} --config {conf} --out {results} --log {log} --exhaustiveness {exhaustiveness}'.format(
					vina=self.locations['vina'], receptor=self.locations['receptor'], ligand=self.locations['ligand'],
					conf=self.locations['config'], results=self.locations['results'], log=self.locations['log'],
					exhaustiveness=self.screen.options['exhaustiveness']))
				self.screen.results[self.screen.options['receptor']][self.cmpnd] = 0
