# coding: utf-8

import sys
import os
import PscIdaAnalyzer

def IdaProcess(idaPath, idaScriptPath, peFilePath):
    IdaAnalyzer = PscIdaAnalyzer.IdaAnalyzer()
    IdaAnalyzer.setIdapath(idaPath)
    IdaAnalyzer.setIdaScriptPath(idaScriptPath)
    IdaAnalyzer.setPeFilePath(peFilePath)
    
    IdaAnalyzer.start()
    
def main():

    if len(sys.argv) != 4:
        print 'Usage: Three arguments needed: \n\t1.ida_path (file) \n\t2.ida_script_path (file) \n\t3.pe_file_path (file/dir)\n'
        print 'Example:\nPsc.py "D:\Program Files (x86)\IDA 6.8\idaq.exe" "E:\IDAScript_dumpfunc.py" "E:\sample\\test.exe"'
        print '\nNote:\nEach Argument Should Be Enclosed In Double Quotation Marks If It Contains Whitespace!\n'
        return
    
    ida_path = sys.argv[1]
    ida_script_path = sys.argv[2]
    pe_file_path = sys.argv[3]
    
    if os.path.isfile(pe_file_path):
        IdaProcess(ida_path, ida_script_path, pe_file_path)
    elif os.path.isdir(pe_file_path):
        for root, dirs, files in os.walk(pe_file_path):
            for file in files:
                file_path = os.path.join(root, file)
                IdaProcess(ida_path, ida_script_path, file_path)
    else:
        raise RuntimeError("Target file/dir not exist!")
        
if __name__ == '__main__':
    main()