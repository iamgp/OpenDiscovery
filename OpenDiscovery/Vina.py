import sys, os, errno, subprocess

def make_folder(path):
    """Attempts folder creation

        Tries to create a folder. Raises an exception if one exists already/
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


class Vina(object):
	"""Vina driver"""
	def __init__(self, screen, cmpnd):

		self.locations = {}
		self.screen = screen

		if 'linux' in sys.platform:
			self.locations['vina'] = screen.protocolDir + "/OpenDiscovery/lib/vina-linux/vina"
		elif 'darwin' in sys.platform:
			self.locations['vina'] = screen.protocolDir + "/OpenDiscovery/lib/vina-osx/vina"

			self.locations['receptor'] = screen.ligandDir + "/receptor/" + screen.options['receptor'] + ".pdbqt"
			self.locations['ligand'] = screen.ligandDir + "/ligands/" + cmpnd + ".pdbqt"
			self.locations['config'] = screen.ligandDir + "/receptor/" + screen.options['receptor'] + ".txt"
			#print config_location
			self.locations['results'] = screen.ligandDir + "/results/" + cmpnd + ".pdbqt"
			self.locations['log'] = screen.ligandDir + "/results/" + cmpnd + ".txt"

			make_folder(screen.ligandDir + "/results")

	def run(self):
		subprocess.call('{vina} --receptor {receptor} --ligand {ligand} --config {conf} --out {results} --log {log} --exhaustiveness {exhaustiveness}'.format(
			vina=self.locations['vina'], receptor=self.locations['receptor'], ligand=self.locations['ligand'],
			conf=self.locations['config'], results=self.locations['results'], log=self.locations['log'],
			exhaustiveness=self.screen.options['exhaustiveness']), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)