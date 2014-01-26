 #! /usr/bin/env python
# -*- coding: utf-8 -*-

import OpenDiscovery as od
import OpenDiscovery.screen as ODScreen
import argparse
from time import gmtime, strftime, time

if __name__ == '__main__':

	# Set up parser for options via command line
	#parser = argparse.ArgumentParser(description='Open Discovery Screening Protocol')
	#parser.add_argument('-d', '--directory', help='Path to the ligand directory. Required!', required=True)
	#parser.add_argument('-e', '--exhaustiveness', help='Exhaustiveness. Default = 20.', type=int, default=20)
	#parser.add_argument('-r', '--receptor', help='Receptor Name. Must be located within the receptor folder. Default = receptor.', default='receptor')
	#parser.add_argument('--driver', help='The docking driver to use. Default = vina, default='vina')
	#options = vars(parser.parse_args())

	# or hard code them in
	options                   = {}
	options['directory']      = '~/Desktop/od2/'
	options['receptor']       = 'receptor'
	options['exhaustiveness'] = 1
	options['driver'] 		  = 'vina'

	# let's time it
	t = time()


	# set up a new screen instance
	s = ODScreen.Screen(
			parse 			= False,
			directory 		= options['directory'],
			receptor 		= options['receptor'],
			exhaustiveness 	= options['exhaustiveness'],
			driver 			= options['driver']
		)

	od.logHeader('Time Taken: {0:.2f} seconds'.format(time() - t))
	print '\n'