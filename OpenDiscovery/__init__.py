# -*- coding: utf-8 -*-

__author__ = 'Gareth Price'
__email__ = 'gareth.price@warwick.ac.uk'
__version__ = '2.4.4'
__url__ = 'http://opendiscovery.co.uk'

OD_VERSION = __version__

import sys
import os
import errno

def log(message="", verbose=True, colour=None, background=None, bold=False, underline=False, inverted=False, run=False, ret=False):
    """ log() prints a message that is formatted properly.

        Using ANSI colour and formatting strings, log() prints out a formatted
        string. If run=True, the following print command (or log())
        will appear on the same line.
    """
    if 'linux' in sys.platform:
        if ret:
            return message
        if run:
            print message,
        else:
            print message

    elif 'darwin' in sys.platform:
        if verbose:

            colours = {
                'black':    '90',
                'red':      '91',
                'green':    '92',
                'yellow':   '93',
                'blue':     '94',
                'magenta':  '95',
                'cyan':     '96',
                'white':    '97',
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

            if bold:
                message = '\033[1m' + message + '\033[21m'
            if underline:
                message = '\033[4m' + message + '\033[24m'
            if background is not None:
                message = '\033[' + backgrounds[background] + \
                    'm' + message + '\033[49m'
            if colour is not None:
                message = '\033[' + colours[colour] + 'm' + message + '\033[0m'
            if inverted:
                message = '\033[7m' + message + '\033[27m'

            if ret:
                return message
            if run:
                print message,
            else:
                print message

    return


def logHeader(message):
    """logHeader() prints out a formatted message which is used for heading sections."""

    message = '\n{message}'.format(message=message)
    print message

def printHeader(message):
    if 'linux' in sys.platform:
        print """\r{message:<20} """.format(message=message)
    elif 'darwin' in sys.platform:
        print """\r   \033[38;5;204m{message:<20}\033[0m """.format(message=message)


class ProgressBar(object):
    """A Simple class for showing a progress bar to the user"""

    def __init__(self, progress, total, message, newline=True):
        if 'linux' in sys.platform:
            message = "{message:<20}".format(message=message)
        elif 'darwin' in sys.platform:
            message = """  \033[38;5;204m{message:<20}\033[0m """.format(message=message)

        import time
        time.sleep(0.01)

        progress += 1
        percentage = (progress*10/total) #(divided by 10)
        percentage_left = 10 - percentage

        bar = '['
        bar += percentage * log('*', colour="white", ret=True)
        bar += percentage_left * log('*', colour="black", ret=True)
        bar += ']'
        bar += ' {}'.format(progress)

        string = ''
        if progress != total:
            if progress == 1 and newline == True:
                string = '\n\r {message} {bar}'.format(message=message, bar=bar)
            else:
                string = '\r {message} {bar}'.format(message=message, bar=bar)
        else:
                string = '\r {message} {bar}'.format(message=message, bar=bar)

        sys.stdout.write(string)
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
