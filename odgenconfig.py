import glob
import os
def getFileNameFromPath(path):
    return os.path.splitext(os.path.basename(path))[0]

class configFile(object):
    def __init__(self, name, c, s):
        self.name = name
        self.c = c
        self.s = s

    def write(self, directory):
        config = """center_x = {cx}
center_y = {cy}
center_z = {cz}

size_x = {sx}
size_y = {sy}
size_z = {sz}""".format(cx=float(self.c['x']), cy=float(self.c['y']), cz=float(self.c['z']),
                        sx=float(self.s['x']), sy=float(self.s['y']), sz=float(self.s['z']))

        with open(directory+"/confs/"+self.name+".txt", 'w') as f:
            f.write(config)


if __name__ == '__main__':
    options                   = {}
    options['directory']      = '~/Desktop/MULTIPLEPDB/'
    directory = os.path.abspath(os.path.expanduser(options['directory']))
    receptor_folder = directory + "/receptor/*.pdbqt"


    ligands = []

    for ligand in glob.glob(receptor_folder):
        ligands.append(getFileNameFromPath(ligand))

    confs_to_write = [
        {"name":"a", "center": {"x":10, "y":-113, "z":5}, "size": {"x":14, "y":14, "z":14}},
        {"name":"b", "center": {"x":10, "y":-113, "z":1}, "size": {"x":14, "y":14, "z":14}},
        {"name":"c", "center": {"x":10, "y":-113, "z":-3}, "size": {"x":14, "y":14, "z":14}},
        {"name":"d", "center": {"x":10, "y":-113, "z":-7}, "size": {"x":14, "y":14, "z":14}}
    ]

    for conf in confs_to_write:
        for ligand in ligands:
            name = ligand + "-" + conf['name']

            c = configFile(name, conf['center'], conf['size'])
            c.write(directory)



