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
# Revision 1.11  2010/09/07 23:52:48  bruno
# star power for gb
#
# Revision 1.10  2010/06/22 21:26:22  mjk
# Build env is now from src/devel package, nothing outside of base roll.
#
# Revision 1.9  2009/05/01 19:06:49  mjk
# chimi con queso
#
# Revision 1.8  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.7  2008/08/12 19:14:33  anoop
# Bug fix
#
# Revision 1.6  2008/08/09 19:27:51  anoop
# beginning of actual usable 411 plugins. For now password and group file
# plugins
#
# Revision 1.5  2008/08/07 20:49:21  anoop
# Create plugin directory, so that 411put doesn't fail
#
# Revision 1.4  2008/07/22 00:49:50  anoop
# Minor changes to build solaris packages correctly
#
# Revision 1.3  2008/05/20 01:04:29  anoop
# Made Makefiles more Solaris friendly
#
# Revision 1.2  2008/03/06 23:41:32  mjk
# copyright storm on
#
# Revision 1.1  2007/12/10 21:28:33  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.8  2007/06/23 04:03:38  mjk
# mars hill copyright
#
# Revision 1.7  2006/09/11 22:48:49  mjk
# monkey face copyright
#
# Revision 1.6  2006/08/10 00:10:53  mjk
# 4.2 copyright
#
# Revision 1.5  2005/10/12 18:09:42  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:03:19  mjk
# updated copyright
#
# Revision 1.3  2005/05/27 23:28:00  fds
# Include the Group.mk makefile
#
# Revision 1.2  2005/05/24 21:22:45  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/01 02:02:40  mjk
# moved from core to base
#
# Revision 1.2  2004/07/21 22:05:51  fds
# A place for other file trees.
#
# Revision 1.1  2004/05/25 02:31:05  fds
# Since becoming a 411-master is a job that should not be taken on lightly, we
# are moving the tools necessary for it into a separate package. These files are
# essentially unchanged from those in 'rocks-411', except the initscript, which
# is slightly simpler.
#
#

SCRIPTS = 411put
PKGROOT = /opt/rocks

REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../devel/devel
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

PLUGIN_DIR = /opt/rocks/var/plugins/411

build: $(SCRIPTS)

install:: build
	mkdir -p $(ROOT)/$(PKGROOT)/sbin/
	mkdir -p $(ROOT)/etc/411.d
	chmod 0755 $(ROOT)/etc/411.d
	mkdir -p $(ROOT)/var/411/groups/Compute
	mkdir -p $(ROOT)/$(INIT_SCRIPTS_DIR)
	mkdir -p $(ROOT)/$(PLUGIN_DIR)
	$(INSTALL) -m555 $(SCRIPTS)  $(ROOT)/$(PKGROOT)/sbin/
	$(INSTALL) -m700 init.d/411 $(ROOT)/$(INIT_SCRIPTS_DIR)
	$(INSTALL) -m444 var/Makefile $(ROOT)/var/411
	$(INSTALL) -m644 var/Files.mk $(ROOT)/var/411
	$(INSTALL) -m644 var/Group.mk $(ROOT)/var/411
	$(INSTALL) -m400 plugins/*.py $(ROOT)/$(PLUGIN_DIR)

clean::
	rm -f $(SCRIPTS)
	rm -f *.pyc
