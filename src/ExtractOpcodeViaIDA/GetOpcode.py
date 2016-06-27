import sys
import subprocess


def startIDA(command) :

    child = subprocess.Popen(command)
    print "child : ", child
    child.wait()
    print 'parent process'

def main():

    if len(sys.argv) < 6:
        print 'arguments should be: ida_path ida_script_path out_file_path function_name pe_file_path\n'
        print 'Example: GetOpcode.py "D:\Program Files (x86)\IDA 6.8\idaq.exe" "E:\MyCode\ICE\FLIRT\GetOpcdeIDAScript.py" "E:\\func.txt" wcscmp  "E:\MyCode\ICE\FLIRT\obj\wcscmp.obj"'
        return
    ida_path = sys.argv[1]
    ida_script_path = sys.argv[2]
    out_file_path = sys.argv[3]
    function_name = sys.argv[4]
    pe_file_path = sys.argv[5]
    command_line = '%s -c -A -S"%s %s %s" %s' % (ida_path, ida_script_path, out_file_path, function_name, pe_file_path)
    print 'command:', command_line
    startIDA(command_line)

if __name__ == '__main__':
    main()