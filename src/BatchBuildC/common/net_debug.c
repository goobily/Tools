#include "net_debug.h"

int net_initialize(void)
{
    WORD sock_ver = MAKEWORD(2,2);
    WSADATA data;

    return WSAStartup(sock_ver, &data);
}

void net_cleanup(void)
{
    WSACleanup();
}

SOCKET net_session_start(const char *host, u_short port)
{
    SOCKET sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock == INVALID_SOCKET)
    {
        return INVALID_SOCKET;
    }

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr.S_un.S_addr = inet_addr(host);
    if (connect(sock, (struct sockaddr *)&addr, sizeof(addr)) == SOCKET_ERROR)
    {
        int err = WSAGetLastError();
        closesocket(sock);
        WSASetLastError(err);
        return INVALID_SOCKET;
    }

    return sock;
}

void net_session_end(SOCKET sock)
{
    closesocket(sock);
}

int net_session_send_recv(SOCKET sock, const char *sdata, size_t slen, char *rbuffer, size_t rlen)
{
    int ret = send(sock, sdata, slen, 0);
    if (ret < 0)
    {
        return ret;
    }
    
    if (rbuffer && rlen)
    {
        return recv(sock, rbuffer, rlen, 0);
    }
	else
	{
		return ret;
	}
}

int net_session_print_recv(SOCKET sock, char *rbuf, size_t rlen, const char *fmt, ...)
{
    va_list vl;
    va_start(vl, fmt);

    int result = net_session_vprint_recv(sock, rbuf, rlen, fmt, vl);

    va_end(vl);

    return result;
}

int net_session_print(SOCKET sock, const char *fmt, ...)
{
    va_list vl;
    va_start(vl, fmt);

    int result = net_session_vprint_recv(sock, NULL, 0, fmt, vl);

    va_end(vl);

    return result;
}

int net_session_vprint_recv(SOCKET sock, char *rbuf, size_t rlen, const char *fmt, va_list vl)
{
	char buffer[1024 * 2];
    int result = vsnprintf(buffer, _countof(buffer), fmt, vl);
    if (result > 0) {
        result = net_session_send_recv(sock, buffer, result, rbuf, rlen);
    }

	return result;
}
