#include <idc.idc>

static main()
{

  auto addr, end, args, locals, frame, firstArg, name, ret ,handle, path, index, filename, outputfilename ,segaddr;

  addr = 0;

  Wait();    

  segaddr = MinEA();

  Message("Base:%x\n",segaddr);

  handle = fopen(ARGV[1],"w");

  for( addr = NextFunction(addr); addr != BADADDR; addr = NextFunction(addr))

  {
    name = Name(addr);

    end  = GetFunctionAttr(addr, FUNCATTR_END);
    if(substr(name,0,4) == "sub_")
		continue;
    
    Message("Function:%s, starts at %x,ends at %x\n", name, addr-segaddr, end-segaddr);

    fprintf(handle,"Function:%s, starts at %x,ends at %x\n", name, addr-segaddr, end-segaddr);

  }

  fclose(handle); 

  Exit(0);
}