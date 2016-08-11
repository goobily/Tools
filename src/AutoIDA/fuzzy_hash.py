# coding: utf-8
import ctypes
class FuzzyHash(object):
    def __init__(self):
        self.fuzzy = ctypes.cdll.fuzzy
        
        self.fuzzy_compare = self.fuzzy.fuzzy_compare
        self.fuzzy_compare.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.fuzzy_compare.restype = ctypes.c_int
        
        self.fuzzy_hash_buf = self.fuzzy.fuzzy_hash_buf
        self.fuzzy_hash_buf.restype = ctypes.c_int
        self.fuzzy_hash_buf.argtypes = [ctypes.c_char_p, ctypes.c_uint, ctypes.c_void_p]

    def hash_str(self, s):
        hs = ctypes.create_string_buffer(148)
        err = self.fuzzy_hash_buf(s, ctypes.sizeof(hs), hs)
        if err:
            raise RuntimeError("Cannot hash string. Error: " + str(err))
            
        return hs.value
        
    def compare(self, lhs, rhs):
        return self.fuzzy_compare(lhs, rhs)
