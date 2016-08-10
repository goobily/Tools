from idc import *

def get_function_opcode(start_addr, end_addr):
    regex_str = ''
    p = start_addr
    while p < end_addr:
        b = Byte(p)
        regex_str += r"\x{0:02x}".format(b)
        p += 1
    return regex_str

def main():
    addr = 0
    Wait()
    segaddr = MinEA()
    print 'Base:%x', segaddr
    with open(ARGV[1], "w") as f:
        addr = NextFunction(addr)
        while addr!= BADADDR:
            name = Name(addr)
            end = GetFunctionAttr(addr, FUNCATTR_END)
            if name[0:4] == "sub_":
                function_opcode_regex = get_function_opcode(addr, end)
                f.write('%s = "%s"\r\n' % (name, function_opcode_regex))
            addr = NextFunction(addr)
    Exit(0)
    
if __name__ == '__main__':
    main()
    