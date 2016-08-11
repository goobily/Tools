# coding: utf-8
import fuzzy_hash

hasher = fuzzy_hash.FuzzyHash()

hash1 = hasher.hash_str("1111111111122222223333334446666666445555555555555555555566666666666666665")
hash2 = hasher.hash_str("11111111x112222s2233x33344546xx66664453555555555555555555x66666x66666666665")
print hash1
print hash2
print hasher.compare(hash1, hash2)