# $Id: Makefile,v 1.1 2010/09/20 20:00:51 anoop Exp $

# @Copyright@
# @Copyright@

# $Log: Makefile,v $
# Revision 1.1  2010/09/20 20:00:51  anoop
# Added lsof to solaris base roll
#

REDHAT.ROOT	=	$(CURDIR)/../../
PKGROOT		=	/opt/rocks/
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build:
	bzcat $(NAME).tar.bz2 | $(TAR) -xf -
	( cd $(NAME)_$(VERSION) && $(TAR) -xf $(NAME)_$(VERSION)_src.tar )
	( cd $(NAME)_$(VERSION)/$(NAME)_$(VERSION)_src/;	\
	./Configure solariscc < /dev/null;			\
	$(MAKE);						\
	)

install::
	mkdir -p $(ROOT)/$(PKGROOT)
	mkdir -p $(ROOT)/$(PKGROOT)/bin
	mkdir -p $(ROOT)/$(PKGROOT)/man/man8/
	( cd $(NAME)_$(VERSION)/$(NAME)_$(VERSION)_src/;	\
	  $(INSTALL) -m 2755 -g sys lsof $(ROOT)/$(PKGROOT)/bin;\
	  $(INSTALL) -m 444 lsof.8 $(ROOT)/$(PKGROOT)/man/man8; \
	)

clean::
	rm -rf $(NAME)_$(VERSION)
