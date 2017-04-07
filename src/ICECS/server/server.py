
import os
import shutil
import time

REPORT_POSTFIX = ".zip"

MAX_TIME = 60
TIME_INTERVAL = 5

OriSampleFolder = "F:\\work\\CAWS2017\\sample"
OriReportFolder = "F:\\work\\CAWS2017\\report_no_MOT"
ShareSampleFolder = "F:\\VmShare\sample"
ShareReportFolder = "F:\\VmShare\\report"

def report_exists(sample_name, report_folder):
    sample_report_file = sample_name + REPORT_POSTFIX
    sample_report_path = os.path.join(report_folder, sample_report_file)
    return os.path.exists(sample_report_path)

def delete_file_folder(src):
    '''delete files and folders'''
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass
    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc=os.path.join(src,item)
            delete_file_folder(itemsrc)
    
def monitorReport(sampleFile, reportFolder) :
    bRet = False

    reportFile = sampleFile + REPORT_POSTFIX
    reportPath = os.path.join(reportFolder, reportFile)

    i = 0
    while not os.path.exists(reportPath) and i<60:
        time.sleep(TIME_INTERVAL)
        i += 1

    print "reportPath: ", reportPath
    if os.path.exists(reportPath):
        bRet = True
        print "++", reportFile
    else :
        print "--", reportFile
    if bRet:
        try:
            dest_report_path = os.path.join(OriReportFolder, reportFile)
            shutil.move(reportPath, dest_report_path)
        except IOError as e:
            print e
        finally:
            pass
    return bRet

def main():
   
    if not os.path.exists(ShareSampleFolder):
        os.mkdir(ShareSampleFolder)
    if not os.path.exists(ShareReportFolder):
        os.mkdir(ShareReportFolder)  
    if not os.path.exists(OriReportFolder):
        os.mkdir(OriReportFolder)
        
    failed = []
    counter = 0
    os.system("G:\\ICE\\revert_ice.bat")
    #while True :
    allSamples = os.listdir(OriSampleFolder)
    for sample in allSamples :
        if report_exists(sample, OriReportFolder):
            print "Already exist, Skip!!!!"
            continue
        samplePath = os.path.join(OriSampleFolder, sample)
        share_sample_path = os.path.join(ShareSampleFolder, sample)
        print "[ %d : %d ]" % (counter, len(failed))
        print ">>", sample  
        delete_file_folder(ShareSampleFolder)
        delete_file_folder(ShareReportFolder)
        try:
            shutil.copy(samplePath, share_sample_path)                         
            if monitorReport(sample, ShareReportFolder):
                #os.remove(share_sample_path)
                counter += 1
            else :
                failed.append(sample)
                allSamples += failed
                #os.system("G:\\ICE\\revert_ice.bat")           
        except IOError as e:
            print e 
        finally:            
            os.system("G:\\ICE\\revert_ice.bat")
            time.sleep(10)
        #delete_file_folder(ShareSampleFolder)
'''          
    allSamples += failed
    if len(allSamples)<1 :
        print "No samples in", sampleFolder
    time.sleep(5)
'''

if __name__ == '__main__':
    main()
