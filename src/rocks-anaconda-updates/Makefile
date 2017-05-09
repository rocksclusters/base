REDHAT.ROOT     = $(CURDIR)/../../

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build:	
	echo "no build required"

install::
	mkdir -p $(ROOT)/RedHat/base
	install -ma+r comps.xml $(ROOT)/$(PKGROOT)

