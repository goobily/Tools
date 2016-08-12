# coding: utf-8

import os 
from stat import *

def isEmptyFile(filePath):
    if os.path.exists(filePath):
        return os.stat(filePath).st_size == 0
    return True