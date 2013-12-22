import sys
from lib.odcore import *

print('# ----------------------------------------- #')
print('#              OPEN DISCOVERY               #')
print('#               Check Module                #')
print('# ----------------------------------------- #')
print('# Version:  {0}                             #'.format(VERSION))
print('# URL:      www.opendiscovery.org.uk        #')
print('# Contacts: gareth.price@warwick.ac.uk      #')
print('#           a.marsh@warwick.ac.uk           #')
print('# ----------------------------------------- #')

dependencies = {'pymol': 'http://pymol.com', 'obabel' : 'http://openbabel.org/wiki/Get_Open_Babel', 'python' : 'http://www.python.org/getit/', 'lib/vina': 'http://vina.scripps.edu/download.html' }


print('\n')
for dep in dependencies:
	if testCommand(dep) == True:
		print('Success: {0} is installed.\n'.format(dep))
	else:
		print('{0}: {1} is not installed. You can download it from\n         {2}\n'.format( 'Warning' if dep == 'pymol' else 'Failure' ,dep, dependencies[dep]))

print('\n')

print('# ----------------------------------------- #')
print('#'),
print('FINSHED'.center(41)),
print('#')
print('# ----------------------------------------- #')
sys.exit()  # exits the program
