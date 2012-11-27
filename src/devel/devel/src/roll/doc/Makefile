# 
# $Id: Makefile,v 1.5 2012/11/27 00:48:33 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.6 (Emerald Boa)
# 		         version 6.1 (Emerald Boa)
# 
# Copyright (c) 2000 - 2013 The Regents of the University of California.
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
# Revision 1.5  2012/11/27 00:48:33  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.4  2012/05/06 05:48:39  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2011/07/23 02:30:43  phil
# Viper Copyright
#
# Revision 1.2  2010/09/07 23:53:05  bruno
# star power for gb
#
# Revision 1.1  2010/06/22 21:07:44  mjk
# build env moving into base roll
#
# Revision 1.13  2009/05/01 19:07:15  mjk
# chimi con queso
#
# Revision 1.12  2008/10/18 00:56:07  mjk
# copyright 5.1
#
# Revision 1.11  2008/03/06 23:41:50  mjk
# copyright storm on
#
# Revision 1.10  2007/06/23 04:03:33  mjk
# mars hill copyright
#
# Revision 1.9  2006/09/11 22:48:04  mjk
# monkey face copyright
#
# Revision 1.8  2006/08/10 00:10:20  mjk
# 4.2 copyright
#
# Revision 1.7  2005/10/12 18:09:08  mjk
# final copyright for 4.1
#
# Revision 1.6  2005/09/16 01:02:44  mjk
# updated copyright
#
# Revision 1.5  2005/05/24 21:22:13  mjk
# update copyright, release is not any closer
#
# Revision 1.4  2005/04/05 20:44:19  nadya
# move logic of creating rocks.dsl, rocks.css and stylesheet-images to Rules.mk
# Add target predoc in order to make docs in a local directory
#
# Revision 1.3  2004/02/12 01:08:50  nadya
# add rocks.css to the distro
#
# Revision 1.2  2004/02/12 00:46:11  nadya
# add styling from rocks docs
#
# Revision 1.1  2004/01/06 23:26:43  bruno
# first pass
#
#
#


PKGROOT		= /var/www/html/roll-documentation/devel/$(VERSION)
REDHAT.ROOT	= /usr/src/redhat
ROCKSROOT	= ../../..
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk


default: $(NAME).spec ../$(NAME)-$(VERSION).tar.gz

html: predoc index.sgml
	jw --backend html --dsl $(PWD)/rocks.dsl#html index.sgml

pdf: predoc index.sgml
	jw --backend pdf --dsl $(PWD)/rocks.dsl#print index.sgml

build: html pdf

install:: build
	mkdir -p $(ROOT)/$(PKGROOT)/images
	mkdir -p $(ROOT)/$(PKGROOT)/stylesheet-images
	install -ma+r index.pdf 	$(ROOT)/$(PKGROOT)/$(NAME).pdf
	install -ma+r *.html    	$(ROOT)/$(PKGROOT)/
	install -ma+r images/*.png	$(ROOT)/$(PKGROOT)/images/
	install -ma+r stylesheet-images/{*.gif,*.png} \
		$(ROOT)/$(PKGROOT)/stylesheet-images/
	install -ma+r rocks.css $(ROOT)/$(PKGROOT)/

clean::
	rm -f *.html
	rm -f index.pdf


