import sys
import os
import subprocess
import zipfile
import shutil

def runICE(in_dir, out_path):

    #cmd = ["python", "Ice.py", "-s"]

    for root, dirs, files in os.walk(in_dir):
        for file in files:
            cmd = ["python", "Ice.py", "-s"]
            targetFile = os.path.join(root, file)
            cmd.append(targetFile)
            cmd.append("-d")
            cmd.append(out_path)
            retval = subprocess.call(cmd,0,None,None,None,None)
            print 'retval: ', retval

    # compress report
    report_folder = os.path.join(out_path, 'report')
    f = zipfile.ZipFile('report.zip', 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(report_folder):
        for filename in filenames:
            f.write(os.path.join(dirpath, filename))
    f.close()
    #shutil.move('report.zip')
    return

def main():
    if len(sys.argv) != 3:
        print "usage: ", os.path.basename(__file__), " in_dir out_path"
        return
    if not os.path.exists(sys.argv[1]):
        print 'ERROR: input dir not exist!'
        return
    runICE(sys.argv[1], sys.argv[2])

    return
if __name__ == '__main__':
    main()