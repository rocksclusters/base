# $Id: Makefile,v 1.1 2011/04/11 22:41:50 anoop Exp $

# @Copyright@
# @Copyright@

# $Log: Makefile,v $
# Revision 1.1  2011/04/11 22:41:50  anoop
# RPC service that initiates transfer of shared 411 key
#

PKGROOT	=	/opt/rocks
REDHAT.ROOT =	$(CURDIR)/../../../
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

sec_channel_svc.c : sec_channel.x
	rpcgen -M -N $<

sec_channel_server: sec_channel_svc.c sec_channel_server.c
	$(CC) $(CFLAGS) -c $^
	$(CC) $(CFLAGS) -o $@ $(^:%c=%o)

build: sec_channel_server

install::
	mkdir -p $(ROOT)/$(PKGROOT)/sbin
	mkdir -p $(ROOT)/$(INIT_SCRIPTS_DIR)
	$(INSTALL) -m0500 sec_channel_server $(ROOT)/$(PKGROOT)/sbin
	$(INSTALL) -m0500 sec-channel.init $(ROOT)/$(INIT_SCRIPTS_DIR)/sec-channel

clean::
	rm -rf sec_channel_svc.c sec_channel_server	\
	sec_channel.h *.o sec_channel_clnt.c
