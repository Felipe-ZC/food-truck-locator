import sys

def isCorrectVersion():
    ver = sys.version_info
    if ver.major < 3 or ver.minor < 6:
        raise RuntimeError("Invalid Python version, please use Python 3.7 to run this script!")
