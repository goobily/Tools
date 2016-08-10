import sys
import subprocess

def startIDA(command) :

    child = subprocess.Popen(command)
    print "IDA begin to analyzing...."
    child.wait()
    print 'IDA end analyzing....'

def main():

    if len(sys.argv) < 5:
        print 'Four arguments needed: \n\t1.ida_path \n\t2.ida_script_path \n\t3.out_file_path \n\t4.pe_file_path\n'
        print 'Example:\nGetOpcode.py "D:\Program Files (x86)\IDA 6.8\idaq.exe" "E:\MyCode\ICE\FLIRT\GetOpcdeIDAScript.py" "E:\\func.txt" "E:\MyCode\ICE\FLIRT\obj\wcscmp.obj"'
        print '\nNote:\nEach Argument Should Be Enclosed In Double Quotation Marks If It Contains Whitespace!\n'
        return
    ida_path = '"%s"' % sys.argv[1]
    ida_script_path = sys.argv[2]
    out_file_path = sys.argv[3]
    pe_file_path = '"%s"' % sys.argv[4]
    ida_script_args = '"%s %s"' % (ida_script_path, out_file_path)
    print "ida_script_args", ida_script_args
    command_line = "%s -c -A -S%s %s" % (ida_path, ida_script_args, pe_file_path)
    print 'command:', command_line

    startIDA(command_line)

if __name__ == '__main__':
    main()