# coding: utf-8

import fuzzy_hash
import os
import json
from itertools import combinations
from PscResultManager import *

class HashMacher(object):
    def __init__(self, sourceFilesPath=""):
        self.sourceFiles = set()
        self.resultFolder = ""
        self.resultFile = ""       
        self.setResultFolder()
        self.setResultFile()
        self.addSourceFiles(sourceFilesPath)
        self.hasher = fuzzy_hash.FuzzyHash()
     
    def setResultFolder(self, dir=""):
        if dir != "":
            self.resultFolder = dir
        else:
            self.resultFolder = os.path.join(PscResultManager().getResultDir(), "HashMachResult")
        if not os.path.exists(self.resultFolder):
            os.mkdir(self.resultFolder)
            
    def setResultFile(self):
        self.resultFile = os.path.join(self.resultFolder, "HashMatchResult.json")
        
    def addSourceFiles(self, sourceFilesPath=""):
        if sourceFilesPath == "":
            return
        if os.path.isfile(sourceFilesPath):
            self.sourceFiles.add(sourceFilesPath)
        elif os.path.isdir(sourceFilesPath):
            for root, dirs, files in os.walk(sourceFilesPath):
                for file in files:
                    filePath = os.path.join(root, file)
                    self.sourceFiles.add(filePath)
        else:
            print "Source file add to compare hash does not exist!"
            
    def hashCompareScore(self, lhs, rhs):
        return self.hasher.compare(lhs, rhs)
    
    def analyze2HashResultFiles(self, lFile, rFile):
        if lFile=="" or rFile=="":
            print "Hahs file to analyze is empty!"
            return 
        if os.path.splitext(lFile)[1] != ".json" or os.path.splitext(rFile)[1] != ".json":
            print "Hash file to analyze is not json file!"
            return 
        with open(lFile, 'r') as f:
            lData = json.load(f).get("HashResult", list())
        with open(rFile, 'r') as f:
            rData = json.load(f).get("HashResult", list())
        hash_MatchData = []
        for lElement in lData:
            lEleHash = lElement.get("HashValue")
            for rElement in rData:
                rEleHash = rElement.get("HashValue")
                score = self.hashCompareScore(lEleHash, rEleHash)
                # if score > 0, we just think they are similar
                if score == 0:
                    continue
                leftItem = dict(FunctionName=lElement.get("FunctionName"), SourceString=lElement.get("SourceString"))
                rightItem = dict(FunctionName=rElement.get("FunctionName"), SourceString=rElement.get("SourceString"))
                hash_MatchData.append(dict(Left=leftItem, Right=rightItem, Score=score)) 
        return hash_MatchData
        
    def analyzeAll(self):
        if len(self.sourceFiles) < 2:
            print "Files to do Hash Match must >= 2 !"
            return
        hash_MatchData = []
        FileCombinations = combinations(self.sourceFiles, 2)
        for item in FileCombinations:
            hash_MatchData = hash_MatchData + self.analyze2HashResultFiles(item[0], item[1])
        return hash_MatchData
    
    def startMatch(self):   
        resultData = self.analyzeAll()
        if resultData == None:
            return
        json_HashMatchData = dict(HashMacher=resultData)
        with open(self.resultFile , 'w+') as f:
            json.dump(json_HashMatchData, f)
        
        