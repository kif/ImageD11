

#ifndef _write_check_h
#define _write_check_h

#define NCALL 8


#define EAXMAX 0

void readcpuid(void);
uint32_t maxcall(void);
int flag_SSE(void);
int flag_SSE2(void);
int flag_SSE3(void);
int flag_FMA3(void);
int flag_SSE41(void);
int flag_SSE42(void);
int flag_MOVBE(void);
int flag_XSAVE(void);
int flag_OSXSAVE(void);
int flag_AVX(void);
int flag_AVX2(void);
int flag_AVX512F(void);
int i_have_SSE2(void);
int i_have_SSE42(void);
int i_have_AVX(void);
int i_have_AVX2(void);
int i_have_AVX512F(void);
#endif
