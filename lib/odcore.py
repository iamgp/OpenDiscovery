import os
import errno
import subprocess
import glob
from distutils.dir_util import copy_tree
import re
from delegate import *
# -----------------------------------------
#              OPEN DISCOVERY
#        CORE FUNCTIONs (LEAVE ALONE)
# -----------------------------------------
# Version:  1.0
# URL:      www.opendiscovery.org.uk
# Contacts: gareth.price@warwick.ac.uk
#           a.marsh@warwick.ac.uk
# -----------------------------------------

VERSION=1.0.1

def make_folder(path):
    """Attempts folder creation

        Tries to create a folder. Raises an exception if one exists already/
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def try_remove(filename):
    """Attempts file deletion

        Tried to delete a file/folder. If the path doesn't exist,
        raise an exception
    """
    try:
        os.remove(filename)
    except OSError, e:
        if e.errno != errno.ENOENT:
            raise


def log(string, suppress=False):
    """Logs the message to od_log.txt

        Used extensively to print out messages to the user while simultaneously
        writing the same message to a log file
    """
    with open("od_log.txt", "a+") as logFile:
        if 'FINISHED' in logFile.read():
            logFile.seek(0)
        if suppress == False:
            logFile.write(string + "\n")
            print string
        elif suppress == True:
            logFile.write(string + " ")
            print string,


def can_write(path):
    """Checks if directory is present

        If the directory is present, print out skipping message and return false. Otherwise
        return true.
    """
    if(os.path.isdir(path) == False):
        return True
    else:
        print 'Skipping %s' % path
        return False


def testCommand(commandToTest):
    """Tests if a command is present

        Used in odcheck to determine whether programs are installed and are callable
        from the command line.
    """
    if subprocess.call('type {0} > /dev/null 2>&1'.format(commandToTest), shell=True) == 0:
        return True
    else:
        return False


def use_obabel(inputType, outputType, obabel_extra=''):
    """ Wrapper for Open Babel (must be installed)

        This looks for files in the inputType folder
        and runs obabel outputting files of outputType.
        Also includes ability to provide string to pass to Open Babel
        through the obabel_extra argument.
    """
    make_folder(outputType)
    log('\n'), log('{0}'.format(outputType).center(45).upper())
    for cmpnd in glob.glob('{0}/*.{1}'.format(inputType, inputType)):
        b = os.path.splitext(os.path.basename(cmpnd))[0]
        log('Writing {0}/{1}.{2}'.format(outputType, b, outputType).center(45))
        subprocess.call('obabel {0} -O {1}/{2}.{3} {4}'.format(
            cmpnd, outputType, b, outputType, obabel_extra), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

def use_parallelized_obabel(inputType, outputType, obabel_extra=''):
    make_folder(outputType)
    x = [] # number of elements in array
    y = []
    for cmpnd in glob.glob('{0}/*.{1}'.format(inputType, inputType)):
        b = os.path.splitext(os.path.basename(cmpnd))[0]
        if len(x) > 20:
            parallelize(_execute_obabel, x)
            print ''
            print 'Written: ',
            for a in y:
                print a,
            #print x
            x = []
            y = []
        x.append('obabel {0} -O {1}/{2}.{3} {4}'.format(cmpnd, outputType, b, outputType, obabel_extra))
        y.append(b)


def _execute_obabel(toRun):
    return subprocess.call('{0}'.format(toRun), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

def use_obminimize(inputFolder):
    """ Wrapper for OBMinimize (must be installed - comes with Open Babel)

        This uses obminimize to minimize all pdb files in inputFolder.
    """
    log('\n'), log(' Minimisation'.center(45).upper())
    copy_tree(inputFolder, '{0}-minimised'.format(inputFolder))
    for cmpnd in glob.glob('{0}-minimised/*'.format(inputFolder)):
        b = os.path.splitext(os.path.basename(cmpnd))[0]
        log('Minimising {0}'.format(b).center(45))
        subprocess.call('obminimize -sd -c 1e-5 {0}'.format(
            cmpnd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


def file_present(path):
    """ Simply checks if a file is present"""
    if os.path.isfile(os.path.abspath(path)) == True:
        return True
    else:
        return False

def concatPDBs(pdb1, pdb2, newName):
    subprocess.call('grep -h ATOM {0} {1} >| {2}'.format(pdb1, pdb2, newName))
    #print 'grep -h ATOM {0} {1} >| {2}'.format(pdb1, pdb2, newName)
