# coding: utf-8

import os
from PscUtilities import *

# decorator for singleton
def singleton(cls, *args, **kw):
    instances = {}
    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class PscResultManager(object) :
    def __init__(self, resultDir=""):
        if resultDir!= "":
            self._dir_ = resultDir
        else:
            current_dir = os.path.split(os.path.realpath(__file__))[0]
            self._dir_ = os.path.join(current_dir, "PscResult")
        if not os.path.exists(self._dir_):
            os.mkdir(self._dir_)
            
    def getResultDir(self):
        return self._dir_