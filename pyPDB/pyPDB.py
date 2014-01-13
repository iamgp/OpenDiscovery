#!/usr/bin/python

from molecule import *
import os, sys
import numpy, math, json
import matplotlib.pyplot as plt

class pyPDB(object):
    """PDB Class"""
    def __init__(self, filename):
        self.filename = filename
        self.molecule = None
        self.selectedAtoms = []
        self.reduced = []
        self._readFile()

    def _readFile(self):
        m = Molecule(self.filename)
        m.name = os.path.splitext(self.filename)[0].lower()

        f = open(self.filename, 'r').read().replace('\r\n', '\n')

        l = 0
        for line in f.splitlines():
            l += 1
            if (line[0:4] == 'ATOM' or line[0:6] == 'HETATM'):
                # get atom information
                atom = self._readAtom(line)
                # add atom to molecule atoms
                m.atoms[atom.id] = atom
                if atom.residue_id not in m.residues.keys():
                    # new residue
                    r = Residue()
                    r.id = atom.residue_id
                    r.name = atom.residue_name
                    r.atoms = [atom.id]
                    m.residues[r.id] = r
                else:
                    # new atom to residue
                    m.residues[atom.residue_id].atoms.append(atom)

            if line[0:6] == 'CONECT':
                bonds_in_line = self._readBonds(line)
                for bond in bonds_in_line:
                    m.bonds.append(bond)

        #if m.bond_total() == 0:
            #print 'Warning: No CONECT info, so no bond analysis.'

        self.molecule = m

    def _readAtom(self, line):
        a = Atom()
        a.id = int(line[6:11])
        a.element = line[12:14].strip().upper()
        a.residue_name = line[17:21].strip().upper()
        a.residue_id = int(line[22:27])
        a.coords[0] = float(line[31:38]) # x
        a.coords[1] = float(line[39:46]) # y
        a.coords[2] = float(line[47:54]) # z
        return a

    def _readBonds(self, line):
        fields = line.split()
        bonds = []
        n = 2
        while n < len(fields):
            bond = Bond()
            bond.atom1 = int(fields[1])
            bond.atom2 = int(fields[n])
            bonds.append(bond)
            n += 1

        return bonds

    def distanceBetweenAtoms(self, atomid1, atomid2):
        atom1 = self.molecule.atoms[atomid1]
        atom2 = self.molecule.atoms[atomid2]

        a = numpy.array((atom1.coords[0], atom1.coords[1], atom1.coords[2]))
        b = numpy.array((atom2.coords[0], atom2.coords[1], atom2.coords[2]))
        dist = numpy.linalg.norm(a-b)

        return int(dist * 100) / 100.00

    def atomsWithinDistanceOfAtom(self, atomid, distance):

        referenceAtom = self.molecule.atoms[atomid]

        atomsWithinDistance = []
        atomDistances = []
        for key in self.molecule.atoms:
            if self.distanceBetweenAtoms(atomid, self.molecule.atoms[key].id) <= distance:
                if self.molecule.atoms[key].id != atomid:
                    atomsWithinDistance.append(self.molecule.atoms[key])
                    d = self.distanceBetweenAtoms(atomid, self.molecule.atoms[key].id)
                    atomDistances.append(d)

        return (atomsWithinDistance, atomDistances)

    def toJSON(self):
        ret = '{ \n'
        ret += '\t "atom_total": {0},\n'.format(self.molecule.atom_total())
        ret += '\t "residue_total": {0},\n'.format(self.molecule.residue_total())
        ret += '\t "bond_total": {0}'.format(self.molecule.bond_total())
        ret += '\n}'
        return ret

    def distanceMap(self):
        n1 = 0
        dist_map = []
        for atom in self.molecule.atoms:
            atom1 = self.molecule.atoms[atom]
            temp_distances = []

            for a2 in self.molecule.atoms:
                atom2 = self.molecule.atoms[a2]
                temp_distances.append(self.distanceBetweenAtoms(atom1.id, atom2.id))


            dist_map.append(temp_distances)

        return dist_map

    def plotDistanceMap(self, save=False, directory='', close=False):
        m = self.distanceMap()
        matrix = numpy.matrix(m)

        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.set_aspect('equal')
        plt.title('Distance Map')
        extent = self.molecule.atom_total() + 0.5
        plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.hot, extent=(0.5,extent,0.5,extent))
        plt.colorbar()

        if save == True:
            plt.savefig('{}distance_map.pdf'.format(directory))

        if close == True:
            plt.close()
        else:
            plt.show()

    def selectAtom(self,atomid):
        atom = self.molecule.atoms[atomid]

        alreadySelected = False
        for atoms in self.selectedAtoms:
            if atomid == atoms.id:
                alreadySelected = True

        if alreadySelected == False:
            self.selectedAtoms.append(atom)

        return self # enables chaining


    def selectAtoms(self, atomids=[]):
        for atom in atomids:
            alreadySelected = False
            for atoms in self.selectedAtoms:
                if atom == atoms.id:
                    alreadySelected = True

            if alreadySelected == False:
                self.selectedAtoms.append(self.molecule.atoms[atom])

    def reduce(self):
        for atom in self.molecule.atoms:
            if 'H' not in self.molecule.atoms[atom].element:
                self.reduced.append(self.molecule.atoms[atom])

        return self.reduced

if __name__ == '__main__':
    p = pyPDB('pdbs/gly.pdb')
    if p:
        print 'loaded'


