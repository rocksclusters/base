# 
# $Id: Makefile,v 1.7 2008/10/16 20:35:43 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		            version 5.0 (V)
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
# Revision 1.7  2008/10/16 20:35:43  bruno
# only call predoc once
#
# Revision 1.6  2008/04/07 21:52:28  bruno
# today's installment of docs
#
# Revision 1.5  2008/03/06 23:41:46  mjk
# copyright storm on
#
# Revision 1.4  2007/07/03 19:15:05  phil
# Darn it. Phil Checked in something when he didn't mean to. Revert to
# version 1.2 of each of these
#
# Revision 1.2  2007/06/23 04:03:26  mjk
# mars hill copyright
#
# Revision 1.1  2007/06/16 03:11:25  mjk
# builds with command reference
#
# Revision 1.14  2006/09/21 03:21:49  mjk
# remove resized images
#
# Revision 1.13  2006/09/21 03:21:02  mjk
# cleanup manual
#
# Revision 1.12  2006/09/11 18:16:24  mjk
# *** empty log message ***
#
# Revision 1.11  2006/08/15 19:11:26  mjk
# starting new manual
#
# Revision 1.10  2006/08/10 00:12:18  mjk
# 4.2 copyright
#
# Revision 1.9  2005/12/30 18:39:48  mjk
# remove spec files
#
# Revision 1.8  2005/10/18 20:20:39  bruno
# automatically set the copyright date
#
# Revision 1.7  2005/10/12 18:11:20  mjk
# final copyright for 4.1
#
# Revision 1.6  2005/09/16 01:04:58  mjk
# updated copyright
#
# Revision 1.5  2005/05/24 21:24:10  mjk
# update copyright, release is not any closer
#
# Revision 1.4  2005/04/05 22:24:27  nadya
# move logic of creating rocks.dsl, rocks.css and stylesheet-images to Rules.mk
# Add target predoc in order to make docs in a local directory
#
# Revision 1.3  2004/12/01 19:35:09  bruno
# touchups
#
# Revision 1.2  2004/10/15 03:36:35  mjk
# html build, pdf does not
#
# Revision 1.1  2004/10/14 20:51:29  mjk
# docs start
#

PKGROOT		= /var/www/html/roll-documentation/$(ROLL)/$(VERSION)
REDHAT.ROOT	= $(PWD)/../../
ROCKSROOT	= ../../../../..
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

default: $(NAME).spec ../$(NAME)-$(VERSION).tar.gz

build:
	jw --backend html --dsl $(PWD)/rocks.dsl#html index.sgml
	jw --backend pdf --dsl $(PWD)/rocks.dsl#print index.sgml

install::
	mkdir -p $(ROOT)/$(PKGROOT)/images/install
	mkdir -p $(ROOT)/$(PKGROOT)/stylesheet-images
	mkdir -p $(ROOT)/$(PKGROOT)/examples
	install -ma+r index.pdf 	$(ROOT)/$(PKGROOT)/$(NAME).pdf
	install -ma+r *.html    	$(ROOT)/$(PKGROOT)/
	install -ma+r images/*.png	$(ROOT)/$(PKGROOT)/images/
	install -ma+r images/install/*.png	\
		$(ROOT)/$(PKGROOT)/images/install
	install -ma+r stylesheet-images/{*.gif,*.png} \
		$(ROOT)/$(PKGROOT)/stylesheet-images/
	install -ma+r rocks.css $(ROOT)/$(PKGROOT)/

clean::
	rm -f *.html
	rm -f index.pdf
	rm -f images/resized-*.png

