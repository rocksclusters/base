# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.7 2010/09/07 23:53:08 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4 (Maverick)
# 
# Copyright (c) 2000 - 2010 The Regents of the University of California.
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
# Revision 1.7  2010/09/07 23:53:08  bruno
# star power for gb
#
# Revision 1.6  2010/06/22 21:26:24  mjk
# Build env is now from src/devel package, nothing outside of base roll.
#
# Revision 1.5  2009/10/05 17:19:15  bruno
# need to rename LICENSE file to LICENSE.FreeDOS, otherwise, the automatic spec
# file building code tried to include the contents of the LICENSE file which
# caused the rpm building processes to fail.
#
# Revision 1.4  2009/05/01 19:07:08  mjk
# chimi con queso
#
# Revision 1.3  2008/10/18 00:56:02  mjk
# copyright 5.1
#
# Revision 1.2  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.1  2008/03/05 05:15:51  phil
# Put this in the base roll for V
#
# Revision 1.3  2008/02/27 22:24:43  phil
# Add License file
#
# Revision 1.2  2008/02/27 20:14:50  phil
# Grab the files in the addon directory
#
# Revision 1.1  2008/02/27 20:00:36  phil
# Automate the steps to build a 2.88MB Floppy image for flashing over pxe.
#

PKGROOT		= /opt/pxeflash
REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../devel/devel
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

FLASHFILES 	= addon 
CP		= /bin/cp

build:
	make -f Makefile.disk BOOTIMG=$(DOSBOOT) build

install::
	mkdir -p $(ROOT)/$(PKGROOT)
	mkdir -p $(ROOT)/$(PKGROOT)/addon
	$(CP) $(DOSBOOT) $(ROOT)/$(PKGROOT)
	mkdir -p $(ROOT)/tftpboot/pxelinux
	install -m755 /usr/lib/syslinux/memdisk $(ROOT)/tftpboot/pxelinux
	make -f Makefile.disk ROOT=$(ROOT) BOOTIMG=$(DOSBOOT) install
	install -m644 Makefile.disk $(ROOT)/$(PKGROOT)/Makefile
	install -m644 version.mk $(ROOT)/$(PKGROOT)/version.mk
	install -m644 README $(ROOT)/$(PKGROOT)/README
	install -m644 LICENSE.FreeDOS $(ROOT)/$(PKGROOT)/
	$(TAR) cf - --exclude CVS addon | (cd $(ROOT)/$(PKGROOT); $(TAR) xvf - ) 


clean::
	make -f Makefile.disk ROOT=$(ROOT) BOOTIMG=$(DOSBOOT) clean 
