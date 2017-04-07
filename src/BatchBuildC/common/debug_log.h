#ifndef DEBUG_LOG_H_INCLUDED
#define DEBUG_LOG_H_INCLUDED

#pragma once

#include "common.h"

#include <stdarg.h>

EXTERN_C_GUARD_BEGIN

int output_debug(const char* fmt, ...);
int voutput_debug(const char* fmt, va_list vl);

EXTERN_C_GUARD_END

#endif // DEBUG_LOG_H_INCLUDED
