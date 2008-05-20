# $Id: Makefile,v 1.1 2008/05/20 01:03:08 anoop Exp $

# @Copyright@
# @Copyright@

# $Log: Makefile,v $
# Revision 1.1  2008/05/20 01:03:08  anoop
# Added pcre postfix and php for solaris
#
# Revision 1.1  2008/05/02 00:17:56  anoop
# Added Postfix for solaris. Will be moved to a different roll in
# the future.
#

# DESCRIPTION:
# Solaris-only package


REDHAT.ROOT = $(CURDIR)/../../
ROCKSROOT = ../../../../..
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build:
	gunzip -c $(NAME)-$(VERSION).tar.gz | $(TAR) -xf -
	(\
		cd $(NAME)-$(VERSION);	\
		$(MAKE);		\
	)
install::
	(\
		cd $(NAME)-$(VERSION);	\
		$(MAKE) non-interactive-package install_root=$(ROOT); \
	);
	mkdir -p $(ROOT)/lib/svc/method
	mkdir -p $(ROOT)/var/svc/manifest/network
	$(INSTALL) -m0755 postfix.init $(ROOT)/lib/svc/method/postfix
	$(INSTALL) -m0644 postfix.xml $(ROOT)/var/svc/manifest/network/postfix.xml

clean::
	rm -rf $(NAME)-$(VERSION)
