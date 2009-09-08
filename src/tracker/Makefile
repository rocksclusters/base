#
# $Id: Makefile,v 1.1 2009/09/08 22:17:49 bruno Exp $
#
# @COPYRIGHT@
# @COPYRIGHT@
#
# $Log: Makefile,v $
# Revision 1.1  2009/09/08 22:17:49  bruno
# start of the new tracker
#
#

REDHAT.ROOT     = $(CURDIR)/../../

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

#INCLUDE	= -I/usr/include/apr-1
#LIBS	= -L/opt/rocks/lib -lcurl
#LIBS	= -lcurl
#EXTRA	= -DDEBUG

build:	client server

client:		client.c lib.c
	cc $(INCLUDE) $(EXTRA) -o client client.c lib.c $(LIBS)

server:		server.c
	cc $(INCLUDE) $(EXTRA) -o server server.c lib.c $(LIBS)

hashit:		hashit.c
	cc $(INCLUDE) $(EXTRA) -o hashit hashit.c lib.c $(LIBS)

install::
	mkdir -p $(ROOT)/$(PKGROOT)/tracker
	cp client $(ROOT)/$(PKGROOT)/tracker

clean::
	rm -f $(NAME).spec.in
	rm -f client server hashit

