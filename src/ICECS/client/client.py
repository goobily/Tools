
import os
import shutil
import time
import sys
import subprocess

REPORT_POSTFIX = ".output.txt"

MAX_TIME = 5
TIME_INTERVAL = 5

sampleFolder = "Z:\\VmShare\\sample"
workFolder = "C:\\Sample"
reportFolder = "C:\\ICELOG"
sharReportFolder = "Z:\\VmShare\\report"
    
def monitorReport(sampleFile, reportFolder) :
    bRet = False

    reportFile = sampleFile + REPORT_POSTFIX
    reportPath = os.path.join(reportFolder, reportFile)

    i = 0
    while os.path.exists(reportPath)==False and i<MAX_TIME/TIME_INTERVAL :
        time.sleep(TIME_INTERVAL)
        i += 1

    if os.path.exists(reportPath)==True :
        bRet = True
        print "++", reportFile
    else :
        print "--", reportFile
    return bRet

def monitorSample(sampleFolder) :
    bRet = False
    allSamples = os.listdir(sampleFolder)
    while len(allSamples)<1 :       
        time.sleep(TIME_INTERVAL)
        allSamples = os.listdir(sampleFolder)
        print "Wait sample"

    sample = allSamples[0]
    return sample
    
def runCommand(command, bWait = True):
        #logging.info("run command: [%s]" % (command))
        if bWait == True:
            subprocess.call(command)
        else:
            return subprocess.Popen(command)
            
def zip_result(sample_name, ice_result_folder):
    curDir = os.path.dirname(os.path.abspath(__file__))
    sevenZExecutable = os.path.join(curDir, "7z.exe")
    print "7z:", sevenZExecutable
    zip_name = sample_name + ".zip"
    outZip = os.path.join(curDir, zip_name)
    print "outZip:", outZip
    print "IceResultFolder:", ice_result_folder
    
    sevenZ_command = "%s a -tzip -pvirus %s -r %s\\*.cfg %s\\*.log" % (sevenZExecutable, outZip, ice_result_folder, ice_result_folder)
    print sevenZ_command
    runCommand(sevenZ_command)
    #runCommand("%s a -tzip -pvirus %s -r %s\\*.cfg %s\\*.log" % (sevenZExecutable, outZip, ice_result_folder, ice_result_folder))
    
    share_zip = os.path.join(sharReportFolder, zip_name)
    print "share_zip:", share_zip
    try:
      shutil.copyfile(outZip, share_zip)
    except IOError as e:
      print e
    
def main():
    
    if not os.path.exists(workFolder):
        os.mkdir(workFolder)
    if not os.path.exists(reportFolder):
        os.mkdir(reportFolder)
    #cmdStr = "c:\\IDA6.6\\idaq.exe -A -S\"c:\\ICE\\debugger.py\" "
    cmdStr = """
C:\ICE\Ice.py -s {0} -d {1} -x 55
"""
    while True :
        sample = monitorSample(sampleFolder)
        samplePath = os.path.join(sampleFolder, sample)
        workPath = os.path.join(workFolder, sample)
        print "samplepath:", samplePath
        print "workpath:", workPath
        try:
          shutil.copyfile(samplePath, workPath)
        except IOError as e:
          print e
          
        if not workPath.endswith(".exe"):
            newName = workPath + ".exe"
            os.rename(workPath, newName)
            workPath = newName
        #cmdStr += workPath
        cmdStr = cmdStr.format(workPath, reportFolder)
        print cmdStr
        try:
            os.system(cmdStr)
        except:
            pass
        #runCommand(cmdStr, True)
        print "Sample:", sample
        if os.path.exists(workPath):
            try:
                os.remove(workPath)
            except IOError as e:
                print e
        zip_result(sample, reportFolder)
        time.sleep(10)

if __name__ == '__main__':
    main()
