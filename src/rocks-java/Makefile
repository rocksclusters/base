# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.3 2012/11/27 00:48:42 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
# 		         version 7.0 (Manzanita)
# 
# Copyright (c) 2000 - 2017 The Regents of the University of California.
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
# Revision 1.3  2012/11/27 00:48:42  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.2  2012/05/06 05:48:48  phil
# Copyright Storm for Mamba
#
# Revision 1.1  2012/04/12 05:17:40  phil
# Moved to base roll from java roll
#
# Revision 1.21  2011/07/23 02:31:12  phil
# Viper Copyright
#
# Revision 1.20  2010/09/07 23:53:21  bruno
# star power for gb
#
# Revision 1.19  2009/05/01 19:07:20  mjk
# chimi con queso
#
# Revision 1.18  2008/11/30 19:38:40  anoop
# *** empty log message ***
#
# Revision 1.17  2008/10/18 00:56:12  mjk
# copyright 5.1
#
# Revision 1.16  2008/09/12 22:21:55  mjk
# JDK6 (linux) added /usr/java/latest.  Start using this instead of the
# versioned name so we can never do this again.
#
# Revision 1.15  2008/09/12 19:31:34  anoop
# Bug fixes to re-enable building outside the tree.
#
# Revision 1.14  2008/09/12 19:04:12  anoop
# Made the java roll more solaris friendly
#
# Revision 1.13  2008/08/29 18:22:36  mjk
# can build outside of tree
#
# Revision 1.12  2008/03/06 23:41:55  mjk
# copyright storm on
#
# Revision 1.11  2007/06/23 04:03:47  mjk
# mars hill copyright
#
# Revision 1.10  2006/12/07 23:07:20  mjk
# - Update JDK
# - Split single node file into server/client/base
# - No more per arch profile scripts
# - Eclipse only on frontend
# - tomcat and jboss everywhere (but not running)
#
# Revision 1.9  2006/09/11 22:49:05  mjk
# monkey face copyright
#
# Revision 1.8  2006/08/10 00:11:09  mjk
# 4.2 copyright
#
# Revision 1.7  2005/12/30 17:57:35  mjk
# remove spec file
#
# Revision 1.6  2005/10/12 18:10:00  mjk
# final copyright for 4.1
#
# Revision 1.5  2005/09/16 01:03:37  mjk
# updated copyright
#
# Revision 1.4  2005/05/24 21:23:00  mjk
# update copyright, release is not any closer
#
# Revision 1.3  2005/02/24 01:11:54  mjk
# java version differs by arch
#
# Revision 1.2  2003/11/08 19:45:32  mjk
# fixed rpm errors
#
# Revision 1.1  2003/11/08 19:19:42  mjk
# only install the SDK
#

REDHAT.ROOT = $(CURDIR)/../../
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build:

install::
	mkdir -p $(ROOT)/etc/profile.d
	$(INSTALL) -m755  java.sh.$(OS)  $(ROOT)/etc/profile.d/java.sh
	$(INSTALL) -m755  java.csh.$(OS) $(ROOT)/etc/profile.d/java.csh

clean::
	rm -f $(NAME).spec.in
