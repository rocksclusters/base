# $Id: Makefile,v 1.2 2010/06/22 21:26:24 mjk Exp $
#
# @COPYRIGHT@
# @COPYRIGHT@
#
# $Log: Makefile,v $
# Revision 1.2  2010/06/22 21:26:24  mjk
# Build env is now from src/devel package, nothing outside of base roll.
#
# Revision 1.1  2008/05/20 01:03:07  anoop
# Added pcre postfix and php for solaris
#
# Revision 1.1  2008/05/02 00:27:29  anoop
# Added perl command reg-exp on which lighttpd is dependant.
#
#

PKGROOT		= /opt/rocks
REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../devel/devel
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build:
	gunzip -c $(NAME)-$(VERSION).tar.gz | $(TAR) -xf -
	(\
		cd $(NAME)-$(VERSION);	\
		./configure --prefix=$(PKGROOT);\
		$(MAKE);	\
	);

install::
	(\
		cd $(NAME)-$(VERSION);  \
		$(MAKE) prefix=$(ROOT)/$(PKGROOT) install; \
	);

clean::
	rm -rf $(NAME)-$(VERSION)
