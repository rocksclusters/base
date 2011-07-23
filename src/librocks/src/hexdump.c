/*
 * $Id: hexdump.c,v 1.3 2011/07/23 02:30:48 phil Exp $
 *
 * @Copyright@
 * 
 * 				Rocks(r)
 * 		         www.rocksclusters.org
 * 		         version 5.4.3 (Viper)
 * 
 * Copyright (c) 2000 - 2011 The Regents of the University of California.
 * All rights reserved.	
 * 
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met:
 * 
 * 1. Redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer.
 * 
 * 2. Redistributions in binary form must reproduce the above copyright
 * notice unmodified and in its entirety, this list of conditions and the
 * following disclaimer in the documentation and/or other materials provided 
 * with the distribution.
 * 
 * 3. All advertising and press materials, printed or electronic, mentioning
 * features or use of this software must display the following acknowledgement: 
 * 
 * 	"This product includes software developed by the Rocks(r)
 * 	Development Team at the San Diego Supercomputer Center at the
 * 	University of California, San Diego and its contributors."
 * 
 * 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
 * neither the name or logo of this software nor the names of its
 * authors may be used to endorse or promote products derived from this
 * software without specific prior written permission.  The name of the
 * software includes the following terms, and any derivatives thereof:
 * "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
 * the associated name, interested parties should contact Technology 
 * Transfer & Intellectual Property Services, University of California, 
 * San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
 * Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
 * 
 * THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
 * BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
 * OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
 * IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 * 
 * @Copyright@
 *
 * $Log: hexdump.c,v $
 * Revision 1.3  2011/07/23 02:30:48  phil
 * Viper Copyright
 *
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




