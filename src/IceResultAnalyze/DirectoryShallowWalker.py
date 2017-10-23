# coding: utf-8

import os
from abc import ABCMeta, abstractmethod


class DirectoryShallowWalker(object):
    __metaclass__ = ABCMeta

    def walk(self, root_dir):
        for root, dirs, files in os.walk(root_dir, topdown=True):
            if self.is_directory_interesting(root):
                self.process_directory(root)
                dirs[:] = []

    @abstractmethod
    def process_directory(self, dir_path):
        pass

    @abstractmethod
    def is_directory_interesting(self, dir_path):
        pass
