# coding: utf-8

import os 
from stat import *
import filecmp

def isEmptyFile(filePath):
    if os.path.exists(filePath):
        return os.stat(filePath).st_size == 0
    return True
    
def isEqualFile(lFile, rFile):
    return filecmp.cmp(lFile, rFile)
    
