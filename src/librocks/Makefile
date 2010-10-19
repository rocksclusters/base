# $Id: Makefile,v 1.1 2010/10/19 01:00:10 mjk Exp $
#
# @Copyright@
# @Copyright@
#
# $Log: Makefile,v $
# Revision 1.1  2010/10/19 01:00:10  mjk
# *** empty log message ***
#

PKGROOT		= /opt/rocks
REDHAT.ROOT	= $(CURDIR)/../../
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build:
	$(MAKE) -C src

install:: build
	mkdir -p $(ROOT)/$(PKGROOT)/include
	mkdir -p $(ROOT)/$(PKGROOT)/lib
	install -m444 include/*.h $(ROOT)/$(PKGROOT)/include/
	install -m444 lib/*.so $(ROOT)/$(PKGROOT/lib/

clean::
	$(MAKE) -C src clean

