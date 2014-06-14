#! /usr/bin/env python
# -*- coding: utf-8 -*-

from OpenDiscovery.screen import run

# ---------------------------------------------------------------------------- #
# Set up options 															   #
# ---------------------------------------------------------------------------- #
# Options available:														   #
# 	- parse      		allows entry via the command line (all 				   #
# 						other options are defunct) 							   #
# 	- directory			tell OpenDiscovery where the files are 				   #
# 						this is required! 									   #
# 	- exhaustiveness	how much effort do you want to use? must be a number   #
# 	- verbose			If True, all commands will show their output (useful   #
# 						for debugging)										   #
# ---------------------------------------------------------------------------- #

options                   = {}
options['directory']      = '~/Desktop/OD_Experiment/'
options['exhaustiveness'] = 10
#options['parse']		  = True 				(for e.g.)
#options['verbose']		  = True 				(for e.g.)

# ---------------------------------------------------------------------------- #
# Run the screening								 			   				   #
# ---------------------------------------------------------------------------- #

od = run(options)

print od.numberOfReceptors()