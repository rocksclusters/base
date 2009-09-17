#
# $Id: Makefile,v 1.3 2009/09/17 20:12:49 bruno Exp $
#
# @COPYRIGHT@
# @COPYRIGHT@
#
# $Log: Makefile,v $
# Revision 1.3  2009/09/17 20:12:49  bruno
# lots of good stuff:
#  - expandable, circular hash table
#  - clients randomly shuffle their peer list
#  - skip to next peer if download of peer fails
#
# Revision 1.2  2009/09/15 21:52:13  bruno
# closer
#
# Revision 1.1  2009/09/08 22:17:49  bruno
# start of the new tracker
#
#

REDHAT.ROOT     = $(CURDIR)/../../

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

INCLUDE	= -I/usr/include/apr-1
#LIBS	= -L/opt/rocks/lib -lcurl
LIBS	= -lcurl
EXTRA	= -Wall
#EXTRA	= -Wall -DDEBUG

build:	tracker-client.cgi server

tracker-client.cgi:	tracker-client.c client.c lib.c
	cc $(INCLUDE) $(EXTRA) -o tracker-client.cgi tracker-client.c \
		client.c lib.c $(LIBS)

server:		server.c
	cc $(INCLUDE) $(EXTRA) -o server server.c lib.c $(LIBS)

hashit:		hashit.c
	cc $(INCLUDE) $(EXTRA) -o hashit hashit.c lib.c $(LIBS)

install::
	mkdir -p $(ROOT)/$(PKGROOT)/tracker
	cp tracker-client.cgi $(ROOT)/$(PKGROOT)/tracker

clean::
	rm -f $(NAME).spec.in
	rm -f tracker-client.cgi server hashit

