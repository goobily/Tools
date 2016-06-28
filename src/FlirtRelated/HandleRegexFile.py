import sys
import os

def handleFile(in_file, out_file) :
    fw = open(out_file, 'w+')

    with open(in_file, 'r') as f:
        for line in f :
            line = line.strip()
            line = line.replace(' ', '')
            if not len(line):
                continue
            print 'line : ', line
            pos_fn_b = line.find('.') + 1
            pos_fn_e = line.find('=')
            fun_name = line[pos_fn_b:pos_fn_e]
            print 'function name ; ', fun_name
            pos_op_b = line.find('"', pos_fn_e)
            pos_op_e = line.find('"', pos_op_b+1)
            opcode = line[pos_op_b+1 : pos_op_e]
            print  'opcode : ', opcode
            opcode = opcode.replace('\\x','')
            #print 'opcode : ', opcode
            if len(opcode) > 128:
                opcode = opcode[:128]
            print 'opcode : ', opcode
            fw.write(fun_name+'\t=\t'+opcode+'\r\n')
    fw.close()

def main() :
    if len(sys.argv) != 3 :
        print 'usage : %s input_file out_file' % os.path.basename(__file__)
    handleFile(sys.argv[1], sys.argv[2])
    return

if __name__ == '__main__' :
    main()