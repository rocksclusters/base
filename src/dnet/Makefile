# $Id: Makefile,v 1.1 2009/05/15 00:36:17 anoop Exp $

# @Copyright@
# @Copyright@

# $Log: Makefile,v $
# Revision 1.1  2009/05/15 00:36:17  anoop
# Added libdnet. Necessary for greceptor to work correctly on solaris
#

REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../../../../..
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build:
	gunzip -c $(NAME)-$(VERSION).tar.gz | $(TAR) -xf -
	(					\
		cd $(NAME)-$(VERSION);		\
		./configure --prefix=$(PKGROOT);\
		$(MAKE);			\
	)

install::
	mkdir -p $(ROOT)/$(PKGROOT)
	(					\
		cd $(NAME)-$(VERSION);		\
		$(MAKE) prefix=$(ROOT)/$(PKGROOT) install;\
	)

clean::
	rm -rf $(NAME)-$(VERSION)
