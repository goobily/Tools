from idc import *


def get_function_opcode(start_addr, end_addr):

    regex_str = ''
    p = start_addr

    while p < end_addr:
        b = Byte(p)
        regex_str += r"\x{0:02x}".format(b)
        p += 1
    return regex_str

def process_obj_zero_addr(function_name):
    with open(ARGV[1], "w") as f:
        start = 0
        end = 0x40 # default extract 64 bytes
        function_opcode_regex = get_function_opcode(start, end)
        f.write('%s = "%s"' % (function_name, function_opcode_regex))

def main():
    Wait()

    segaddr = MinEA()
    print "Base:%x\n" % (segaddr,)
    function_name = ARGV[2]
    with open(ARGV[1], "w") as f:
        addr = 0
        while addr != BADADDR:
            addr = NextFunction(addr)
            if addr == BADADDR:
                process_obj_zero_addr(function_name)
                break
            name = Name(addr)
            print 'name=', name
            end = GetFunctionAttr(addr, FUNCATTR_END)
            print 'start = %x' % addr
            print 'end = %x' % end

            #if not name or name.startswith("sub_") or GetFunctionAttr(addr, FUNCATTR_FLAGS) & FUNC_LIB == 0 or function_name not in name:
            #    continue
            if function_name not in name:
                continue
            function_opcode_regex = get_function_opcode(addr, end)

            f.write('%s = "%s"\r\n' % (name, function_opcode_regex))

if __name__ == '__main__':
    main()
    exit(0)
