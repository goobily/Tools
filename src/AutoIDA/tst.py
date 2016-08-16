# coding: utf-8

#from __future__ import print_function

import fuzzy_hash

hasher = fuzzy_hash.FuzzyHash()


str1 = "\\x55\\x8b\\xec\\x56\\x8b\\xf0\\x8b\\x46\\x0c\\x83\\x38\\x01\\x0f\\x8f\\xdf\\x3c\\x02\\x00\\x8b\\x46\\x04\\x40\\xe8\\xc5\\xfe\\xff\\xff\\x8b\\x46\\x04\\x8b\\x0e\\x66\\x8b\\x55\\x08\\x66\\x89\\x14\\x41\\xff\\x46\\x04\\x8b\\x46\\x04\\x8b\\x0e\\x33\\xd2\\x66\\x89\\x14\\x41\\x8b\\xc6\\x5e\\x5d\\xc2\\x04\\x00"
str2 = "\\x56\\x8b\\xf0\\x8b\\x46\\x0c\\x83\\x38\\x01\\x0f\\x8f\\x74\\x41\\x02\\x00\\x5e\\xc3"

str3 = "aaaaaaaxbbbbbbbcccccccdddddddeeeeeeefffffffggggggghhhhhhhxiiiiiiijjjjjjj"

hash1 = hasher.hash_str(str1)
print "hash1: ", hash1

hash2 = hasher.hash_str(str2)
print "hash2: ", hash2

print "hash1&hash2: ", hasher.compare(hash1, hash2)

list_a = [[1],[2],[3],[4],[4],[5],[6]]
list_b = [1,2,3]
for i in range(len(list_a)-1, -1, -1):
    list_a[i] += list_b
    list_a[i] = list(set(list_a[i]))

print "list_a: ", list_a

"""
hash3 = hasher.hash_str(str3)
print "hash3: ", hash3

print "hash1&hash3: ", hasher.compare(hash1, hash3)

print "hash2&hash3: ", hasher.compare(hash2, hash3)

file1 = r'F:\work\Ransome\RANSOM_CRYPGPCODE\ThreatHub\4dd27f8a138b7a5fd65a97ce133af8348c3d77f3'

file_hash1 = hasher.hash_file(file1)

file2 = r'F:\work\Ransome\RANSOM_CRYPGPCODE\ThreatHub\1654e26243eba115b2aac63b176bd304f1333260'
file_hash2 = hasher.hash_file(file2)

print 'file1 hash: ', file_hash1
print 'file2 hash: ', file_hash2


print 'file1&file1: ', hasher.compare(file_hash1, file_hash2)
"""
import os
import sys

"""
os.chdir(r"F:\work\Ransome\RANSOM_CRYPGPCODE\ThreatHub\upnpacked")
hashes = []
for f in os.listdir(os.curdir):
    hashes.append(hasher.hash_file(f))

for i in hashes:
    print()
    for j in hashes:
        print(hasher.compare(i, j), end="")
        print("\t", end="")
"""


"""
def test():
    #hasher.compare("12288:shkDgouVA2nxKkorvdRgQriDwOIxmxiZnYQE7PJcbNCxNFw8ibolxrcp:kRmJkcoQricOIQxiZY1WNC9w8Eol1k", "24576:oRmJkcoQricOIQxiZY1ia9qbwH32T5llU+yFb0A/7fcdxMIL8+D:NJZoQrbTFZY1ia9qbwHGT5lqXFIKfarR")
    hasher.hash_str(str1)


if __name__ == '__main__':
    test()
    import timeit
    print timeit.timeit("test()", setup="from __main__ import test")
"""
