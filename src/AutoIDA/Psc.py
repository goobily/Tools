# coding: utf-8

import sys
import os
from PscIdaAnalyzer import *
from PscHashMatcher import *


def IdaProcess(idaAnalyzer, idaPath, idaScriptPath, peFilePath):
    idaAnalyzer.initEnvironment(idaPath, idaScriptPath, peFilePath)
    if os.path.isfile(peFilePath):
        idaAnalyzer.setPeFilePath(peFilePath)
        idaAnalyzer.startAnalyze()
    elif os.path.isdir(peFilePath):
        for root, dirs, files in os.walk(peFilePath):
            for file in files:
                file_path = os.path.join(root, file)
                idaAnalyzer.setPeFilePath(file_path)
                idaAnalyzer.startAnalyze()
    else:
        raise RuntimeError("Target file/dir not exist!")
    
def main():

    if len(sys.argv) != 5:
        print 'Usage: Four arguments needed: \n\t1.ida_path (file) \n\t2.ida_script_path (file) \n\t3.pe_file_path (file/dir) \n\t4.result_folder'
        print 'Example:\nPsc.py "D:\Program Files (x86)\IDA 6.8\idaq.exe" "E:\IDAScript_dumpfunc.py" "E:\sample\\test.exe" "E:\\result"'
        print '\nNote:\nEach Argument Should Be Enclosed In Double Quotation Marks If It Contains Whitespace!\n'
        return
    
    PscResultManager(sys.argv[4])
    ida_analyzer = IdaAnalyzer()
    IdaProcess(ida_analyzer, sys.argv[1], sys.argv[2], sys.argv[3])
    
    hash_matcher = HashMacher(ida_analyzer.getResultHasher().getResultFolder())
    hash_matcher.newStartMatch()
    
    
if __name__ == '__main__':
    main()