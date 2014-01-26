# -*- coding: utf-8 -*-

__author__ = 'Gareth Price'
__email__ = 'gareth.price@warwick.ac.uk'
__version__ = '2.0.4'

import sys, os, errno

def log(message="", verbose=True, colour=None, background=None, bold=False, underline=False, inverted=False, run=False):

    if verbose:

        colours = {
            'black':    '90',
            'red':      '91',
            'green':    '92',
            'yellow':   '93',
            'blue':     '94',
            'magenta':  '95',
            'cyan':     '96',
            'white':    '97'
        }

        backgrounds = {
            'default':  '49',
            'black':    '100',
            'red':      '101',
            'green':    '102',
            'yellow':   '103',
            'blue':     '104',
            'magenta':  '105',
            'cyan':     '106',
            'white':    '107'
        }

        if bold:                   message = '\033[1m' + message + '\033[21m'
        if underline:              message = '\033[4m' + message + '\033[24m'
        if background is not None: message = '\033[' + backgrounds[background] + 'm' + message + '\033[49m'
        if colour is not None:     message = '\033[' + colours[colour] + 'm' + message + '\033[0m'
        if inverted:               message = '\033[7m' + message + '\033[27m'

        if run:
            print message,
        else:
            print message

    return

def logHeader(message):
    message = '\033[1m' + message + '\033[21m'
    message = '\n\n\033[34m ==> \033[0m'+ message
    print message

class ProgressBar(object):
    """docstring for ProgressBar"""

    def __init__(self, progress, total, symbol="█"):
        percentage = (progress*100) / total
        bar = "     \033[94m"+ (symbol* (4*percentage/20)) +"\033[0m"  + (symbol * (20 - (4*percentage/20)) ) + " " + str(progress) + "/" + str(total)
        sys.stdout.write('\r'+bar)
        sys.stdout.flush()

def makeFolder(path):
    """Attempts folder creation

        Tries to create a folder. Raises an exception if one exists already/
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise