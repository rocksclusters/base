/* $Id: hexdump_test.c,v 1.1 2010/10/19 23:06:29 mjk Exp $
 *
 * @Copyright@
 * @Copyright@
 * 
 * $Log: hexdump_test.c,v $
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
