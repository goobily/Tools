#ifndef NET_DEBUG_H_INCLUDED
#define NET_DEBUG_H_INCLUDED

#pragma once

#include <stddef.h>
#include <stdlib.h>
#include <winsock2.h>

#include "common.h"

EXTERN_C_GUARD_BEGIN

int net_initialize(void);
void net_cleanup(void);

SOCKET net_session_start(const char *host, u_short port);
void net_session_end(SOCKET sock);
int net_session_send_recv(SOCKET sock, const char *sdata, size_t slen, char *rbuffer, size_t rlen);
int net_session_print_recv(SOCKET sock, char *rbuf, size_t rlen, const char *fmt, ...);
int net_session_print(SOCKET sock, const char *fmt, ...);
int net_session_vprint_recv(SOCKET sock, char *rbuf, size_t rlen, const char *fmt, va_list vl);

EXTERN_C_GUARD_END

#endif // NET_DEBUG_H_INCLUDED