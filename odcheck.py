import sys
from lib.odcore import *

print('# ----------------------------------------- #')
print('#              OPEN DISCOVERY               #')
print('#               Check Module                #')
print('# ----------------------------------------- #')
print('# Version:  {0}                           #'.format(VERSION))
print('# URL:      www.opendiscovery.org.uk        #')
print('# Contacts: gareth.price@warwick.ac.uk      #')
print('#           a.marsh@warwick.ac.uk           #')
print('# ----------------------------------------- #')

dependencies = {
	'pymol': 'http://pymol.com',
	'obabel' : 'http://openbabel.org/wiki/Get_Open_Babel',
	'python' : 'http://www.python.org/getit/',
	'lib/vina': 'http://vina.scripps.edu/download.html'
}

MIN_PYTHON_VER = (2,7,5)

if sys.version_info < MIN_PYTHON_VER:
	print('A more up to date version of python is required.')
	print('You can download a new version (2.7.5 or above) at http://www.python.org/getit/.')
	sys.exit()

print('\n')
for dep in dependencies:
	if testCommand(dep) == True:
		print('Success: {0} is installed.'.format(dep))
		if dep == 'obabel':
			print(get_obabel_version())
	else:
		print('{0}: {1} is not installed. You can download it from\n         {2}'.format( 'Warning' if dep == 'pymol' else 'Failure' ,dep, dependencies[dep]))

print('\n')

print('# ----------------------------------------- #')
print('#'),
print('FINSHED'.center(41)),
print('#')
print('# ----------------------------------------- #')
sys.exit()  # exits the program
