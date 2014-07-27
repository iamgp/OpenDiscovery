import os

def expandPath(path):
	return os.path.abspath(os.path.expanduser(path))

def tryForKeyInDict(needle, haystack, fallback):
	try:
		return haystack[needle]
	except Exception, e:
		return fallback

def getFileNameFromPath(path):
	return os.path.splitext(os.path.basename(path))[0]

def getDirNameFromPath(path):
	return os.path.basename(os.path.normpath(path))

def enum(**enums):
    return type('Enum', (), enums)

def makeFolder(path):
    """Attempts folder creation

        Tries to create a folder. Raises an exception if one exists already/
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise