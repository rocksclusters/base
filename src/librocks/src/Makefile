# $Id: Makefile,v 1.4 2010/11/04 02:20:41 anoop Exp $
#
# @Copyright@
# @Copyright@
#
# $Log: Makefile,v $
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
ARCH=$(shell ../../devel/devel/bin/arch)


CFLAGS = -fPIC

ifeq ($(OS), linux)
CFLAGS += -Wall -g
HEXDUMPTEST = hexdump_test
endif

default: librocks.so $(HEXDUMPTEST)

OBJS = hexdump.o channel_clnt.o channel_xdr.o

hexdump.o: hexdump.c ../include/hexdump.h

hexdump_test: hexdump_test.o hexdump.o
	$(CC) $(CFLAGS) -o $@ $^

channel_clnt.c: channel.x
	rpcgen -N $^

channel_xdr.c: channel.x
	rpcgen -N -c -o $@ $^

librocks.so: $(OBJS)
	$(CC) $(CFLAGS) -shared -o $@ $^
clean:
	-rm *.o *.so
	-rm channel_clnt.c channel_svc.c channel_xdr.c channel.h
	-rm hexdump_test
