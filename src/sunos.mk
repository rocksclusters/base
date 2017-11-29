# $Id: sunos.mk,v 1.24 2012/11/27 00:48:01 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWindwer)
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
# $Log: sunos.mk,v $
# Revision 1.24  2012/11/27 00:48:01  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.23  2012/05/06 05:48:14  phil
# Copyright Storm for Mamba
#
# Revision 1.22  2011/08/24 06:12:09  anoop
# Need rocks-admin package for solaris
#
# Revision 1.21  2011/08/24 06:04:33  anoop
# Include sec-channel client for solaris
#
# Revision 1.20  2011/07/23 02:30:22  phil
# Viper Copyright
#
# Revision 1.19  2011/01/26 01:47:57  anoop
# Removed librocks from Solaris
#
# Revision 1.18  2010/10/20 21:32:46  mjk
# fix ordering
#
# Revision 1.17  2010/09/20 20:01:54  anoop
# Added lsof to solaris base roll
#
# Revision 1.16  2010/09/07 23:52:48  bruno
# star power for gb
#
# Revision 1.15  2009/11/23 20:33:41  anoop
# JDK for SunOS in the base roll
#
# Revision 1.14  2009/11/20 23:38:38  bruno
# from anoop:
# 	Disable building and installation of rocks-cpan and cpan-support on
# 	Solaris. Will re-enable for next release after testing.
#
# Revision 1.13  2009/11/10 21:32:28  anoop
# Install CPAN config files to help create RPM files from CPAN directly
# Make sure to build and install rocks-cpan during bootstrap of the base roll
# Include CPAN support on solaris as well. All CPAN files are only for
# foundation-perl
#
# Revision 1.12  2009/05/15 00:38:11  anoop
# Adding libdnet to the mix
#
# Revision 1.11  2009/05/01 19:06:49  mjk
# chimi con queso
#
# Revision 1.10  2009/04/15 20:58:02  anoop
# Added foundation-python-xml to the mix
#
# Revision 1.9  2008/12/10 23:19:05  anoop
# Bug fixes for sun build
#
# Revision 1.8  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.7  2008/09/22 16:10:39  bruno
# for anoop
#
# Revision 1.6  2008/07/28 18:38:16  anoop
# Added mercurial to base devel appliance build
#
# Revision 1.5  2008/07/22 00:49:50  anoop
# Minor changes to build solaris packages correctly
#
# Revision 1.4  2008/05/20 21:52:40  anoop
# More packages on Solaris
#
# Revision 1.3  2008/05/20 01:01:21  anoop
# Added new packages to the base roll. Linux.mk excludes those new packages
# when building the roll on Linux
#
# Revision 1.2  2008/03/06 23:41:31  mjk
# copyright storm on
#
# Revision 1.1  2007/10/03 00:02:02  anoop
# *** empty log message ***
#
# Revision 1.9  2007/09/04 19:28:39  anoop
# Additional Packages to bootstrap self.
#
# Revision 1.8  2007/09/04 16:20:53  anoop
# More solaris work
#
# Revision 1.7  2007/06/23 04:03:19  mjk
# mars hill copyright
#
# Revision 1.6  2007/06/13 17:51:09  anoop
# Pretty Printing
#
# Revision 1.5  2007/01/23 02:17:35  anoop
# Newer version of MySQLdb-python
#
# Revision 1.4  2006/12/06 00:20:20  anoop
# All the Makefiles get a bit of an overhaul
#
# $(INSTALL) is used instead of install
# $(MAKE) is used instead of make or gmake
# $(TAR) is used instead of tar of gtar
#
# The mode argument for the $(INSTALL) command needs to be numeric and
# follow the convention of
#
# install [-cs] [-g group] [-m mode] [-o owner] file ...  destination
# install  -d   [-g group] [-m mode] [-o owner] dir
#
# This is portable across solaris and linux.
#
# Finally "tar xzf $TARFILE.tar.gz" is replaced with "gunzip -c $TARFILE.tar.gz | tar -xf -"
# This is again done for portability.
#
# This needs to be the convention from now on.
#
# Revision 1.3  2006/09/11 22:47:01  mjk
# monkey face copyright
#
# Revision 1.2  2006/08/10 00:09:25  mjk
# 4.2 copyright
#
# Revision 1.1  2005/12/31 07:35:46  mjk
# - sed replace the python path
# - added os makefiles
#

SRCDIRS = foundation-coreutils foundation-gawk	\
	  foundation-readline foundation-wget	\
	  foundation-mysql foundation-python	\
	  foundation-perl foundation-libxml2	\
	  foundation-python-extras php postfix	\
	  foundation-ant sun-java		\
	  foundation-cvs foundation-gd		\
	  foundation-python-xml phpMyAdmin	\
	  foundation-graphviz foundation-rcs	\
	  foundation-mercurial devel cpan	\
	  pcre pylib command admin 411	\
	  411-master bittorrent tentakel dnet	\
	  ganglia-pylib receptor ssl lsof \
	  channel sec-channel
