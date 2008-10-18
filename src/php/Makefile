# $Id: Makefile,v 1.3 2008/10/18 00:56:01 mjk Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		           version 5.1  (VI)
# 
# Copyright (c) 2000 - 2008 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log: Makefile,v $
# Revision 1.3  2008/10/18 00:56:01  mjk
# copyright 5.1
#
# Revision 1.2  2008/07/22 00:49:50  anoop
# Minor changes to build solaris packages correctly
#
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
			--with-pdo-mysql=/opt/rocks/ \
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
