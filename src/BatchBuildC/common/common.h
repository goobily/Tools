#ifndef COMMON_C_INCLUDED
#define COMMON_C_INCLUDED

#pragma once

#ifdef __cplusplus
#define EXTERN_C_GUARD_BEGIN extern "C" {
#define EXTERN_C_GUARD_END }
#else
#define EXTERN_C_GUARD_BEGIN
#define EXTERN_C_GUARD_END
#endif // __cplusplus

#endif // COMMON_C_INCLUDED
