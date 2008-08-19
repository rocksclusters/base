# $Id: create-package.mk,v 1.1 2008/08/19 18:51:12 mjk Exp $
#
# This makefile is used by the "rocks create package" command to turn any
# directory into an RPM copied into the contrib area.
#
# @Copyright@
# @Copyright@
#
# $Log: create-package.mk,v $
# Revision 1.1  2008/08/19 18:51:12  mjk
# rocks create package stuff
#

NAME    = $(PACKAGE_NAME)
VERSION = $(PACKAGE_VERSION)
RELEASE = $(PACKAGE_RELEASE)

PKGROOT         = /opt/rocks
REDHAT.ROOT     = $(CURDIR)
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build:

install::
	mkdir -p $(ROOT)/$(PACKAGE_PREFIX)
	cp -a $(PACKAGE_DIRECTORY) $(ROOT)/$(PACKAGE_PREFIX)/

dir2pkg:
	$(MAKE) pkg
	cp $(REDHAT.ROOT)/RPMS/$(ARCH)/* \
		/home/install/contrib/$(ROCKS_VERSION)/$(ARCH)/RPMS/
