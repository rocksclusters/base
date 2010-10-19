/* $Id: hexdump.h,v 1.1 2010/10/19 23:06:29 mjk Exp $
 *
 * @Copyright@
 * @Copyright@
 *
 * $Log: hexdump.h,v $
 * Revision 1.1  2010/10/19 23:06:29  mjk
 * c is hard
 *
 */
 
#ifndef _ROCKS_HEXDUMP_H_
#define _ROCKS_HEXDUMP_H_
 
#ifdef __cplusplus
extern "C" {
#endif

	void  HexDump(const char *label, const char *msg, int len);
	void  HexDumpToFile(FILE *fout, const char *label, const char *msg, int len);
	char *HexDumpToString(const char *label, const char *msg, int len);

#ifdef __cplusplus
}
#endif


 
#endif /* __ROCKS_HEXDUMP_H__ */
