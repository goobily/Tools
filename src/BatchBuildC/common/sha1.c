/*
 *****************************************************************************
 *
 *	(C) Copyright 1989-2009 Trend Micro, Inc.
 *	All Rights Reserved.
 *
 *	This program is an unpublished copyrighted work which is proprietary
 *	to Trend Micro, Inc. and contains confidential information that is not
 *	to be reproduced or disclosed to any other person or entity without
 *	prior written consent from Trend Micro, Inc. in each and every instance.
 *
 *	WARNING:  Unauthorized reproduction of this program as well as
 *	unauthorized preparation of derivative works based upon the
 *	program or distribution of copies by sale, rental, lease or
 *	lending are violations of federal copyright laws and state trade
 *	secret laws, punishable by civil and criminal penalties.
 *
 */

/*==========================================================================*/
/* sha1.c */
/* This file is copied from AEGIS's source code */
/* Due to consistency issue, 
   please do not modify coding in this file without consulting VSAPI's RDs.

Sample of use:
   // Open File
   __VSSHA1Init(&ctx);
   while (// Read File) {
       __VSSHA1Update(...);
   }
   // Close File
   __VSSHA1Finish(&ctx);
*/
#include "sha1.h"
#include <windows.h>

#define GET_VULONG(n,b,i)                       \
{                                               \
    (n) = ( (VULONG) (b)[(i)    ] << 24 )       \
        | ( (VULONG) (b)[(i) + 1] << 16 )       \
        | ( (VULONG) (b)[(i) + 2] <<  8 )       \
        | ( (VULONG) (b)[(i) + 3]       );      \
}

#define PUT_VULONG(n,b,i)                       \
{                                               \
    (b)[(i)    ] = (unsigned char) ( (n) >> 24 );       \
    (b)[(i) + 1] = (unsigned char) ( (n) >> 16 );       \
    (b)[(i) + 2] = (unsigned char) ( (n) >>  8 );       \
    (b)[(i) + 3] = (unsigned char) ( (n)       );       \
}

#define GET_VULONGLONG(n,b,i)                            \
{                                                       \
	(n) = ( (unsigned long long) (b)[(i)    ] << 56 )       \
	| ( (unsigned long long) (b)[(i) + 1] << 48 )       \
	| ( (unsigned long long) (b)[(i) + 2] << 40 )       \
	| ( (unsigned long long) (b)[(i) + 3] << 32 )       \
	| ( (unsigned long long) (b)[(i) + 4] << 24 )       \
	| ( (unsigned long long) (b)[(i) + 5] << 16 )       \
	| ( (unsigned long long) (b)[(i) + 6] <<  8 )       \
	| ( (unsigned long long) (b)[(i) + 7]       );      \
}

#define PUT_VULONGLONG(n,b,i)                            \
{                                                       \
	(b)[(i)    ] = (unsigned char) ( (n) >> 56 );       \
	(b)[(i) + 1] = (unsigned char) ( (n) >> 48 );       \
	(b)[(i) + 2] = (unsigned char) ( (n) >> 40 );       \
	(b)[(i) + 3] = (unsigned char) ( (n) >> 32 );       \
	(b)[(i) + 4] = (unsigned char) ( (n) >> 24 );       \
	(b)[(i) + 5] = (unsigned char) ( (n) >> 16 );       \
	(b)[(i) + 6] = (unsigned char) ( (n) >>  8 );       \
	(b)[(i) + 7] = (unsigned char) ( (n)       );       \
}

/*
 * Round constants
 */
static const unsigned long long K[80] =
{
    0x428A2F98D728AE22,  0x7137449123EF65CD,
    0xB5C0FBCFEC4D3B2F,  0xE9B5DBA58189DBBC,
    0x3956C25BF348B538,  0x59F111F1B605D019,
    0x923F82A4AF194F9B,  0xAB1C5ED5DA6D8118,
    0xD807AA98A3030242,  0x12835B0145706FBE,
    0x243185BE4EE4B28C,  0x550C7DC3D5FFB4E2,
    0x72BE5D74F27B896F,  0x80DEB1FE3B1696B1,
    0x9BDC06A725C71235,  0xC19BF174CF692694,
    0xE49B69C19EF14AD2,  0xEFBE4786384F25E3,
    0x0FC19DC68B8CD5B5,  0x240CA1CC77AC9C65,
    0x2DE92C6F592B0275,  0x4A7484AA6EA6E483,
    0x5CB0A9DCBD41FBD4,  0x76F988DA831153B5,
    0x983E5152EE66DFAB,  0xA831C66D2DB43210,
    0xB00327C898FB213F,  0xBF597FC7BEEF0EE4,
    0xC6E00BF33DA88FC2,  0xD5A79147930AA725,
    0x06CA6351E003826F,  0x142929670A0E6E70,
    0x27B70A8546D22FFC,  0x2E1B21385C26C926,
    0x4D2C6DFC5AC42AED,  0x53380D139D95B3DF,
    0x650A73548BAF63DE,  0x766A0ABB3C77B2A8,
    0x81C2C92E47EDAEE6,  0x92722C851482353B,
    0xA2BFE8A14CF10364,  0xA81A664BBC423001,
    0xC24B8B70D0F89791,  0xC76C51A30654BE30,
    0xD192E819D6EF5218,  0xD69906245565A910,
    0xF40E35855771202A,  0x106AA07032BBD1B8,
    0x19A4C116B8D2D0C8,  0x1E376C085141AB53,
    0x2748774CDF8EEB99,  0x34B0BCB5E19B48A8,
    0x391C0CB3C5C95A63,  0x4ED8AA4AE3418ACB,
    0x5B9CCA4F7763E373,  0x682E6FF3D6B2B8A3,
    0x748F82EE5DEFB2FC,  0x78A5636F43172F60,
    0x84C87814A1F0AB72,  0x8CC702081A6439EC,
    0x90BEFFFA23631E28,  0xA4506CEBDE82BDE9,
    0xBEF9A3F7B2C67915,  0xC67178F2E372532B,
    0xCA273ECEEA26619C,  0xD186B8C721C0C207,
    0xEADA7DD6CDE0EB1E,  0xF57D4F7FEE6ED178,
    0x06F067AA72176FBA,  0x0A637DC5A2C898A6,
    0x113F9804BEF90DAE,  0x1B710B35131C471B,
    0x28DB77F523047D84,  0x32CAAB7B40C72493,
    0x3C9EBE0A15C9BEBC,  0x431D67C49C100D4C,
    0x4CC5D4BECB3E42B6,  0x597F299CFC657E2A,
    0x5FCB6FAB3AD6FAEC,  0x6C44198C4A475817
};

static unsigned char sha1_padding[64] =
{
 0x80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
};

void __VSSHA1Init( SHA1_CTX *ctx )
{
    ctx->total[0] = 0;
    ctx->total[1] = 0;

    ctx->state[0] = 0x67452301;
    ctx->state[1] = 0xEFCDAB89;
    ctx->state[2] = 0x98BADCFE;
    ctx->state[3] = 0x10325476;
    ctx->state[4] = 0xC3D2E1F0;
    MEMSET(ctx->digest, 0, sizeof(ctx->digest));
	MEMSET(ctx->buffer, 0, sizeof(ctx->buffer));
}

/**
 * Description:
 *  Function will update ctx with input data[64].
 * Parameters:
 *  ctx : [IN] SHA1_CTX
 *        [OUT] ctx->state
 * Return:
 *  No.
 */
static void sha1_process( SHA1_CTX *ctx, unsigned char data[64] )
{
    VULONG temp, W[16], A, B, C, D, E;

    GET_VULONG( W[0],  data,  0 );
    GET_VULONG( W[1],  data,  4 );
    GET_VULONG( W[2],  data,  8 );
    GET_VULONG( W[3],  data, 12 );
    GET_VULONG( W[4],  data, 16 );
    GET_VULONG( W[5],  data, 20 );
    GET_VULONG( W[6],  data, 24 );
    GET_VULONG( W[7],  data, 28 );
    GET_VULONG( W[8],  data, 32 );
    GET_VULONG( W[9],  data, 36 );
    GET_VULONG( W[10], data, 40 );
    GET_VULONG( W[11], data, 44 );
    GET_VULONG( W[12], data, 48 );
    GET_VULONG( W[13], data, 52 );
    GET_VULONG( W[14], data, 56 );
    GET_VULONG( W[15], data, 60 );

#define S(x,n) ((x << n) | ((x & 0xFFFFFFFF) >> (32 - n)))

#define R(t)                                            \
(                                                       \
    temp = W[(t -  3) & 0x0F] ^ W[(t - 8) & 0x0F] ^     \
           W[(t - 14) & 0x0F] ^ W[ t      & 0x0F],      \
    ( W[t & 0x0F] = S(temp,1) )                         \
)

#define P(a,b,c,d,e,x)                                  \
{                                                       \
    e += S(a,5) + F(b,c,d) + K + x; b = S(b,30);        \
}

    A = ctx->state[0];
    B = ctx->state[1];
    C = ctx->state[2];
    D = ctx->state[3];
    E = ctx->state[4];

#define F(x,y,z) (z ^ (x & (y ^ z)))
#define K 0x5A827999

    P( A, B, C, D, E, W[0]  );
    P( E, A, B, C, D, W[1]  );
    P( D, E, A, B, C, W[2]  );
    P( C, D, E, A, B, W[3]  );
    P( B, C, D, E, A, W[4]  );
    P( A, B, C, D, E, W[5]  );
    P( E, A, B, C, D, W[6]  );
    P( D, E, A, B, C, W[7]  );
    P( C, D, E, A, B, W[8]  );
    P( B, C, D, E, A, W[9]  );
    P( A, B, C, D, E, W[10] );
    P( E, A, B, C, D, W[11] );
    P( D, E, A, B, C, W[12] );
    P( C, D, E, A, B, W[13] );
    P( B, C, D, E, A, W[14] );
    P( A, B, C, D, E, W[15] );
    P( E, A, B, C, D, R(16) );
    P( D, E, A, B, C, R(17) );
    P( C, D, E, A, B, R(18) );
    P( B, C, D, E, A, R(19) );

#undef K
#undef F

#define F(x,y,z) (x ^ y ^ z)
#define K 0x6ED9EBA1

    P( A, B, C, D, E, R(20) );
    P( E, A, B, C, D, R(21) );
    P( D, E, A, B, C, R(22) );
    P( C, D, E, A, B, R(23) );
    P( B, C, D, E, A, R(24) );
    P( A, B, C, D, E, R(25) );
    P( E, A, B, C, D, R(26) );
    P( D, E, A, B, C, R(27) );
    P( C, D, E, A, B, R(28) );
    P( B, C, D, E, A, R(29) );
    P( A, B, C, D, E, R(30) );
    P( E, A, B, C, D, R(31) );
    P( D, E, A, B, C, R(32) );
    P( C, D, E, A, B, R(33) );
    P( B, C, D, E, A, R(34) );
    P( A, B, C, D, E, R(35) );
    P( E, A, B, C, D, R(36) );
    P( D, E, A, B, C, R(37) );
    P( C, D, E, A, B, R(38) );
    P( B, C, D, E, A, R(39) );

#undef K
#undef F

#define F(x,y,z) ((x & y) | (z & (x | y)))
#define K 0x8F1BBCDC

    P( A, B, C, D, E, R(40) );
    P( E, A, B, C, D, R(41) );
    P( D, E, A, B, C, R(42) );
    P( C, D, E, A, B, R(43) );
    P( B, C, D, E, A, R(44) );
    P( A, B, C, D, E, R(45) );
    P( E, A, B, C, D, R(46) );
    P( D, E, A, B, C, R(47) );
    P( C, D, E, A, B, R(48) );
    P( B, C, D, E, A, R(49) );
    P( A, B, C, D, E, R(50) );
    P( E, A, B, C, D, R(51) );
    P( D, E, A, B, C, R(52) );
    P( C, D, E, A, B, R(53) );
    P( B, C, D, E, A, R(54) );
    P( A, B, C, D, E, R(55) );
    P( E, A, B, C, D, R(56) );
    P( D, E, A, B, C, R(57) );
    P( C, D, E, A, B, R(58) );
    P( B, C, D, E, A, R(59) );

#undef K
#undef F

#define F(x,y,z) (x ^ y ^ z)
#define K 0xCA62C1D6

    P( A, B, C, D, E, R(60) );
    P( E, A, B, C, D, R(61) );
    P( D, E, A, B, C, R(62) );
    P( C, D, E, A, B, R(63) );
    P( B, C, D, E, A, R(64) );
    P( A, B, C, D, E, R(65) );
    P( E, A, B, C, D, R(66) );
    P( D, E, A, B, C, R(67) );
    P( C, D, E, A, B, R(68) );
    P( B, C, D, E, A, R(69) );
    P( A, B, C, D, E, R(70) );
    P( E, A, B, C, D, R(71) );
    P( D, E, A, B, C, R(72) );
    P( C, D, E, A, B, R(73) );
    P( B, C, D, E, A, R(74) );
    P( A, B, C, D, E, R(75) );
    P( E, A, B, C, D, R(76) );
    P( D, E, A, B, C, R(77) );
    P( C, D, E, A, B, R(78) );
    P( B, C, D, E, A, R(79) );

#undef K
#undef F

    ctx->state[0] += A;
    ctx->state[1] += B;
    ctx->state[2] += C;
    ctx->state[3] += D;
    ctx->state[4] += E;
}

/**
 * Description:
 *  Function will update ctx->total[]
 * Parameters:
 *  ctx : [IN] SHA1_CTX
 *        [OUT] SHA1_CTX->total[]
 *  input : [IN] characters that updates SHA1
 *  length : [IN] lenght of input
 * Return:
 *  No.
 */
void __VSSHA1Update( SHA1_CTX *ctx, unsigned char *input, VULONG length )
{
    VULONG left, fill;

    if( ! length ) return;

    left = ctx->total[0] & 0x3F;
    fill = 64 - left;

    ctx->total[0] += length;
    ctx->total[0] &= 0xFFFFFFFF;

    if( ctx->total[0] < length )
        ctx->total[1]++;

    if( left && length >= fill )
    {
        MEMCPY( (void *) (ctx->buffer + left),
                (void *) input, fill );
        sha1_process( ctx, ctx->buffer );
        length -= fill;
        input  += fill;
        left = 0;
    }

    while( length >= 64 )
    {
        sha1_process( ctx, input );
        length -= 64;
        input  += 64;
    }

    if( length )
    {
        MEMCPY( (void *) (ctx->buffer + left),
                (void *) input, length );
    }
}

/**
 * Description:
 *  Function will summarise SHA1 and store into SHA1_CTX->digest[20]
 * Parameters:
 *  cts : [IN] SHA1_CTX
 * Return:
 *  No.
 */
void __VSSHA1Finish( SHA1_CTX *ctx)
{
    VULONG last, padn;
    VULONG high, low;
    unsigned char msglen[8];

    high = ( ctx->total[0] >> 29 )
         | ( ctx->total[1] <<  3 );
    low  = ( ctx->total[0] <<  3 );

    PUT_VULONG( high, msglen, 0 );
    PUT_VULONG( low,  msglen, 4 );

    last = ctx->total[0] & 0x3F;
    padn = ( last < 56 ) ? ( 56 - last ) : ( 120 - last );

    __VSSHA1Update( ctx, sha1_padding, padn );
    __VSSHA1Update( ctx, msglen, 8 );

    PUT_VULONG( ctx->state[0], ctx->digest,  0 );
    PUT_VULONG( ctx->state[1], ctx->digest,  4 );
    PUT_VULONG( ctx->state[2], ctx->digest,  8 );
    PUT_VULONG( ctx->state[3], ctx->digest, 12 );
    PUT_VULONG( ctx->state[4], ctx->digest, 16 );
}

void __VSSHA256Init( SHA256_CTX *ctx )
{
	ctx->total[0] = 0;
	ctx->total[1] = 0;

	ctx->state[0] = 0x6A09E667;
	ctx->state[1] = 0xBB67AE85;
	ctx->state[2] = 0x3C6EF372;
	ctx->state[3] = 0xA54FF53A;
	ctx->state[4] = 0x510E527F;
	ctx->state[5] = 0x9B05688C;
	ctx->state[6] = 0x1F83D9AB;
	ctx->state[7] = 0x5BE0CD19;
	MEMSET(ctx->digest, 0, sizeof(ctx->digest));
	MEMSET(ctx->buffer, 0, sizeof(ctx->buffer));
}

void sha256_process( SHA256_CTX *ctx, unsigned char data[64] )
{
	VULONG temp1, temp2, W[64];
	VULONG A, B, C, D, E, F, G, H;

	GET_VULONG( W[0],  data,  0 );
	GET_VULONG( W[1],  data,  4 );
	GET_VULONG( W[2],  data,  8 );
	GET_VULONG( W[3],  data, 12 );
	GET_VULONG( W[4],  data, 16 );
	GET_VULONG( W[5],  data, 20 );
	GET_VULONG( W[6],  data, 24 );
	GET_VULONG( W[7],  data, 28 );
	GET_VULONG( W[8],  data, 32 );
	GET_VULONG( W[9],  data, 36 );
	GET_VULONG( W[10], data, 40 );
	GET_VULONG( W[11], data, 44 );
	GET_VULONG( W[12], data, 48 );
	GET_VULONG( W[13], data, 52 );
	GET_VULONG( W[14], data, 56 );
	GET_VULONG( W[15], data, 60 );

#define  SHR(x,n) ((x & 0xFFFFFFFF) >> n)
#define ROTR(x,n) (SHR(x,n) | (x << (32 - n)))

#define S0(x) (ROTR(x, 7) ^ ROTR(x,18) ^  SHR(x, 3))
#define S1(x) (ROTR(x,17) ^ ROTR(x,19) ^  SHR(x,10))

#define S2(x) (ROTR(x, 2) ^ ROTR(x,13) ^ ROTR(x,22))
#define S3(x) (ROTR(x, 6) ^ ROTR(x,11) ^ ROTR(x,25))

#define F0(x,y,z) ((x & y) | (z & (x | y)))
#define F1(x,y,z) (z ^ (x & (y ^ z)))

#define R1(t)                                    \
	(                                               \
	W[t] = S1(W[t -  2]) + W[t -  7] +          \
	S0(W[t - 15]) + W[t - 16]            \
	)

#define P1(a,b,c,d,e,f,g,h,x,K)                  \
	{                                               \
	temp1 = h + S3(e) + F1(e,f,g) + K + x;      \
	temp2 = S2(a) + F0(a,b,c);                  \
	d += temp1; h = temp1 + temp2;              \
	}

	A = ctx->state[0];
	B = ctx->state[1];
	C = ctx->state[2];
	D = ctx->state[3];
	E = ctx->state[4];
	F = ctx->state[5];
	G = ctx->state[6];
	H = ctx->state[7];

	P1( A, B, C, D, E, F, G, H, W[ 0], 0x428A2F98 );
	P1( H, A, B, C, D, E, F, G, W[ 1], 0x71374491 );
	P1( G, H, A, B, C, D, E, F, W[ 2], 0xB5C0FBCF );
	P1( F, G, H, A, B, C, D, E, W[ 3], 0xE9B5DBA5 );
	P1( E, F, G, H, A, B, C, D, W[ 4], 0x3956C25B );
	P1( D, E, F, G, H, A, B, C, W[ 5], 0x59F111F1 );
	P1( C, D, E, F, G, H, A, B, W[ 6], 0x923F82A4 );
	P1( B, C, D, E, F, G, H, A, W[ 7], 0xAB1C5ED5 );
	P1( A, B, C, D, E, F, G, H, W[ 8], 0xD807AA98 );
	P1( H, A, B, C, D, E, F, G, W[ 9], 0x12835B01 );
	P1( G, H, A, B, C, D, E, F, W[10], 0x243185BE );
	P1( F, G, H, A, B, C, D, E, W[11], 0x550C7DC3 );
	P1( E, F, G, H, A, B, C, D, W[12], 0x72BE5D74 );
	P1( D, E, F, G, H, A, B, C, W[13], 0x80DEB1FE );
	P1( C, D, E, F, G, H, A, B, W[14], 0x9BDC06A7 );
	P1( B, C, D, E, F, G, H, A, W[15], 0xC19BF174 );
	P1( A, B, C, D, E, F, G, H, R1(16), 0xE49B69C1 );
	P1( H, A, B, C, D, E, F, G, R1(17), 0xEFBE4786 );
	P1( G, H, A, B, C, D, E, F, R1(18), 0x0FC19DC6 );
	P1( F, G, H, A, B, C, D, E, R1(19), 0x240CA1CC );
	P1( E, F, G, H, A, B, C, D, R1(20), 0x2DE92C6F );
	P1( D, E, F, G, H, A, B, C, R1(21), 0x4A7484AA );
	P1( C, D, E, F, G, H, A, B, R1(22), 0x5CB0A9DC );
	P1( B, C, D, E, F, G, H, A, R1(23), 0x76F988DA );
	P1( A, B, C, D, E, F, G, H, R1(24), 0x983E5152 );
	P1( H, A, B, C, D, E, F, G, R1(25), 0xA831C66D );
	P1( G, H, A, B, C, D, E, F, R1(26), 0xB00327C8 );
	P1( F, G, H, A, B, C, D, E, R1(27), 0xBF597FC7 );
	P1( E, F, G, H, A, B, C, D, R1(28), 0xC6E00BF3 );
	P1( D, E, F, G, H, A, B, C, R1(29), 0xD5A79147 );
	P1( C, D, E, F, G, H, A, B, R1(30), 0x06CA6351 );
	P1( B, C, D, E, F, G, H, A, R1(31), 0x14292967 );
	P1( A, B, C, D, E, F, G, H, R1(32), 0x27B70A85 );
	P1( H, A, B, C, D, E, F, G, R1(33), 0x2E1B2138 );
	P1( G, H, A, B, C, D, E, F, R1(34), 0x4D2C6DFC );
	P1( F, G, H, A, B, C, D, E, R1(35), 0x53380D13 );
	P1( E, F, G, H, A, B, C, D, R1(36), 0x650A7354 );
	P1( D, E, F, G, H, A, B, C, R1(37), 0x766A0ABB );
	P1( C, D, E, F, G, H, A, B, R1(38), 0x81C2C92E );
	P1( B, C, D, E, F, G, H, A, R1(39), 0x92722C85 );
	P1( A, B, C, D, E, F, G, H, R1(40), 0xA2BFE8A1 );
	P1( H, A, B, C, D, E, F, G, R1(41), 0xA81A664B );
	P1( G, H, A, B, C, D, E, F, R1(42), 0xC24B8B70 );
	P1( F, G, H, A, B, C, D, E, R1(43), 0xC76C51A3 );
	P1( E, F, G, H, A, B, C, D, R1(44), 0xD192E819 );
	P1( D, E, F, G, H, A, B, C, R1(45), 0xD6990624 );
	P1( C, D, E, F, G, H, A, B, R1(46), 0xF40E3585 );
	P1( B, C, D, E, F, G, H, A, R1(47), 0x106AA070 );
	P1( A, B, C, D, E, F, G, H, R1(48), 0x19A4C116 );
	P1( H, A, B, C, D, E, F, G, R1(49), 0x1E376C08 );
	P1( G, H, A, B, C, D, E, F, R1(50), 0x2748774C );
	P1( F, G, H, A, B, C, D, E, R1(51), 0x34B0BCB5 );
	P1( E, F, G, H, A, B, C, D, R1(52), 0x391C0CB3 );
	P1( D, E, F, G, H, A, B, C, R1(53), 0x4ED8AA4A );
	P1( C, D, E, F, G, H, A, B, R1(54), 0x5B9CCA4F );
	P1( B, C, D, E, F, G, H, A, R1(55), 0x682E6FF3 );
	P1( A, B, C, D, E, F, G, H, R1(56), 0x748F82EE );
	P1( H, A, B, C, D, E, F, G, R1(57), 0x78A5636F );
	P1( G, H, A, B, C, D, E, F, R1(58), 0x84C87814 );
	P1( F, G, H, A, B, C, D, E, R1(59), 0x8CC70208 );
	P1( E, F, G, H, A, B, C, D, R1(60), 0x90BEFFFA );
	P1( D, E, F, G, H, A, B, C, R1(61), 0xA4506CEB );
	P1( C, D, E, F, G, H, A, B, R1(62), 0xBEF9A3F7 );
	P1( B, C, D, E, F, G, H, A, R1(63), 0xC67178F2 );

	ctx->state[0] += A;
	ctx->state[1] += B;
	ctx->state[2] += C;
	ctx->state[3] += D;
	ctx->state[4] += E;
	ctx->state[5] += F;
	ctx->state[6] += G;
	ctx->state[7] += H;
}

void __VSSHA256Update( SHA256_CTX * ctx, unsigned char *input, VULONG length )
{
	VULONG left, fill;

	if( ! length ) return;

	left = ctx->total[0] & 0x3F;
	fill = 64 - left;

	ctx->total[0] += length;
	ctx->total[0] &= 0xFFFFFFFF;

	if( ctx->total[0] < length )
		ctx->total[1]++;

	if( left && length >= fill )
	{
		MEMCPY( (void *) (ctx->buffer + left),
			(void *) input, fill );
		sha256_process( ctx, ctx->buffer );
		length -= fill;
		input  += fill;
		left = 0;
	}

	while( length >= 64 )
	{
		sha256_process( ctx, input );
		length -= 64;
		input  += 64;
	}

	if( length )
	{
		MEMCPY( (void *) (ctx->buffer + left),
			(void *) input, length );
	}
}

static unsigned char sha256_padding[64] =
{
	0x80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
};

void __VSSHA256Finish( SHA256_CTX *ctx )
{
	VULONG last, padn;
	VULONG high, low;
	unsigned char msglen[8];

	high = ( ctx->total[0] >> 29 )
		| ( ctx->total[1] <<  3 );
	low  = ( ctx->total[0] <<  3 );

	PUT_VULONG( high, msglen, 0 );
	PUT_VULONG( low,  msglen, 4 );

	last = ctx->total[0] & 0x3F;
	padn = ( last < 56 ) ? ( 56 - last ) : ( 120 - last );

	__VSSHA256Update( ctx, sha256_padding, padn );
	__VSSHA256Update( ctx, msglen, 8 );

	PUT_VULONG( ctx->state[0], ctx->digest,  0 );
	PUT_VULONG( ctx->state[1], ctx->digest,  4 );
	PUT_VULONG( ctx->state[2], ctx->digest,  8 );
	PUT_VULONG( ctx->state[3], ctx->digest, 12 );
	PUT_VULONG( ctx->state[4], ctx->digest, 16 );
	PUT_VULONG( ctx->state[5], ctx->digest, 20 );
	PUT_VULONG( ctx->state[6], ctx->digest, 24 );
	PUT_VULONG( ctx->state[7], ctx->digest, 28 );
}

void __VSSHA512Init( SHA512_CTX *ctx )
{
	ctx->total[0] = 0;
	ctx->total[1] = 0;

	ctx->state[0] = 0x6A09E667F3BCC908;
	ctx->state[1] = 0xBB67AE8584CAA73B;
	ctx->state[2] = 0x3C6EF372FE94F82B;
	ctx->state[3] = 0xA54FF53A5F1D36F1;
	ctx->state[4] = 0x510E527FADE682D1;
	ctx->state[5] = 0x9B05688C2B3E6C1F;
	ctx->state[6] = 0x1F83D9ABFB41BD6B;
	ctx->state[7] = 0x5BE0CD19137E2179;
	MEMSET(ctx->digest, 0, sizeof(ctx->digest));
	MEMSET(ctx->buffer, 0, sizeof(ctx->buffer));
}

static void sha512_process( SHA512_CTX *ctx, const unsigned char data[128] )
{
	int i;
	unsigned long long temp1, temp2, W[80];
	unsigned long long A, B, C, D, E, F, G, H;

#define  SHR512(x,n) (x >> n)
#define ROTR512(x,n) (SHR512(x,n) | (x << (64 - n)))

#define S0512(x) (ROTR512(x, 1) ^ ROTR512(x, 8) ^  SHR512(x, 7))
#define S1512(x) (ROTR512(x,19) ^ ROTR512(x,61) ^  SHR512(x, 6))

#define S2512(x) (ROTR512(x,28) ^ ROTR512(x,34) ^ ROTR512(x,39))
#define S3512(x) (ROTR512(x,14) ^ ROTR512(x,18) ^ ROTR512(x,41))

#define F0(x,y,z) ((x & y) | (z & (x | y)))
#define F1(x,y,z) (z ^ (x & (y ^ z)))

#define P512(a,b,c,d,e,f,g,h,x,K)                  \
	{                                               \
	temp1 = h + S3512(e) + F1(e,f,g) + K + x;      \
	temp2 = S2512(a) + F0(a,b,c);                  \
	d += temp1; h = temp1 + temp2;              \
	}

	for( i = 0; i < 16; i++ )
	{
		GET_VULONGLONG( W[i], data, i << 3 );
	}

	for( ; i < 80; i++ )
	{
		W[i] = S1512(W[i -  2]) + W[i -  7] +
			S0512(W[i - 15]) + W[i - 16];
	}

	A = ctx->state[0];
	B = ctx->state[1];
	C = ctx->state[2];
	D = ctx->state[3];
	E = ctx->state[4];
	F = ctx->state[5];
	G = ctx->state[6];
	H = ctx->state[7];
	i = 0;

	do
	{
		P512( A, B, C, D, E, F, G, H, W[i], K[i] ); i++;
		P512( H, A, B, C, D, E, F, G, W[i], K[i] ); i++;
		P512( G, H, A, B, C, D, E, F, W[i], K[i] ); i++;
		P512( F, G, H, A, B, C, D, E, W[i], K[i] ); i++;
		P512( E, F, G, H, A, B, C, D, W[i], K[i] ); i++;
		P512( D, E, F, G, H, A, B, C, W[i], K[i] ); i++;
		P512( C, D, E, F, G, H, A, B, W[i], K[i] ); i++;
		P512( B, C, D, E, F, G, H, A, W[i], K[i] ); i++;
	}
	while( i < 80 );

	ctx->state[0] += A;
	ctx->state[1] += B;
	ctx->state[2] += C;
	ctx->state[3] += D;
	ctx->state[4] += E;
	ctx->state[5] += F;
	ctx->state[6] += G;
	ctx->state[7] += H;
}

void __VSSHA512Update( SHA512_CTX * ctx, unsigned char *input, VULONGLONG length )
{
	VULONGLONG fill;
	unsigned int left;

	if( length <= 0 )
		return;

	left = (unsigned int) (ctx->total[0] & 0x7F);
	fill = 128 - left;

	ctx->total[0] += (unsigned long long) length;

	if( ctx->total[0] < (unsigned long long) length )
		ctx->total[1]++;

	if( left && length >= fill )
	{
		MEMCPY( (void *) (ctx->buffer + left),
			(void *) input, fill );
		sha512_process( ctx, ctx->buffer );
		input += fill;
		length  -= fill;
		left = 0;
	}

	while( length >= 128 )
	{
		sha512_process( ctx, input );
		input += 128;
		length  -= 128;
	}

	if( length > 0 )
	{
		MEMCPY( (void *) (ctx->buffer + left),
			(void *) input, length );
	}
}

static const unsigned char sha512_padding[128] =
{
	0x80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
};

void __VSSHA512Finish( SHA512_CTX *ctx )
{
	VULONGLONG last, padn;
	unsigned long long high, low;
	unsigned char msglen[16];

	high = ( ctx->total[0] >> 61 )
		| ( ctx->total[1] <<  3 );
	low  = ( ctx->total[0] <<  3 );

	PUT_VULONGLONG( high, msglen, 0 );
	PUT_VULONGLONG( low,  msglen, 8 );

	last = (VULONGLONG)( ctx->total[0] & 0x7F );
	padn = ( last < 112 ) ? ( 112 - last ) : ( 240 - last );

	__VSSHA512Update( ctx, (unsigned char *) sha512_padding, padn );
	__VSSHA512Update( ctx, msglen, 16 );

	PUT_VULONGLONG( ctx->state[0], ctx->digest,  0 );
	PUT_VULONGLONG( ctx->state[1], ctx->digest,  8 );
	PUT_VULONGLONG( ctx->state[2], ctx->digest, 16 );
	PUT_VULONGLONG( ctx->state[3], ctx->digest, 24 );
	PUT_VULONGLONG( ctx->state[4], ctx->digest, 32 );
	PUT_VULONGLONG( ctx->state[5], ctx->digest, 40 );
	PUT_VULONGLONG( ctx->state[6], ctx->digest, 48 );
	PUT_VULONGLONG( ctx->state[7], ctx->digest, 56 );
}
