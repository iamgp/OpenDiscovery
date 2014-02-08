#! /usr/bin/env python
# -*- coding: utf-8 -*-

from time import time
import OpenDiscovery as od
import OpenDiscovery.screen as ODScreen
import glob
import os
import shutil

if __name__ == '__main__':

	t = time()

	options                   = {}
	options['directory']      = '~/Desktop/od2/'
	options['exhaustiveness'] = 1
	options['driver'] 		  = 'vina'
	options['receptors']	  = []

	directory = os.path.abspath(os.path.expanduser(options['directory']))
	receptor_folder = directory + "/receptor/*.pdbqt"

	for receptor in glob.glob(receptor_folder):
		options['receptors'].append(receptor)

	for receptor in options['receptors']:
		r = os.path.basename(os.path.normpath(receptor))
		rName, rExtension = os.path.splitext(r)

		#s = ODScreen.Screen(
		# 		parse 			= False,
		# 		directory 		= options['directory'],
		# 		receptor 		= rName,
		# 		exhaustiveness 	= options['exhaustiveness'],
		# 		driver 			= options['driver']
		#)

		#shutil.move(directory+"/results", directory+"/results-"+rName)
		#shutil.move(directory+"/od.json", directory+"/od-"+rName+".json")

	od.logHeader('Time Taken: {0:.2f} seconds\n'.format(time() - t))



