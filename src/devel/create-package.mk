# $Id: create-package.mk,v 1.2 2008/08/20 22:12:02 mjk Exp $
#
# This makefile is used by the "rocks create package" command to turn any
# directory into an RPM copied into the contrib area.
#
# @Copyright@
# @Copyright@
#
# $Log: create-package.mk,v $
# Revision 1.2  2008/08/20 22:12:02  mjk
# works
#
# Revision 1.1  2008/08/19 18:51:12  mjk
# rocks create package stuff
#

PKGROOT         = /opt/rocks
REDHAT.ROOT     = $(CURDIR)
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build:

install::
	mkdir -p $(ROOT)/$(PREFIX)
	cp -a $(SOURCE_DIRECTORY) $(ROOT)/$(PREFIX)/

dir2pkg:
	$(MAKE) pkg
	mv $(REDHAT.ROOT)/RPMS/$(ARCH)/* $(DEST_DIRECTORY)
