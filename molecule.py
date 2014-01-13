class Atom(object):
    """Atom Class"""
    def __init__(self, id=-1, element="", coords=None, residue_id=-1, residue_name=""):
        self.id = id
        self.element = element
        self.residue_id = residue_id
        self.residue_name = residue_name
        if coords == None:
            self.coords = [0,0,0]
        else:
            self.coords = coords

class Bond(object):
    """Bond Class"""
    def __init__(self, atom1=0, atom2=0):
        self.atom1 = atom1
        self.atom2 = atom2

class Residue(object):
    """Residue Class"""
    def __init__(self, id=-1, name="", atoms=None):
        self.id = id
        self.name = name
        if atoms == None:
            self.atoms = []
        else:
            self.atoms = atoms

class Molecule(object):
    """Molecule Class"""
    def __init__(self, id=0, name="", atoms=None, bonds=None, residues=None):
        self.id = id
        self.name = name

        if atoms == None:
            self.atoms = {}
        else:
            self.atoms = atoms

        if bonds == None:
            self.bonds = []
        else:
            self.bonds = bonds

        if residues == None:
            self.residues = {}
        else:
            self.residues = residues

    def residue_total(self):
        return len(self.residues)

    def atom_total(self):
        return len(self.atoms)

    def bond_total(self):
        return len(self.bonds)


if __name__ == '__main__':
    m = Molecule(1, "Water")
    m.atoms[1] = Atom(1, "O", coords=[1,2,3])
    m.atoms[2] = Atom(1, "H", coords=[4,2,3])
    m.atoms[3] = Atom(1, "H", coords=[1,5,7])

    m.bonds.append(Bond(1,2))
    m.bonds.append(Bond(1,3))

    print "Molecule name is: %s" % m.name

    for key in m.atoms.keys():
        a = m.atoms[key]
        print "Atom #%s is %s    \t x: %.3f \t y: %.3f \t z: %.3f" % (a.id, a.element, a.coords[0], a.coords[1], a.coords[2])

    for bond in m.bonds:
        print "bond between atom %s and atom %s" % (bond.atom1, bond.atom2)


