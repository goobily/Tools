# coding: utf-8

import subprocess
import os
import fuzzy_hash
import json
import sys
from PscResultManager import *

class IdaAnalyzer(object):
    def __init__(self):
        self.idaPath = ""
        self.idaScriptPath = ""
        self.resultFile = ""
        self.resultFolder = ""
        self.peFilePath = ""
        self.resultHasher = None
        self.setResultHasher()
        self.setResultFolder()
     
    def initEnvironment(self, idaPath, idaScriptPath, peFilePath="", resultFolder=""):
        self.setIdapath(idaPath)
        self.setIdaScriptPath(idaScriptPath)
        self.setPeFilePath(peFilePath)
        self.setResultFolder(resultFolder)
        
    def setIdapath(self, path=""):
        self.idaPath = path
    
    def setIdaScriptPath(self, path=""):
        self.idaScriptPath = path
    
    def setResultFile(self, path=""):
        if path != "":
            self.resultFile = path
        result_file_name = os.path.basename(os.path.splitext(self.peFilePath)[0] + '.txt')
        self.resultFile = os.path.join(self.resultFolder, result_file_name)
    
    def setResultFolder(self, dir=""):
        if dir != "":
            self.resultFolder = dir
        else:
            self.resultFolder = os.path.join(PscResultManager().getResultDir(), "IDAResult")
        if not os.path.exists(self.resultFolder):
            os.mkdir(self.resultFolder)  
        
    def getResultFolder(self):
        return self.resultFolder
        
    def setPeFilePath(self, path=""):
        self.peFilePath = path
        self.setResultFile()
        
    def setResultHasher(self):
        self.resultHasher = IdaResultHasher()
    
    def getResultHasher(self):
        return self.resultHasher
        
    def buildCommand(self):
        command = ""
        if self.idaPath == "":
            raise RuntimeError("IDA path can't be empty. IdaPath=[%s]" % self.idaPath)
        elif self.idaScriptPath == "":
            raise RuntimeError("IDA script path can't be empty. IdaScriptPath=[%s]" % self.idaScriptPath)
        elif self.peFilePath == "":
            raise RuntimeError("Pe File can't be empty. PeFilePath=[%s]" % self.peFilePath)
        elif self.resultFile == "":
            self.setResultFile()            
        ida_script_args = '"%s %s"' % (self.idaScriptPath, self.resultFile)
        print "IDA Script Args: ", ida_script_args
        ida_Path = '"%s"' % (self.idaPath)
        pe_file_path = '"%s"' % self.peFilePath
        print "Target File: ", pe_file_path
        
        self.command = "%s -c -A -S%s %s" % (ida_Path,ida_script_args, pe_file_path)
        
    def startAnalyze(self, command=""):
        if command == "":
            self.buildCommand()
        else:
            self.command = command
        print "command: \n%s" % self.command    
        child = subprocess.Popen(self.command)
        print "IDA begin to analyzing...."
        child.wait()
        print 'IDA end analyzing....'
        
        if os.path.exists(self.resultFile) and isEmptyFile(self.resultFile):
            os.remove(self.resultFile)
            return   
        if os.path.exists(self.resultFile):
            if self.resultHasher != None:
                self.resultHasher.generateHash(self.resultFile)

class IdaResultHasher(object):
    def __init__(self, sourceFile=""):
        self.sourceFile = sourceFile
        self.resultFolder = ""
        self.hasher = fuzzy_hash.FuzzyHash()
        self.setResultFolder()
        
    def setResultFolder(self, result_folder=""):
        if result_folder != "":
            self.resultFolder = result_folder
        else:
            self.resultFolder = os.path.join(PscResultManager().getResultDir(), "HashFile")
        if not os.path.exists(self.resultFolder):
            os.mkdir(self.resultFolder) 
            
    def getResultFolder(self):
        return self.resultFolder
        
    def generateHash(self, sourceFile=""):
        if sourceFile != "":
            self.sourceFile = sourceFile
        data = []
        if self.sourceFile == "" or not os.path.exists(self.sourceFile):
            print "File to generate hash does not exists! [file: %s]" % self.sourceFile
            return
        with open(self.sourceFile, 'r') as f:
            for line in f:
                line = line.strip()
                if len(line) == 0:
                    continue
                #print 'line : ', line
                line_splits = line.split("=")
                functionName = line_splits[0]
                opcodeSeries = line_splits[1].replace('"', "").strip()
                #print "FunctionName: ", functionName
                #print "Opcode Series: ", opcodeSeries
                hash_OpocdeSeries = self.hasher.hash_str(opcodeSeries)
                hash_item = dict(FunctionName =functionName, HashValue=hash_OpocdeSeries, SourceString=opcodeSeries)
                
                data.append(hash_item)

        json_fileName = os.path.join(self.resultFolder, os.path.basename(os.path.splitext(self.sourceFile)[0] + '.json'))
        print "Result Json File: ", json_fileName 
        json_data = dict(HashResult=data)
        with open(json_fileName, 'w+') as f:
            json.dump(json_data, f)

'''  
def main():
    if len(sys.argv) < 2:
        print "Input IDA result file!"
        return
    else:
        Hasher = IdaResultHasher(sys.argv[1])
        Hasher.generateHash()
    
if __name__ == '__main__':
    main()
'''    