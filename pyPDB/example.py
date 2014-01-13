from pyPDB import *

# load pdb
p = pyPDB('pdbs/gly.pdb')

# reduce the molecule
for atom in p.reduce():
	print '{}{}'.format(atom.element, atom.id)

# select one atom
p.selectAtom(4)

# select multiple atoms individually (this continues after the previous one)
p.selectAtom(5).selectAtom(6)

# or select multiple atoms all in one go
p.selectAtoms([4,5,6])

# the 'p' pyPDB instance now has a selectedAtoms attribute that is iterable:
for atom in p.selectedAtoms:
	print '{}{}'.format(atom.element, atom.id)

# calculate a distance map
print p.distanceMap()

# and also plot it
p.plotDistanceMap(save=False, close=True)

# calculate the distance between two atoms
print p.distanceBetweenAtoms(8,9)

# calculate atoms within a given distance of another atom
print p.atomsWithinDistanceOfAtom(10, 3)

# you can iterate over something like the above such as:
atomsWithinDistance = p.atomsWithinDistanceOfAtom(10, 3)
i=0
for x in atomsWithinDistance[0]:
    print 'Atom {}{} is within {} of {}{}: {}'.format(x.element, x.id, 3, p.molecule.atoms[10].element, 10, atomsWithinDistance[1][i])
    i+=1

# output a description of 'p' as json
print p.toJSON()

# reduce a pdb:
p.reduce()

# ...which can be iterated over:
for atom in p.reduce():
    print '{}{}'.format(atom.element, atom.id)
