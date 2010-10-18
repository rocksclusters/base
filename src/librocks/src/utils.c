/*
 * $Id: utils.c,v 1.1 2010/10/18 17:24:37 mjk Exp $
 *
 * @Copyright@
 * @Copyright@
 *
 * $Log: utils.c,v $
 * Revision 1.1  2010/10/18 17:24:37  mjk
 * *** empty log message ***
 *
 */

#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <assert.h>


void
HexDump(FILE *fout, const char *label, const char *msg, int len)
{
	int	i, j;

	assert(fout);
	assert(msg);

	for (i=0; i<len; i+=16) {
		char	buffer[80];
		char	*p = &buffer[0];
		char	*q = &buffer[52];
    
		memset(buffer, (int)' ', sizeof buffer);
    
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
		*q = '\0';

		if ( !label ) {
			fprintf(fout, "%s", buffer);
		} else {
			fprintf(fout, "%s: %s", label, buffer);
		}

	}
}




