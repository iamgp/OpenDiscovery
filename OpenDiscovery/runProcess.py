# -*- coding: utf-8 -*-
import subprocess

class runProcess(object):
	"""docstring for runProcess"""
	def __init__(self, verbose = False):
		self.verbose = verbose

	def run(self,command):
		if self.verbose:
			subprocess.call(command, shell=True)
		else:
			subprocess.call(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)