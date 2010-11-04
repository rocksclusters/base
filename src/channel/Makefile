# $Id: Makefile,v 1.6 2010/11/04 02:20:15 anoop Exp $
#
# @Copyright@
# @Copyright@
#
# $Log: Makefile,v $
# Revision 1.6  2010/11/04 02:20:15  anoop
# Solaris compatibility fixes
#
# Revision 1.5  2010/10/21 00:21:00  bruno
# name the init script 'channeld'
#
# Revision 1.4  2010/10/20 23:44:46  bruno
# tweak
#
# Revision 1.3  2010/10/20 23:41:04  mjk
# forgot to make this into a service
# needs a solaris version as well
#
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

OS=$(shell ../devel/devel/bin/os)
ARCH=$(shell ../devel/devel/bin/arch)

ifeq ($(OS), linux)
CFLAGS = -Wall -g 
endif

CPPFLAGS = -I/opt/rocks/include
LDFLAGS = -L/opt/rocks/lib -lrocks

ifeq ($(OS), sunos)
LDFLAGS += -lrpcsvc -lnsl
endif

channel.x:
	cp $(PKGROOT)/include/rocks/$@ .

channel_svc.c: channel.x
	rpcgen -h -N -o channel.h $^
	rpcgen -m -N -o $@ $^

channeld: server.o channel_svc.o
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^

411-alert: 411-alert.o
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^


build: channeld 411-alert 411-alert-handler

install:: build
	mkdir -p $(ROOT)/$(PKGROOT)/sbin
	mkdir -p $(ROOT)/$(INIT_SCRIPTS_DIR)
	$(INSTALL) -m544 411-alert $(ROOT)/$(PKGROOT)/sbin/
	$(INSTALL) -m544 411-alert-handler $(ROOT)/$(PKGROOT)/sbin/
	$(INSTALL) -m544 channeld  $(ROOT)/$(PKGROOT)/sbin/
	$(INSTALL) -m755 channel.init $(ROOT)/$(INIT_SCRIPTS_DIR)/channeld

clean::
	-rm *.o
	-rm channeld 411-alert 411-alert-handler
	-rm channel_svc.c channel.x channel.h
