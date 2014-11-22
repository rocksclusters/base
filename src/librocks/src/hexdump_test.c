/* $Id: hexdump_test.c,v 1.4 2012/11/27 00:48:39 phil Exp $
 *
 * @Copyright@
 * 
 * 				Rocks(r)
 * 		         www.rocksclusters.org
 * 		         version 6.2 (SideWinder)
 * 
 * Copyright (c) 2000 - 2014 The Regents of the University of California.
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
 * 	Cluster Group at the San Diego Supercomputer Center at the
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
 * $Log: hexdump_test.c,v $
 * Revision 1.4  2012/11/27 00:48:39  phil
 * Copyright Storm for Emerald Boa
 *
 * Revision 1.3  2012/05/06 05:48:45  phil
 * Copyright Storm for Mamba
 *
 * Revision 1.2  2011/07/23 02:30:48  phil
 * Viper Copyright
 *
 * Revision 1.1  2010/10/19 23:06:29  mjk
 * c is hard
 *
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <assert.h>
#include "../include/hexdump.h"


int
main(int argc, char *argv[])
{
	FILE	*fin;
	size_t	len = 128;
	char	*line = (char *)malloc(len);
	int	n;

	printf("-- TEST 1 --\n");
	HexDump("LABEL", "0123456789ABCDEF", 16);

	printf("-- TEST 2 --\n");
	HexDump("LABEL", "0123456789 ABCDEF", 17);

	printf("-- TEST 3 --\n");

	fin = fopen("hexdump_test.c", "r");
	assert(fin);

	while ( (n = getline(&line, &len, fin)) != -1) {
		HexDump("hexdump_test.c", line, n);
	}

	if ( line ) {
		free(line);
	}

	fclose(fin);
	return 0;
} /* main */
