# $Id: Makefile,v 1.6 2011/01/25 21:16:28 mjk Exp $
#
# @Copyright@
# @Copyright@
#
# $Log: Makefile,v $
# Revision 1.6  2011/01/25 21:16:28  mjk
# - Removed channel.x
# - Off by one on hexdump buffer size
#
# Revision 1.5  2011/01/21 20:06:50  anoop
# Build for 64-bit architecture
#
# Revision 1.4  2010/11/04 02:20:41  anoop
# Solaris compatibility fixes
#
# Revision 1.3  2010/10/19 23:06:29  mjk
# c is hard
#
# Revision 1.2  2010/10/19 01:04:01  mjk
# *** empty log message ***
#
# Revision 1.1  2010/10/18 17:24:37  mjk
# *** empty log message ***
#

OS=$(shell ../../devel/devel/bin/os)

CFLAGS = -Wall -g -fPIC

BINS = hexdump_test

ifeq ($(OS), sunos)
BINS =
CFLAGS += -m64
endif

default: librocks.so $(BINS)

OBJS = hexdump.o

librocks.so: $(OBJS)
	$(CC) $(CFLAGS) -shared -o $@ $^

hexdump.o: hexdump.c ../include/hexdump.h

hexdump_test: hexdump_test.o hexdump.o
	$(CC) $(CFLAGS) -o $@ $^

clean:
	-rm *.o
	-rm hexdump_test
