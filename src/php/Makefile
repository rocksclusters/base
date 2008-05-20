# $Id: Makefile,v 1.1 2008/05/20 01:03:07 anoop Exp $
#
# @Copyright@
# @Copyright@
#
# $Log: Makefile,v $
# Revision 1.1  2008/05/20 01:03:07  anoop
# Added pcre postfix and php for solaris
#
# Revision 1.1  2008/05/02 00:16:55  anoop
# Adding PHP for solaris. Will move to a different roll in the
# future
#

# DESCRIPTION:
# A Solaris only package.


PKGROOT = /opt/rocks
REDHAT.ROOT = $(CURDIR)/../../
ROCKSROOT = ../../../../..

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build:
	gunzip -c $(NAME)-$(VERSION).tar.gz | $(TAR) -xf -
	( \
		cd $(NAME)-$(VERSION); \
		./configure --prefix=$(PKGROOT) \
			--with-config-file-path=/etc \
			--with-apxs2=/usr/apache2/bin/apxs \
			--with-mysql=/opt/rocks/ \
			--with-mysql-sock=/var/opt/rocks/mysql/;\
		$(MAKE); \
	)

install::
	mkdir -p $(ROOT)/etc/apache2/
	cp -rf /etc/apache2/httpd.conf-example $(ROOT)/etc/apache2/httpd.conf
	( \
		cd $(NAME)-$(VERSION); \
		$(MAKE) INSTALL_ROOT=$(ROOT) install; \
		$(INSTALL) -m0644 php.ini-recommended \
			$(ROOT)/etc/php.ini; \
	)
	rm -rf $(ROOT)/etc/apache2/httpd.conf.bak \
		$(ROOT)/etc/apache2/httpd.conf
	sed -f httpd.conf.sed /etc/apache2/httpd.conf-example > \
		$(ROOT)/etc/apache2/httpd.conf.php
	chown root:sys $(ROOT)/etc $(ROOT)/usr
	chmod 0755 $(ROOT)/etc $(ROOT)/usr
	chown -R root:bin $(ROOT)/etc/apache2 $(ROOT)/usr/apache2
	chmod 0755 $(ROOT)/etc/apache2 $(ROOT)/usr/apache2
	rm -rf $(ROOT)/.[a-z]*
	rm -rf $(ROOT)/$(PKGROOT)/lib/php/.[a-z]*

clean::
	-rm -rf $(NAME)-$(VERSION)
