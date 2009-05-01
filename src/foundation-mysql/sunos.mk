# $Id: sunos.mk,v 1.7 2009/05/01 19:07:06 mjk Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
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
# $Log: sunos.mk,v $
# Revision 1.7  2009/05/01 19:07:06  mjk
# chimi con queso
#
# Revision 1.6  2009/04/21 23:57:20  anoop
# Minor modification to Makefile to enable Solaris build
#
# Revision 1.5  2008/10/18 00:55:59  mjk
# copyright 5.1
#
# Revision 1.4  2008/05/20 01:05:49  anoop
# refreshed mysql for solaris only
#
# Revision 1.3  2008/03/06 23:41:42  mjk
# copyright storm on
#
# Revision 1.2  2007/10/25 04:25:42  anoop
# Builds correctly with Sun Studio 12
#
# Revision 1.1  2007/10/02 23:58:20  anoop
# Remove all references to solaris, and added references to sunos.
# This is to standardize the naming between the python scripts and
# the Makefiles. One less variable that I'll have to deal with.
#
# Revision 1.5  2007/06/23 04:03:22  mjk
# mars hill copyright
#
# Revision 1.4  2007/05/08 23:14:14  anoop
# Compilation fixed for solaris and made a little more generic and backward
# compatible.
#
# Revision 1.3  2007/04/04 17:14:47  mjk
# mysql5 runs on linux
#
# Revision 1.2  2007/01/23 01:39:45  anoop
# Moved cluster-kickstart-solaris to the base roll admin package. Made more
# sense to put it there rather than in rocks-boot. Since others may have another
# opinion, I left the other files in the same spot.
#
# Alpha roll build pkgs along with RPMs.
# Foundation-mysql Makefile errors corrected.
# rocks-console gets its own solaris version for now. The changes are minimal and will
# be merged back to the original rocks-console.py file as soon as I've had a
# chance to test it further.
#
# Revision 1.1  2006/12/06 00:25:46  anoop
# The XML file for MYSQL service on solaris. These two files are solaris specific
#

build:
MYSQL_LDFLAGS	= "-L/opt/SUNWspro/lib -lCstd -lCrun"

install::
	mkdir -p $(ROOT)/$(PKGROOT)/share/mysql/
	mkdir -p $(ROOT)/$(INIT_SCRIPTS_DIR)
	$(INSTALL) mysql-server.xml $(ROOT)/$(PKGROOT)/share/mysql/mysql-server.xml
	(							\
		cd mysql-$(VERSION);				\
		$(INSTALL) -m 0744 support-files/mysql.server	\
			$(ROOT)/$(INIT_SCRIPTS_DIR)/mysqld;	\
	)
