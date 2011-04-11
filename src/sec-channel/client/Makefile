# $Id: Makefile,v 1.1 2011/04/11 22:41:49 anoop Exp $

# @Copyright@
# @Copyright@

# $Log: Makefile,v $
# Revision 1.1  2011/04/11 22:41:49  anoop
# RPC service that initiates transfer of shared 411 key
#

PKGROOT	=	/opt/rocks
REDHAT.ROOT =	$(CURDIR)/../../../
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

sec_channel_clnt.c : sec_channel.x
	rpcgen -M -N $<

sec_channel_client.c: sec_channel.x
	rpcgen -Sc -M -N -o $@ $<

get-411-key: sec_channel_client.c sec_channel_clnt.c
	$(CC) $(CFLAGS) -c $^
	$(CC) $(CFLAGS) -o $@ $(^:%c=%o)

build: get-411-key

install::
	mkdir -p $(ROOT)/$(PKGROOT)/bin
	$(INSTALL) -m0500 get-411-key $(ROOT)/$(PKGROOT)/bin

clean::
	rm -rf sec_channel_client.c sec_channel_clnt.c get-411-key \
	sec_channel_svc.c sec_channel.h *.o
