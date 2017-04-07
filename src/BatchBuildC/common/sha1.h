#ifndef SHA1_H
#define SHA1_H

typedef struct{
	unsigned int   total[2];
	unsigned int   state[5];
	unsigned char  buffer[64];
	unsigned char  digest[20];
}SHA1_CTX;

typedef struct {
	unsigned int	total[2];
	unsigned int	state[8];
	unsigned char	buffer[64];
	unsigned char	digest[32];
}SHA256_CTX;

typedef struct
{
	unsigned long long	total[2];
	unsigned long long state[8];
	unsigned char	buffer[128];
	unsigned char	digest[64];
}SHA512_CTX;

#define VULONG unsigned long
#define VULONGLONG unsigned long long
#define MEMSET memset
#define MEMCPY memcpy

#ifdef __cplusplus
extern "C" {
#endif //__cplusplus
void __VSSHA1Init( SHA1_CTX *ctx );
void __VSSHA1Update( SHA1_CTX *ctx, unsigned char *input, VULONG length);
void __VSSHA1Finish( SHA1_CTX *ctx);

void __VSSHA256Init( SHA256_CTX *ctx);
void __VSSHA256Update( SHA256_CTX * ctx, unsigned char *input, VULONG length);
void __VSSHA256Finish( SHA256_CTX *ctx);

void __VSSHA512Init( SHA512_CTX *ctx);
void __VSSHA512Update( SHA512_CTX * ctx, unsigned char *input, VULONGLONG length);
void __VSSHA512Finish( SHA512_CTX *ctx);
#ifdef __cplusplus
}
#endif //__cplusplus

#endif


