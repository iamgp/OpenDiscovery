# OpenDisco
from . import *
from .. import *

# Dependencies
import sh
import logging
import os
import shutil
import glob

# Logging level
logging.basicConfig(level=logging.DEBUG)

#  Constants
kSYSTEM = enum(
    RECEPTOR=0,
    CONF=1,
    LIGAND=2
)


class MDPreparation(object):

    """docstring for MDPreparation"""

    def __init__(
            self,
            directory,
            after_screening=True
    ):
        self.after_screening = after_screening
        self.directory = expandPath(directory)
        self.log = ColourLog(logging.getLogger(__name__))
        self.systems = self.getSystemList()
        self.system_files = []

    def run(self):
        if self.after_screening:
            self.moveScreeningFiles()
            self.prepareFilesForMDPrep()

        self.cleanReceptorPDBs()
        # self.reduceReceptorPDBs()

        self.prepareLigands()

    def moveScreeningFiles(self):
        if os.path.isdir(self.directory + "/Docking"):
            self.log.info('Docking folder is present, skipping consolidation')
            return self

        self.log.info('Moving files in dir: {0}'.format(self.directory))
        _files = glob.glob(self.directory + "/*")
        self.log.debug('Files to move: {0}'.format(_files))
        shutil.copytree(self.directory, self.directory + "/Docking")
        for fname in _files:
            if os.path.isdir(fname):
                shutil.rmtree(fname)
                self.log.debug('Deleting folder: {0}'.format(fname))
            else:
                os.remove(fname)
                self.log.debug('Deleting file: {0}'.format(fname))
        return self

    def prepareFilesForMDPrep(self):
        _prepPath = self.directory + "/MD-Prep/"
        _dockingPath = self.directory + "/Docking/"
        makeFolder(_prepPath)
        self.md_prep_path = _prepPath

        for s in self.systems['systems']:
            _systemPath = _prepPath + \
                s[kSYSTEM.RECEPTOR] + "." + s[kSYSTEM.CONF] + \
                "." + s[kSYSTEM.LIGAND] + "/"
            makeFolder(_systemPath)
            self.log.debug('Creating folder: {0}'.format(_systemPath))

            shutil.copy2(_dockingPath + "receptors/" +
                         s[kSYSTEM.RECEPTOR] + ".pdb", _systemPath + s[kSYSTEM.RECEPTOR] + ".pdb")
            self.log.debug('Copying {0} to {1}'.format(
                _dockingPath + "receptors/" + s[kSYSTEM.RECEPTOR] + ".pdb", _systemPath + s[kSYSTEM.RECEPTOR] + ".pdb"))

            shutil.copy2(_dockingPath + "results-" + s[kSYSTEM.RECEPTOR] + "/" + s[kSYSTEM.CONF] + "/" + s[
                         kSYSTEM.LIGAND] + "/" + s[kSYSTEM.LIGAND] + "_mode_1.pdb", _systemPath + s[kSYSTEM.LIGAND] + ".pdb")
            self.log.debug('Copying {0} to {1}'.format(_dockingPath + "results-" + s[kSYSTEM.RECEPTOR] + "/" + s[kSYSTEM.CONF] + "/" + s[
                           kSYSTEM.LIGAND] + "/" + s[kSYSTEM.LIGAND] + "_mode_1.pdb", _systemPath + s[kSYSTEM.LIGAND] + ".pdb"))

        return

    def cleanReceptorPDBs(self):
        for s in self.systems['systems']:
            self.log.debug(
                'Cleaning Receptor with path: {0}'.format(self.getReceptorPathFromSystem(s)))
            self.__cleanPDB(self.getReceptorPathFromSystem(s))

    def reduceReceptorPDBs(self):
        for s in self.systems['systems']:
            r = self.getReceptorPathFromSystem(s)

            r = '{0}_cleaned.pdb'.format(getFileNameFromPath(r))

            self.log.debug('Reducing Receptor with path: {0}'.format(r))
            self.__reducePDB(r)

    def prepareLigands(self):
        for s in self.systems['systems']:
            for l in self.systems['ligands']:
                lig_name = getFileNameFromPath(l)

                lig_full_name = '{0}.{1}'.format(lig_name, 'pdb')
                _systemPath = self.md_prep_path + \
                    s[kSYSTEM.RECEPTOR] + "." + s[kSYSTEM.CONF] + \
                    "." + s[kSYSTEM.LIGAND] + "/"

                lig_path = os.path.join(_systemPath, lig_full_name)

                sh.antechamber('-i {0} -fi pdb -o {1}.ante.mol2 -fo mol2 -c bcc'.format(
                    lig_path, os.path.join(_systemPath, lig_name)))

    def __reducePDB(self, PDB_path):
        PDB_path = expandPath(PDB_path)

        path, filename = os.path.split(PDB_path)
        filename = getFileNameFromPath(filename)

        out = '{0}_reduced.pdb'.format(filename)
        out = os.path.join(path, out)
        sh.reduce('-build', '-nuclear', PDB_path, '>', out)
        return self

    def __cleanPDB(self, PDB_path):
        PDB_path = expandPath(PDB_path)

        path, filename = os.path.split(PDB_path)
        filename = os.path.splitext(filename)[0]
        filename_out = '{0}_cleaned.pdb'.format(filename)
        out = os.path.join(path, filename_out)

        if not os.path.isfile(out):
            sh.pdb4amber('-i', PDB_path, '-o', out)
        else:
            self.log.debug('skipped {0}'.format(out))

        return filename_out

    def getSystemList(self):
        _receptors = self.getFilesFromDockingFolderWithPath(
            'receptors/*.pdbqt')
        _confs = self.getFilesFromDockingFolderWithPath('confs/*.txt')
        _ligands = self.getFilesFromDockingFolderWithPath('ligands/*.pdbqt')

        _systems = []
        for r in _receptors:
            for c in _confs:
                for l in _ligands:
                    _systems.append(
                        (getFileNameFromPath(r), getFileNameFromPath(c), getFileNameFromPath(l)))

        return {
            'receptors': _receptors,
            'confs': _confs,
            'ligands': _ligands,
            'systems': _systems  # this is a tuple
        }

    def getFilesFromDockingFolderWithPath(self, path):
        return glob.glob(self.directory + "/Docking/" + path)

    def getReceptorPathFromSystem(self, s):
        _prepPath = self.directory + "/MD-Prep/"
        _systemPath = _prepPath + \
            s[kSYSTEM.RECEPTOR] + "." + s[kSYSTEM.CONF] + \
            "." + s[kSYSTEM.LIGAND] + "/"
        return _systemPath + s[kSYSTEM.RECEPTOR] + ".pdb"
