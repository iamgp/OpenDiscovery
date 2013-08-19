"""@package odscreen
ODScreen is the screening module from OpenDiscovery (www.opendiscovery.org.uk).

Starting from a folder of ligands, a folder containing a receptor, and a AutoDock Vina configuration file,
it can automatically perform file preparation and docking, assuming obabel is installed. Vina is bundled in the lib
folder of the protocol folder.

ODScreen also handles mode extraction from the results, summarisation of binding energies (and sorting them into
a CSV file, readable by most spreadsheet programs like Excel) and production of complex PDB files containing
the lowest energy mode and its receptor. This requires pymol to be installed, however.

Contact details: gareth.price@warwick.ac.uk; a.marsh@warwick.ac.uk
"""

import os
import glob
import shutil
import sys
import argparse
from lib.odcore import *
import csv
import operator
from time import gmtime, strftime, time
import subprocess

# odscreen specific functions
def can_write(path):
    """ Checks whether a folder exists and if the user has asked for only
        new folders to be produced"""
    if(onlyAppend == False or (onlyAppend == True and os.path.isdir(path) == False)):
        return True
    else:
        log('\n'), log('Skipping {0}'.format(path).center(45).upper())
        return False


def should_extract():
    """ Checks to see if the result's out.pdbqt file should be extracted.

        If this has already been run, we do not need to extract the modes again."""
    for files in glob.glob('{0}/results/*/'.format(protocolDirectory)):
        if(any(files.find('mode'))):
            return False
        else:
            return True

# set up arguments parser
parser = argparse.ArgumentParser(
    description='Open Discovery Screening Protocol')
parser.add_argument(
    '-a', '--append', help='If this is true, only new folders will be added.',  action='store_true')
parser.add_argument(
    '-c', '--conf', help='RELATIVE path to the conf file (wrt ligand directory). Default = conf.txt', default="conf.txt")
parser.add_argument('-d', '--directory',
                    help='Path to the ligand directory. Required!', required=True)
parser.add_argument('-e', '--exhaustiveness',
                    help='Exhaustiveness. Default = 20.', type=int, default=20)
parser.add_argument('-g', '--genjobfile',
                    help='Generate a job file for cluster use. This will stop the protocol after creation.', action='store_true')
parser.add_argument(
    '-i', '--input', help='Input file type. Must be readable by OBabel. Files must be in folder of the same name. e.g. mol/X.mol if $ -i mol', required=True)
parser.add_argument(
    '-r', '--receptor', help='Receptor Name. Must be located within the receptor folder. Default = receptor.', default='receptor')
parser.add_argument(
    '-s', '--skip', help='Skip the screening?', action='store_true')
args = vars(parser.parse_args())

# set up some nicer names for commonly used arguments
inputType = args['input']
protocolDirectory = os.path.abspath(os.path.split(sys.argv[0])[0])
ligandDirectory = os.path.abspath(args['directory'])
os.chdir(ligandDirectory)
onlyAppend = args['append']
receptorName = args['receptor']
exhaustiveness = args['exhaustiveness']

# check we have the correct starting files
if os.path.isdir(ligandDirectory + "/" + inputType) != True:
    log('There is no ' + inputType +
        ' folder in the ligand directory. Make sure there are files in there with a .' + inputType + ' extension, too.')
    sys.exit()
if os.path.isdir(ligandDirectory + "/receptor") != True:
    log('There is no receptor folder in the ligand directory. Make sure there is a PDB and PDBQT file for the receptor, too.')
    sys.exit()
if os.path.isfile(ligandDirectory + "/" + args['conf']) != True:
    log('There is no ' + args['conf'] + ' file in the ligand directory.')
    sys.exit()

# Summary of the requested protocol
t1 = time()
log('# ----------------------------------------- #')
log('#              OPEN DISCOVERY               #')
log('#             Screening Module              #')
log('# ----------------------------------------- #')
log('# Version:  {0}                             #'.format(VERSION))
log('# URL:      www.opendiscovery.org.uk        #')
log('# Contacts: gareth.price@warwick.ac.uk      #')
log('#           a.marsh@warwick.ac.uk           #')
log('# ----------------------------------------- #')
log('#', True),  log('LigDir: {0}'.format(
    ligandDirectory).center(41), True),  log('#')
log('#', True),  log('Receptor Name: {0}'.format(
    receptorName).center(41), True),  log('#')
log('#', True),  log(
    'Input Type: {0}'.format(inputType).center(41), True),  log('#')
log('#', True),  log(
    'Conf: {0}'.format(args['conf']).center(41), True),  log('#')
log('#', True),  log('Exhaustivness: {0}'.format(
    exhaustiveness).center(41), True),  log('#')
log('# ----------------------------------------- #')
log('#', True),  log('Time Started: {0}'.format(
    strftime("%a, %d %b %Y %H:%M:%S", gmtime())).center(41), True),  log('#')
log('# ----------------------------------------- #')

# for a folder of separate files with smiles codes in
if(inputType != 'smiles'):
    if(can_write('smiles')):
        log('\n'), log('{0} -> SMILES'.format(inputType.upper()).center(45))
        make_folder('smiles')
        open('smiles.txt', 'w').close()
        for files in glob.glob('{0}/*.{1}'.format(inputType, inputType)):
            b = os.path.splitext(os.path.basename(files))[0]
            subprocess.call('obabel {0} -osmi -O smiles/{1}.txt'.format(
                files, b), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            with open('smiles/{0}.txt'.format(b), 'r+') as smiles:
                smile = smiles.read()
                newsmile = smile.strip().split()[0]
                smiles.seek(0)
                smiles.write(newsmile)
                smiles.truncate()
                with open('smiles.txt'.format(b), 'a') as smiles:
                    smiles.write('%s \n' % newsmile)
            log('Writing smiles/{0}.txt'.format(b).center(45))

# producing images for each smiles
if can_write('images'):
    make_folder('images')
    log('\n'), log('IMAGES'.center(45))
    for files in glob.glob("smiles/*.txt"):
        b = os.path.splitext(os.path.basename(files))[0]
        with open(files) as smileFile:
            smile = smileFile.readline()
            subprocess.call('obabel -:"{0}" -p 1000 -O images/{1}.svg'.format(
                smile.strip(), b), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            log('Writing images/{0}.svg'.format(b).center(45))

# create mol files if the input files aren't mol
if(inputType != 'mol' and can_write('mol')):
    use_obabel(inputType, 'mol', '--conformer --systematic -p')

# create mol2 files if the input files aren't mol2
if(inputType != 'mol2' and can_write('mol2')):
    use_obabel(inputType, 'mol2', '--gen3d --conformer --systematic -p')

# create pdb files if the input files aren't pdb
if(inputType != 'pdb' and can_write('pdb')):
    use_obabel(inputType, 'pdb', '--gen3d --conformer --systematic -p')

# minimise
if(can_write('pdb-minimised')):
    use_obminimize('pdb')

# prepare pdbqt files
# NOTE (24/7/13): obabel can be used to achieve this
#               : preliminary tests indicate that obabel's atomtypes are consistent
#               : with MGLTool's prepare_ligand4.py
if(can_write('pdbqt')):
    log('\n'), log(' PDBQT Preparation'.center(45).upper())
    make_folder('pdbqt')
    for cmpnd in glob.glob('pdb-minimised/*.pdb'):
        b = os.path.splitext(os.path.basename(cmpnd))[0]
        log('Writing {0}.pdbqt'.format(b).center(45))
        # subprocess.call('pythonsh {}/lib/prepare_ligand4.py -l {} -o
        # {}/pdbqt/{}.pdbqt'.format(protocolDirectory, cmpnd.strip(),
        # ligandDirectory, b), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        # shell=True)
        subprocess.call('obabel {0} -O {1}/pdbqt/{2}.pdbqt'.format(
            cmpnd, ligandDirectory, b), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


# if the user wants a job file, create a job.pbs file in root dir and exit
if(args['genjobfile']):
    log('\n', ' Creating Job File'.upper().center(45))
    open('job.pbs', 'w').close()
    with open('job.pbs', 'a') as job:
        job.write(
            '#!/bin/bash\n#PBS -l nodes=1:ppn=4,mem=4000mb,walltime=24:00:00\n#PBS -q taskfarm\n#PBS -V\n')
        job.write('#PBS -N vina_job\ncd \$PBS_O_WORKDIR\nmkdir -p results\n')
        for cmpnd in glob.glob('pdbqt/*.pdbqt'):
            b = os.path.splitext(os.path.basename(cmpnd))[0]
            log('Processing {0}'.format(b).center(45))
            job.write('mkdir -p results/{0}\n'.format(b))
            job.write('vina --receptor receptor/{0}.pdbqt --ligand pdbqt/{1}.pdbqt --config {2} --out results/{3}/out.pdbqt --log results/{4}/log.txt --exhaustiveness {5}\n'.format(
                receptorName, b, args['conf'], b, b, exhaustiveness))
    log('\n'), log('# ----------------------------------------- #')
    log('#', True), log('FINSHED'.center(41), True), log('#')
    log('#', True), log(
        'Time Taken: {0:.2f} seconds'.format(time() - t1).center(41), True), log('#')
    log('# ----------------------------------------- #')
    sys.exit()  # exits the program
# check to see if the user wants to skip this, if not run the vina screening
elif(args['skip'] == False):
    log('\n'), log(' SCREENING'.center(45))
    for cmpnd in glob.glob('pdbqt/*.pdbqt'):
        b = os.path.splitext(os.path.basename(cmpnd))[0]
        log('Processing {0}'.format(b).center(45))
        make_folder('results/%s' % b)
        useLibVina = 'vina' if testCommand(
            'vina') == True else '{0}/lib/vina'.format(protocolDirectory)
        subprocess.call('{0} --receptor receptor/{1}.pdbqt --ligand pdbqt/{2}.pdbqt --config {3} --out results/{4}/out.pdbqt --log results/{5}/log.txt --exhaustiveness {6}'.format(
            useLibVina, receptorName, b, args['conf'], b, b, exhaustiveness), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
elif(args['skip'] == True):
    log('\n', 'Skipping screening'.center(45).upper())

# extract modes from multi-mode pdbqt
# if(should_extract()):
log('\n'), log(' EXTRACTING'.center(45))
for cmpnd in glob.glob('results/*/'):
    if 'complex' not in cmpnd:
        b = os.path.basename(os.path.normpath(cmpnd))
        shutil.copy2(
            '{0}/receptor/{1}.pdb'.format(ligandDirectory, receptorName),
            '{0}/{1}/{2}.pdb'.format(ligandDirectory, cmpnd, receptorName))
        log('Processing {0}'.format(cmpnd).center(45))
        os.chdir('{0}/{1}'.format(ligandDirectory, cmpnd))
        subprocess.call('awk -f {0}/lib/extract.awk < out.pdbqt'.format(
            protocolDirectory), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        for mode in glob.glob('mode_*.pdb'):
            os.rename(mode, '{0}_{1}'.format(b, mode))
os.chdir(ligandDirectory)
# else:
# 	log('Skipping extraction')

# covert pdb to mol2
if(can_write('results-mol2')):
    log('\n'), log(' PDB -> MOL2'.center(45))
    for cmpnd in glob.glob('results/*/'):
        if 'complex' not in cmpnd:
            b = os.path.basename(os.path.normpath(cmpnd))
            make_folder('results-mol2')
            log('Writing results-mol2/{0}.mol2'.format(b).center(45))
            subprocess.call('obabel {0}/out.pdbqt -l 1 -O results-mol2/{0}.mol2 '.format(
                cmpnd, b, b), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

# Produce a combined mol for AuPoSOM analysis
if file_present('combined.mol2') != True:
    with open('combined.mol', 'w') as combined:
        for cmpnd in glob.glob('results-mol2/*'):
            with open(cmpnd) as f:
                combined.write(f.read())

# summarise the log files into one summary.txt (used for analysis) and
# summary.csv (excel/R compatible)
open('results/summary.txt', 'w').close()
open('results/summary.csv', 'w').close()
log('\n'), log(' SUMMARISING'.center(45))
for result in glob.glob('results/*/'):
    b = os.path.basename(os.path.normpath(result))
    if b != 'complexes':
        with open('{0}/log.txt'.format(result)) as file:
            for line in file:
                if line.find('0.000') != -1:
                    energy = line.split()[1]
                    with open('results/summary.txt', 'a') as summary:
                        summary.write('{0},{1};'.format(b, float(energy)))
                        log("Summarising {0}".format(b).center(45))
                    with open('results/summary.csv', 'a') as summary:
                        summary.write('{0},{1}\n'.format(b, float(energy)))

# Sorts the CSV in order
reader = csv.reader(open("results/summary.csv"))
sortedlist = sorted(reader, key=operator.itemgetter(1), reverse=True)
open('results/summary-sorted.csv', 'w').close()
with open('results/summary-sorted.csv', 'w') as file:
    for line in sortedlist:
        file.write(line[0] + ', ' + line[1] + '\n')

# makes complexes
#if can_write('results/complexes'):
    log('\n'), log(' MAKING COMPLEXES'.center(45))
    make_folder('results/complexes')
    for cmpnd in glob.glob('results/*/'):
        if 'complex' not in cmpnd:
            b = os.path.basename(os.path.normpath(cmpnd))
            c = cmpnd + b + '_mode_1.pdb'
            #print subprocess.call('pymol -c receptor/{0}.pdb {1}  -d \'save results/complexes/{2}.pdb \''.format(
            #    receptorName, c, b), shell=True)
            print subprocess.call('grep -h ATOM {0} {1} >| {2}'.format('receptor/'+receptorName+'.pdb', c, 'results/complexes/'+receptorName+'.pdb'), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True )
            log('Writing {0}'.format(b).center(45))

log('\n'), log('# ----------------------------------------- #')
log('#', True), log('FINSHED'.center(41), True), log('#')
log('#', True), log(
    'Time Taken: {0:.2f} seconds'.format(time() - t1).center(41), True), log('#')
log('# ----------------------------------------- #')

sys.exit()
