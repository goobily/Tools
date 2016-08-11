# coding: utf-8

import fuzzy_hash

class HashMacher(object):
    def __int__(self):
        self.hasher = fuzzy_hash.FuzzyHash()
    def hash_str(self, str):
        return self.hasher.hash_str(str)
    def compare(self, lhs, rhs):
        return self.hasher.compare(lhs, rhs)
        
    def 
     