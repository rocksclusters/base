# $Id: Makefile,v 1.1 2011/06/08 00:51:33 anoop Exp $

# @Copyright@
# @Copyright@

# $ Log: $

REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../devel/devel
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

PLUGIN_DIR = /opt/rocks/var/plugins/sec_attr

build:

install:: build
	mkdir -p $(ROOT)/$(PLUGIN_DIR)
	$(INSTALL) -m400 plugins/*.py $(ROOT)/$(PLUGIN_DIR)

clean::
