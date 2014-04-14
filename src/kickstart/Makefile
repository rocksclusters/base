#
# $Id: Makefile,v 1.28 2012/11/27 00:48:38 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 6.1.1 (Sand Boa)
# 
# Copyright (c) 2000 - 2014 The Regents of the University of California.
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
# Revision 1.28  2012/11/27 00:48:38  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.27  2012/05/06 05:48:44  phil
# Copyright Storm for Mamba
#
# Revision 1.26  2011/07/23 02:30:47  phil
# Viper Copyright
#
# Revision 1.25  2010/09/07 23:53:07  bruno
# star power for gb
#
# Revision 1.24  2010/06/22 21:26:24  mjk
# Build env is now from src/devel package, nothing outside of base roll.
#
# Revision 1.23  2009/05/01 19:07:07  mjk
# chimi con queso
#
# Revision 1.22  2008/10/18 00:56:01  mjk
# copyright 5.1
#
# Revision 1.21  2008/07/29 20:50:07  bruno
# first rev at a rocks command cgi
#
# Revision 1.20  2008/05/22 21:02:07  bruno
# rocks-dist is dead!
#
# moved default location of distro from /export/home/install to
# /export/rocks/install
#
# Revision 1.19  2008/03/06 23:41:43  mjk
# copyright storm on
#
# Revision 1.18  2007/08/14 20:25:25  anoop
# Minor cleanup
#
# Revision 1.17  2007/08/13 20:52:25  bruno
# - removed the SPEC file
# - moved the rocks-kickstart-external package into the post section of
#   central.xml
#
#

PKGROOT		= /opt/rocks
REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../devel/devel
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

RCFILES	= kcgirc
SCRIPTS	= kgen kdoc kcgi cfgen kroll screengen


build:	$(SCRIPTS) $(RCFILES)
	$(MAKE) -C utils

install::
	mkdir -p $(ROOT)/$(PKGROOT)/sbin
	$(INSTALL) -m 4555 utils/read-ssh-private-key $(ROOT)/$(PKGROOT)/sbin/
	$(INSTALL) -m 4555 utils/read-411-shared-key $(ROOT)/$(PKGROOT)/sbin/
	$(INSTALL) -m 0755 kdoc kgen cfgen kroll screengen \
		$(ROOT)/$(PKGROOT)/sbin/

	mkdir -p $(ROOT)/etc/rc.d/init.d
	cp init.d/rocks-kickstart $(ROOT)/etc/rc.d/init.d

	mkdir -p $(ROOT)/$(PKGROOT)/etc
	$(INSTALL) -m 0644 $(RCFILES) $(ROOT)/$(PKGROOT)/etc/

	mkdir -p $(ROOT)/export/rocks/install/sbin
	$(INSTALL) -m 0755 kcgi $(ROOT)/export/rocks/install/sbin/kickstart.cgi
	$(INSTALL) -m 0755 utils/*.cgi $(ROOT)/export/rocks/install/sbin/

	mkdir -p $(ROOT)/export/rocks/install/site-profiles/$(VERSION)/nodes
	$(INSTALL) -m 0644 $(wildcard site-nodes/*.xml) \
		$(ROOT)/export/rocks/install/site-profiles/$(VERSION)/nodes/



clean::
	$(MAKE) -C utils clean
	rm -f $(RCFILES) $(SCRIPTS)
	rm -f $(SPECFILE).in

