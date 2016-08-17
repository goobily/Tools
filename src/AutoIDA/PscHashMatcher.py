# coding: utf-8

import fuzzy_hash
import os
import json
from itertools import combinations
from PscResultManager import *

SAME_SCORE = 100
SAME_SCORE_COUNT = 20

SIMILAR_SCORE = 10

class HashMacher(object):
    def __init__(self, sourceFilesPath=""):
        self.sourceFiles = set()
        self.resultFolder = ""
        self.resultFile = ""       
        self.setResultFolder()
        self.setResultFile()
        self.addSourceFiles(sourceFilesPath)
        self.hasher = fuzzy_hash.FuzzyHash()
        self.file_hashes = set()
        self.match_result = list()
    def setResultFolder(self, dir=""):
        if dir != "":
            self.resultFolder = dir
        else:
            self.resultFolder = os.path.join(PscResultManager().getResultDir(), "HashMachResult")
        if not os.path.exists(self.resultFolder):
            os.mkdir(self.resultFolder)
            
    def setResultFile(self):
        self.resultFile = os.path.join(self.resultFolder, "HashMatchResult.json")
    
    def getMatchResult(self, file=""):
        file_parser = self.resultFile
        if not isEmptyFile(file):
            file_parser = file
        with open(file_parser, 'r') as f:
            return json.load(f).get("HashMacher", list())
            
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
    
    def fileHashCompareScore(self, lfile, rfile):
        lf_hash = self.hasher.hash_file(lfile)
        rf_hash = self.hasher.hash_file(rfile)
        return lf_hash, rf_hash, self.hasher.compare(lf_hash, rf_hash)
        
    def hashCompareScore(self, lhs, rhs):
        return self.hasher.compare(lhs, rhs)
    
    def stringCompareScore(self, lstr, rstr):
        lhs = self.hasher.hash_str(lstr)
        rhs = self.hasher.hash_str(rstr)
        return self.hashCompareScore(lhs, rhs)
    
    def convertHrData2MrData(self, hrFile):
        mrData = []
        if isEmptyFile(hrFile):
            return mrData
        with open(hrFile, 'r') as f:
            hrData = json.load(f).get("HashResult", list())
        for hrEle in hrData:
            item_opcodes = []
            item_opcodes.append(hrEle.get("Opcode"))
            item_hashes = []
            item_hashes.append(hrEle.get("Hash"))
            mrData.append(dict(Opcodes=item_opcodes, Hashes=item_hashes))
        return mrData
    
    def isInhashSet(self, hash_value, hash_set=list()):
        hash_set_ = self.file_hashes
        if len(hash_set) != 0:
            hash_set_ = hash_set
        for item in hash_set_:
            if self.hashCompareScore(hash_value, item) > SIMILAR_SCORE:
                return True
        return False
        
    def analyze2HashResultFiles(self, lFile, rFile):
        hash_MatchData = []
        if lFile=="" or rFile=="":
            print "Hash files to analyze is empty!"
            return hash_MatchData
        if os.path.splitext(lFile)[1] != ".json" or os.path.splitext(rFile)[1] != ".json":
            print "Hash files to analyze is not json file!"
            return hash_MatchData
        with open(lFile, 'r') as f:
            lData = json.load(f).get("HashResult", list())
        with open(rFile, 'r') as f:
            rData = json.load(f).get("HashResult", list())
        lFile_hash, rFile_hash, file_hash_score = self.fileHashCompareScore(lFile, rFile) 
        if file_hash_score > SIMILAR_SCORE:  # file hash prefilter
            print "Equal hash file, just return hash file."
            if self.isInhashSet(lFile_hash) or self.isInhashSet(rFile_hash):
                return hash_MatchData
            self.file_hashes.add(lFile_hash)
            self.file_hashes.add(rFile_hash)
            return self.convertHrData2MrData(lFile)
            
        hash_MatchData = []
        same_score_num = 0
        for lElement in lData:
            lEleHash = lElement.get("Hash")
            lEleOpocode = lElement.get("Opcode")
            for rElement in rData:
                rEleHash = rElement.get("Hash")
                rEleOpcode = rElement.get("Opcode")
                score = self.hashCompareScore(lEleHash, rEleHash)
                # if score > SIMILAR_SCORE, we just think they are similar
                if score <= SIMILAR_SCORE:
                    continue
                else:
                    item_opcodes = []
                    item_opcodes.append(lEleOpocode)
                    item_opcodes.append(rEleOpcode)
                    item_opcodes = list(set(item_opcodes))
                    
                    item_hashes = []
                    item_hashes.append(lEleHash)
                    item_hashes.append(rEleHash)
                    item_hashes = list(set(item_hashes))

                    if score >= SAME_SCORE and same_score_num < SAME_SCORE_COUNT:
                        same_score_num += 1
                    # if lFile and rFile have more than SAME_SCORE_COUNT funtions score SAME_SCORE, we just think they are the same
                    elif same_score_num >= SAME_SCORE_COUNT: 
                        return self.convertHrData2MrData(lFile)
                    else:
                        hash_MatchData.append(dict(Opcodes=item_opcodes, Hashes=item_hashes)) 
        return hash_MatchData

    def analyzeAll(self):
        if len(self.sourceFiles) < 2:
            print "Files to do Hash Match must >= 2 !"
            return
        self.file_hashes = set()
        FileCombinations = combinations(self.sourceFiles, 2)
        for item in FileCombinations:
            #if isEqualFile(item[0], item[1]): # ignore the same files
            #    continue
            result_analyze2Files = self.analyze2HashResultFiles(item[0], item[1])
            if len(result_analyze2Files)>0:
                self.mergeMatchResult(result_analyze2Files)
    
    def uniqueMatchResult(self):
        remove_duplicate_result = []
        for item in self.match_result:
            item_opcodes = item.get("Opcodes", list())
            item_opcodes = list(set(item_opcodes))
            item_hashes = item.get("Hashes", list())
            item_hashes = list(set(item_hashes))
            remove_duplicate_result.append(dict(Opcodes=item_opcodes, Hashes=item_hashes))
        self.match_result = remove_duplicate_result
        
    def mergeMatchResult(self, new_match_result):
        if len(self.match_result) == 0:
            self.match_result = new_match_result
        else:
            same_score_num = 0
            for r_index in range(len(self.match_result)-1, -1, -1):
                match_flag = False
                item_r_opcodes = self.match_result[r_index].get("Opcodes", list())
                item_r_hashes = self.match_result[r_index].get("Hashes", list())
                for item_n in new_match_result:
                    item_n_opcodes = item_n.get("Opcodes", list())
                    item_n_hashes = item_n.get("Hashes", list())
                    
                    if self.hashCompareScore(item_r_hashes[0], item_n_hashes[0]) >= SAME_SCORE:
                        same_score_num += 1
                        if same_score_num >= SAME_SCORE_COUNT:
                            print "Hash compare score [%d] more than [%d] times, just think they are the same." % (SAME_SCORE, SAME_SCORE_COUNT)
                            self.uniqueMatchResult()
                            return
                        continue
                    # hash compare score > 0 , we just think they are similar
                    if self.hashCompareScore(item_r_hashes[0], item_n_hashes[0]) > SIMILAR_SCORE: 
                        match_flag = True
                        item_r_opcodes += item_n_opcodes
                        item_r_hashes += item_n_hashes
                # remove not matched item in result set to speed up the match routine        
                if match_flag == False:
                    self.match_result.pop(r_index)
        self.uniqueMatchResult()
    
    def newStartMatch(self):
        source_files_num = len(self.sourceFiles)
        if source_files_num == 0:
            print "No hash files to match!"
            return
        if source_files_num == 1:
            print "Just one hash file, no need to match!"
        for file in self.sourceFiles:
            file_hash = self.hasher.hash_file(file)
            if self.isInhashSet(file_hash):
                print "Equal hash file already exists!"
                continue
            self.file_hashes.add(file_hash)
            self.mergeMatchResult(self.convertHrData2MrData(file))
            
        self.uniqueMatchResult()
        json_HashMatchData = dict(HashMacher=self.match_result)
        with open(self.resultFile , 'w+') as f:
            json.dump(json_HashMatchData, f)   
            
    def mergeMatch(self, data_set=list()):
        print "[Merge] Data Set Size = [%d]" % len(data_set)
        if len(data_set) == 0:
            print "Data set empty, nothing to merge!"
            return
        """
        elif len(data_set) == 1:
            print "Data set just one item, no need to merge!"
            return data_set
        """
        merge_result = list()
        for item in data_set[0]:
            result_item_opcode = []
            result_item_opcode.append(item.get("Left").get("Opcode"))
            result_item_opcode.append(item.get("Right").get("Opcode"))
            result_item_opcode = list(set(result_item_opcode))
            
            result_item_hash = []
            result_item_hash.append(item.get("Left").get("Hash"))
            result_item_hash.append(item.get("Right").get("Hash"))
            result_item_hash = list(set(result_item_hash))
            
            merge_result.append(dict(Opcodes=result_item_opcode, Hashes=result_item_hash))
        i = 1
        while i < len(data_set):
            merge_pair = []
            for item in data_set[i]:
                item_i_opcode = []
                item_i_opcode.append(item.get("Left").get("Opcode"))
                item_i_opcode.append(item.get("Right").get("Opcode"))
                item_i_opcode = list(set(item_i_opcode))
                
                item_i_hash = []
                item_i_hash.append(item.get("Left").get("Hash"))
                item_i_hash.append(item.get("Right").get("Hash"))
                item_i_hash = list(set(item_i_hash))
                
                merge_pair.append(dict(Opcodes=item_i_opcode, Hashes=item_i_hash))
            
            for r_index in range(len(merge_result)-1, -1, -1):
                match_flag = False
                item_r_opcodes = merge_result[r_index].get("Opcodes", list())
                item_r_hashes = merge_result[r_index].get("Hashes", list())
                for item_m in merge_pair:
                    item_m_opcodes = item_m.get("Opcodes", list())
                    item_m_hashes = item_m.get("Hashes", list())
                    # hash compare score > 0 , we just think they are similar
                    if self.hashCompareScore(item_r_hashes[0], item_m_hashes[0]) > 0: 
                        match_flag = True
                        item_r_opcodes += item_m_opcodes
                        item_r_opcodes = list(set(item_r_opcodes))
                        item_r_hashes += item_m_hashes
                        item_r_hashes = list(set(item_r_hashes))
                # remove not matched item in result set to speed up the match routine        
                if match_flag == False:
                    merge_result.pop(r_index)
            i += 1
            
        remove_duplicate_result = []
        for item in merge_result:
            item_opcodes = item.get("Opcodes", list())
            item_opcodes = list(set(item_opcodes))
            item_hashes = item.get("Hashes", list())
            item_hashes = list(set(item_hashes))
            remove_duplicate_result.append(item)
        merge_result = []   
        return remove_duplicate_result
    
    def startMatch(self):   
        self.analyzeAll()
        """
        hash_compare_result = self.analyzeAll()
        if hash_compare_result == None:
            return  
        hash_match_result = self.mergeMatch(hash_compare_result)
        if hash_match_result == None:
            return
        """    
        json_HashMatchData = dict(HashMacher=self.match_result)
        with open(self.resultFile , 'w+') as f:
            json.dump(json_HashMatchData, f)
        
        