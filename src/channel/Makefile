# $Id: Makefile,v 1.2 2010/10/20 21:12:34 mjk Exp $
#
# @Copyright@
# @Copyright@
#
# $Log: Makefile,v $
# Revision 1.2  2010/10/20 21:12:34  mjk
# works
#
# Revision 1.1  2010/10/19 23:06:29  mjk
# c is hard
#


PKGROOT		= /opt/rocks
REDHAT.ROOT	= $(CURDIR)/../../
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

CFLAGS = -Wall -g 
CPPFLAGS = -I /opt/rocks/include -iquote /opt/rocks/include/rocks
LDFLAGS = -L /opt/rocks/lib 

channel.x:
	cp $(PKGROOT)/include/rocks/$@ .

channel_svc.c: channel.x
	rpcgen -m -N -o $@ $^

channeld: server.o channel_svc.o
	$(CC) $(CFLAGS) $(LDFLAGS) -lrocks -o $@ $^

411-alert: 411-alert.o
	$(CC) $(CFLAGS) $(LDFLAGS) -lrocks -o $@ $^


build: channeld 411-alert 411-alert-handler

install:: build
	mkdir -p $(ROOT)/$(PKGROOT)/sbin
	install -m544 411-alert $(ROOT)/$(PKGROOT)/sbin/
	install -m544 411-alert-handler $(ROOT)/$(PKGROOT)/sbin/
	install -m544 channeld  $(ROOT)/$(PKGROOT)/sbin/

clean::
	-rm *.o
	-rm channeld 411-alert 411-alert-handler
	-rm channel_svc.c channel.x




