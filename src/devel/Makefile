# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.11 2012/11/27 00:48:32 phil Exp $
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
# Revision 1.11  2012/11/27 00:48:32  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.10  2012/05/06 05:48:39  phil
# Copyright Storm for Mamba
#
# Revision 1.9  2011/07/23 02:30:42  phil
# Viper Copyright
#
# Revision 1.8  2010/09/21 00:37:57  anoop
# don't include CVS files in the RPM
#
# Revision 1.7  2010/09/07 23:53:04  bruno
# star power for gb
#
# Revision 1.6  2010/06/22 21:07:44  mjk
# build env moving into base roll
#
# Revision 1.5  2009/05/01 19:07:05  mjk
# chimi con queso
#
# Revision 1.4  2008/11/30 19:13:29  anoop
# Added templates directory to the rocks-devel package
#
# Revision 1.3  2008/10/18 00:55:59  mjk
# copyright 5.1
#
# Revision 1.2  2008/08/19 19:02:37  mjk
# added create-package.mk
#
# Revision 1.1  2008/06/10 22:44:01  mjk
# added rocks-devel
#

PKGROOT		= /opt/rocks/share/devel
REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT	= devel
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build:

install::
	mkdir -p $(ROOT)/$(PKGROOT)/
	mkdir -p $(ROOT)/etc/profile.d/
	$(INSTALL) -m0555 rocks-devel.sh  $(ROOT)/etc/profile.d
	$(INSTALL) -m0555 rocks-devel.csh $(ROOT)/etc/profile.d
	(								\
		cd devel;						\
		find . | grep -v CVS | cpio -pduv $(ROOT)/$(PKGROOT)/;		\
	)

clean::
