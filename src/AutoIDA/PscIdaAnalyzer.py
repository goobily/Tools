# coding: utf-8

import subprocess
import os
import fuzzy_hash
import json
import sys

class IdaAnalyzer(object):
    def __init__(self):
        self.idaPath = ""
        self.idaScriptPath = ""
        self.resultFilePath = ""
        self.peFilePath = ""
        self.resultHasher = IdaResultHasher()
    def setIdapath(self, path=""):
        self.idaPath = path
    
    def setIdaScriptPath(self, path=""):
        self.idaScriptPath = path
    
    def setResultFilePath(self, path=""):
        self.resultFilePath = path
        
    def setPeFilePath(self, path=""):
        self.peFilePath = path
    
    def buildCommand(self):
        command = ""
        if self.idaPath == "":
            raise RuntimeError("IDA path can't be empty. IdaPath=[%s]" % self.idaPath)
        elif self.idaScriptPath == "":
            raise RuntimeError("IDA script path can't be empty. IdaScriptPath=[%s]" % self.idaScriptPath)
        elif self.peFilePath == "":
            raise RuntimeError("Pe File can't be empty. PeFilePath=[%s]" % self.peFilePath)
        elif self.resultFilePath == "":
            currentDir = os.path.split(os.path.realpath(__file__))[0]
            resultDir = os.path.join(currentDir, "IDAResult")
            if not os.path.exists(resultDir):
                os.mkdir(resultDir)
            resultFileName = os.path.basename(os.path.splitext(self.peFilePath)[0] + '.txt')
            self.resultFilePath = os.path.join(resultDir, resultFileName)
        ida_script_args = '"%s %s"' % (self.idaScriptPath, self.resultFilePath)
        print "IDA Script Args: ", ida_script_args
        ida_Path = '"%s"' % (self.idaPath)
        pe_file_path = '"%s"' % self.peFilePath
        print "Target File: ", pe_file_path
        
        self.command = "%s -c -A -S%s %s" % (ida_Path,ida_script_args, pe_file_path)
        
    def start(self, command=""):
        if command == "":
            self.buildCommand()
        else:
            self.command = command
        print "command: \n%s" % self.command    
        child = subprocess.Popen(self.command)
        print "IDA begin to analyzing...."
        child.wait()
        print 'IDA end analyzing....'
        self.resultHasher.generateHash(self.resultFilePath)

class IdaResultHasher(object):
    def __init__(self, sourceFile=""):
        self.sourceFile = sourceFile
        self.hasher = fuzzy_hash.FuzzyHash()
    def generateHash(self, sourceFile=""):
        if sourceFile != "":
            self.sourceFile = sourceFile
        data = []
        if self.sourceFile == "":
            raise RuntimeError("File to hash not specified!")
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
        
        current_dir = os.path.dirname(self.sourceFile)    
        json_fileName = os.path.join(current_dir, os.path.basename(os.path.splitext(self.sourceFile)[0] + '.json'))
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