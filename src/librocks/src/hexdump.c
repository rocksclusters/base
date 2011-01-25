/*
 * $Id: hexdump.c,v 1.2 2011/01/25 21:16:28 mjk Exp $
 *
 * @Copyright@
 * @Copyright@
 *
 * $Log: hexdump.c,v $
 * Revision 1.2  2011/01/25 21:16:28  mjk
 * - Removed channel.x
 * - Off by one on hexdump buffer size
 *
 * Revision 1.1  2010/10/19 23:06:29  mjk
 * c is hard
 *
 * Revision 1.1  2010/10/18 17:24:37  mjk
 * *** empty log message ***
 *
 */

#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>
#include "../include/hexdump.h"

void
HexDump(const char *label, const char *msg, int len)
{
	HexDumpToFile(stdout, label, msg, len);
} /* HexDump */


void
HexDumpToFile(FILE *fout, const char *label, const char *msg, int len)
{
	char *s;

	s = HexDumpToString(label, msg, len);
	if ( s ) {
		fprintf(fout, "%s\n", s);
		free(s);
	}
} /* HexDumpToFile */


/*
 *           1         2         3         4         5         6         7
 * 01234567890123456789012345678901234567890123456789012345678901234567890
 *
 * 20 20 20 20 20 20 20 20 - 20 20 20 20 20 20 20 20  ................
 *
 */

#define HEX_LINE_LENGTH 66
#define HEX_CHARS	16
#define HEX_ASCII_START	51

/*
          1         2         3         4         5         6         7
01234567890123456789012345678901234567890123456789012345678901234567890123
LABEL: 30 31 32 33 34 35 36 37 - 38 39 20 41 42 43 44 45  0123456789 ABCDE
*/

char *
HexDumpToString(const char *label, const char *msg, int len)
{
	int	i, j, line_len;
	char	*buffer;
	int	buffer_len;
	char	*p; /* current hex   position */
	char	*q; /* current ascii position */

	assert(msg);
	assert(len);

	line_len = HEX_LINE_LENGTH;
	if ( label ) {
		line_len += strlen(label) + strlen(": ");
	}

	buffer_len = (len + HEX_CHARS - 1) / HEX_CHARS * line_len + 1;
	buffer = malloc(buffer_len);
	if ( !buffer ) {
		return NULL;
	}
	memset(buffer, (int)' ', buffer_len);

	p = buffer;
	for (i=0; i<len; i+=16, p+= 17) {
		if ( i > 0 ) {
			*p++ = '\n';
		}
		if ( label ) {
			p += sprintf(p, "%s: ", label);
		}
	  	q = p + HEX_ASCII_START;
        
		for (j=0; j<16 && (j+i) < len; j++) {
			unsigned char	byte = msg[i+j];

			if ( j == 8 ) { 
				p += sprintf(p, "- ");
			}
      
			p += sprintf(p, "%02x ", byte);
      
			if ( isprint(byte) ) {
				*q++ = byte;
			}
			else {
				*q++ = '.';
			}
		}

		*p = ' ';
	}
	*q = '\0';

	return buffer;
}




