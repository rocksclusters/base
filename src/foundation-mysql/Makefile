# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.32 2012/11/27 00:48:36 phil Exp $
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
# Revision 1.32  2012/11/27 00:48:36  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.31  2012/05/06 05:48:43  phil
# Copyright Storm for Mamba
#
# Revision 1.30  2011/11/02 05:08:56  phil
# First take on bootstrap0. Packages, command line and processing to
# bring up the rocks database on a non-Rocks installed host.
# Also reworked generation of post sections to work more like Solaris:
# Each post section now creates a shell script with the desired interpreter.
# Report post command creates a shell script from the post section of a
# (set of) node xml files.
#
# Revision 1.29  2011/07/23 02:30:45  phil
# Viper Copyright
#
# Revision 1.28  2011/04/23 18:34:19  phil
# remove deprecated build option. Patch startup to use rocks paths/files
#
# Revision 1.27  2010/09/07 23:53:06  bruno
# star power for gb
#
# Revision 1.26  2010/06/22 21:26:23  mjk
# Build env is now from src/devel package, nothing outside of base roll.
#
# Revision 1.25  2009/05/01 19:07:06  mjk
# chimi con queso
#
# Revision 1.24  2009/04/29 22:21:51  bruno
# set the permissions so apache can read the mysql socket
#
# Revision 1.23  2009/04/21 23:57:20  anoop
# Minor modification to Makefile to enable Solaris build
#
# Revision 1.22  2009/04/21 23:08:54  mjk
# - runs on linux now
# - solaris is broken until linux work is complete
#
# Revision 1.21  2009/04/18 00:40:34  mjk
# - checkpoint still broken
# - running on different port and mostly different my.cnf
#
# Revision 1.20  2008/10/18 00:55:59  mjk
# copyright 5.1
#
# Revision 1.19  2008/05/20 01:04:29  anoop
# Made Makefiles more Solaris friendly
#
# Revision 1.18  2008/03/06 23:41:42  mjk
# copyright storm on
#
# Revision 1.17  2007/06/23 04:03:22  mjk
# mars hill copyright
#
# Revision 1.16  2007/06/09 00:07:21  anoop
# Escape the backslash
#
# Revision 1.15  2007/06/07 16:19:10  mjk
# - add "rocks add host"
# - add "rocks dump host"
# - add "rocks dump host interface"
# - remove "rocks add host new"
# - add mysql db init script to foundation-mysql
# - more flexible hostname lookup for the command line
#
# Revision 1.14  2007/06/05 17:56:22  mjk
# fix var path for foundation server
#
# Revision 1.12  2007/04/04 17:14:47  mjk
# mysql5 runs on linux
#
# Revision 1.11  2007/01/23 02:05:36  anoop
# Small changes to MySQL makefile
#
# Revision 1.10  2007/01/23 01:39:45  anoop
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
# Revision 1.9  2006/12/06 00:20:21  anoop
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
# Revision 1.8  2006/12/02 01:04:54  anoop
# Ridiculously big ass commit.
# Also known as the week after thanksgiving 2006. Or "The day Anoop
# broke Rocks".
#
# Main Changes.
#
# 1. Added a roll-profile.mk file. This is meant as a makefile for building
# the profile rpm containing all the XML files meant for the roll. This is a
# breakaway from the spec.in file method of building the profile RPM.
#
# 2. The variable PWD is now changed to CURDIR. The main reason for this is
# PWD is supplied by the shell. CURDIR is the variable supplied by gmake itself.
# This means we can have a slightly more platform independant way of doing things.
# Also Solaris was failing to set PWD correctly in the source directories, wreaking
# havoc on the location of the BUILD and PKG directories.
#
# Revision 1.7  2006/09/11 22:47:12  mjk
# monkey face copyright
#
# Revision 1.6  2006/08/10 00:09:35  mjk
# 4.2 copyright
#
# Revision 1.5  2006/07/13 00:44:14  nadya
# use MYSQL_LDFLAGS for configure flags
#
# Revision 1.4  2006/01/16 23:13:53  mjk
# - more source built foundations
# - scipy stuff is here now (may move to hpc roll)
#
# Revision 1.3  2006/01/16 17:51:02  mjk
# fix clean target
#
# Revision 1.2  2006/01/16 17:50:33  mjk
# builds
#
# Revision 1.1  2006/01/16 16:10:51  mjk
# *** empty log message ***
#

PKGROOT		= /opt/rocks
PKGVAR		= /var/$(PKGROOT)/mysql
INSTALLDB	= $(PKGROOT)/sbin/mysql-install-db
REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../devel/devel

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build:
	gunzip -c mysql-$(VERSION).tar.gz | $(TAR) -xf -
	(cd patch-files && find mysql-$(VERSION) -type f | grep -v CVS | cpio -pduv ../)
	( 								\
		cd mysql-$(VERSION);					\
		./configure --prefix=$(PKGROOT)				\
			--localstatedir=$(PKGVAR)			\
			--with-unix-socket-path=$(PKGVAR)/mysql.sock	\
			--with-tcp-port=40000				\
			--with-mysqld-user=rocksdb			\
			--enable-thread-safe-client			\
			--with-ssl					\
			--without-debug					\
			LDFLAGS=$(MYSQL_LDFLAGS) CFLAGS=$(MYSQL_CFLAGS)	\
			;						\
		$(MAKE);						\
	)

install::
	mkdir -p $(ROOT)/$(PKGROOT)/etc/
	mkdir -p $(ROOT)/$(PKGROOT)/sbin/
	mkdir -p $(ROOT)/$(PKGVAR)
	chmod a+rx $(ROOT)/$(PKGVAR)
	(								\
		cd mysql-$(VERSION);					\
		$(MAKE) prefix=$(ROOT)/$(PKGROOT) install;		\
	)
	$(INSTALL) -m 0644 my.cnf $(ROOT)/$(PKGROOT)/etc/my.cnf;
	rm -rf $(ROOT)/$(PKGROOT)/mysql-test
	rm -rf $(ROOT)/$(PKGROOT)/sql-bench
	rm -rf $(ROOT)/var/opt/rocks/mysql
	echo "#!/bin/bash"				>  $(ROOT)/$(INSTALLDB)
	echo "$(PKGROOT)/bin/mysql_install_db \\" 	>> $(ROOT)/$(INSTALLDB)
	echo "  --defaults-file=$(PKGROOT)/etc/my.cnf\\">> $(ROOT)/$(INSTALLDB)
	echo "	--basedir=$(PKGROOT) \\" 		>> $(ROOT)/$(INSTALLDB)
	echo "	--datadir=$(PKGVAR)  \\"		>> $(ROOT)/$(INSTALLDB)
	echo "	--user=rocksdb"				>> $(ROOT)/$(INSTALLDB)
	chmod +x $(ROOT)/$(INSTALLDB)

clean::
	rm -rf mysql-$(VERSION)
