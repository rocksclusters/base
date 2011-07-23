# $Id: Makefile,v 1.4 2011/07/23 02:30:44 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4.3 (Viper)
# 
# Copyright (c) 2000 - 2011 The Regents of the University of California.
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
# 	Development Team at the San Diego Supercomputer Center at the
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
# Revision 1.4  2011/07/23 02:30:44  phil
# Viper Copyright
#
# Revision 1.3  2010/09/07 23:53:05  bruno
# star power for gb
#
# Revision 1.2  2010/06/22 21:26:22  mjk
# Build env is now from src/devel package, nothing outside of base roll.
#
# Revision 1.1  2009/10/01 22:55:22  bruno
# moved from java roll to base roll
#
# Revision 1.8  2009/05/01 19:07:19  mjk
# chimi con queso
#
# Revision 1.7  2008/10/18 00:56:11  mjk
# copyright 5.1
#
# Revision 1.6  2008/08/29 18:22:57  mjk
# can build outside of tree
#
# Revision 1.5  2008/03/06 23:41:55  mjk
# copyright storm on
#
# Revision 1.4  2007/06/23 04:03:47  mjk
# mars hill copyright
#
# Revision 1.3  2006/09/11 22:49:04  mjk
# monkey face copyright
#
# Revision 1.2  2006/08/10 00:11:08  mjk
# 4.2 copyright
#
# Revision 1.1  2006/07/30 01:30:41  mjk
# added eclipse (from javatools)
#
# Revision 1.1  2005/11/01 02:02:21  phil
# various java-based tools
#

PKGROOT		= /opt/eclipse
REDHAT.ROOT	= $(PWD)/../../
ROCKSROOT       = ../devel/devel
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

install::
	mkdir -p $(ROOT)/$(PKGROOT)
	mkdir -p $(ROOT)/etc/profile.d
	(							\
		cd $(NAME);					\
		find . -type f | cpio -pduv $(ROOT)/$(PKGROOT);	\
	)
	install -m444 $(NAME).sh	$(ROOT)/etc/profile.d
	install -m444 $(NAME).csh	$(ROOT)/etc/profile.d

build: 
	gunzip -c $(NAME)-SDK-$(VERSION)-linux-gtk.tar.gz | tar -x

clean::
	rm -rf $(NAME)
