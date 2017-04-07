#include "debug_log.h"

#include <stdlib.h>
#include <stdio.h>
#include <windows.h>

int output_debug(const char* fmt, ...)
{
    va_list vl;
    va_start(vl, fmt);

    int result = voutput_debug(fmt, vl);

    va_end(vl);

    return result;
}

int voutput_debug(const char * fmt, va_list vl)
{
    char buffer[1024 * 2];
    int result = vsnprintf(buffer, _countof(buffer), fmt, vl);

    OutputDebugStringA(buffer);

    return result;
}
