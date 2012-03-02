# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.23 2012/03/02 02:39:18 clem Exp $
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
# Revision 1.23  2012/03/02 02:39:18  clem
# Fix for the python unicode ucs4 problem (aka --enable-unicode=ucs4)
#
# Revision 1.22  2012/02/01 20:38:18  phil
# Support Python-2.6.7 as foundation for version 6. 2.4.2 for version 5
#
# Revision 1.21  2011/07/23 02:30:45  phil
# Viper Copyright
#
# Revision 1.20  2010/09/07 23:53:06  bruno
# star power for gb
#
# Revision 1.19  2010/06/22 21:26:23  mjk
# Build env is now from src/devel package, nothing outside of base roll.
#
# Revision 1.18  2009/05/01 19:07:06  mjk
# chimi con queso
#
# Revision 1.17  2008/10/18 00:56:00  mjk
# copyright 5.1
#
# Revision 1.16  2008/03/06 23:41:43  mjk
# copyright storm on
#
# Revision 1.15  2007/10/25 05:33:11  anoop
# Don't fail if we can't patch on Solaris
#
# Revision 1.14  2007/06/23 04:03:23  mjk
# mars hill copyright
#
# Revision 1.13  2006/12/06 00:20:21  anoop
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
# Revision 1.12  2006/12/02 01:04:54  anoop
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
# Revision 1.11  2006/09/11 22:47:14  mjk
# monkey face copyright
#
# Revision 1.10  2006/08/10 00:09:35  mjk
# 4.2 copyright
#
# Revision 1.9  2006/04/18 23:42:22  mjk
# *** empty log message ***
#
# Revision 1.8  2006/03/24 01:01:43  mjk
# do not use lib64 for 64bit
#
# Revision 1.7  2006/03/24 00:49:07  mjk
# no more patching
#
# Revision 1.6  2006/03/24 00:45:42  mjk
# *** empty log message ***
#
# Revision 1.5  2006/01/20 19:27:22  mjk
# add link from usr/bin to support old rolls
#
# Revision 1.4  2006/01/19 21:25:34  mjk
# enable unicode and ipv6
#
# Revision 1.3  2006/01/17 03:45:59  mjk
# might be complete now
#
# Revision 1.2  2006/01/16 23:13:58  mjk
# - more source built foundations
# - scipy stuff is here now (may move to hpc roll)
#
# Revision 1.1  2005/12/31 07:50:53  mjk
# build python from source
#

PKGROOT		= /opt/rocks
REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../devel/devel
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk


build:
	gunzip -c Python-$(VERSION).tar.gz | $(TAR) -xf -
	-cd patch-files-$(ARCH) && find . -type f | grep -v CVS | cpio -pduv ../
	( 								\
		cd Python-$(VERSION);					\
		./configure $(ADDFLAGS) --prefix=$(PKGROOT) 		\
				$(CONFIGOPTS);				\
		$(MAKE);						\
	)

install:: 
	mkdir -p $(ROOT)/$(PKGROOT)
ifeq ($(strip $(VERSION.MAJOR)),5)
	(								\
		cd Python-$(VERSION);					\
		$(MAKE) prefix=$(ROOT)/$(PKGROOT) install;		\
	)
else
	(								\
		cd Python-$(VERSION);					\
		$(MAKE) DESTDIR=$(ROOT) install;			\
	)
endif
	mkdir -p $(ROOT)/$(PKGROOT)/usr/bin;
	(								\
		cd $(ROOT)/$(PKGROOT)/usr/bin;				\
		ln -s ../../bin/python .;				\
	)

clean::
	rm -rf Python-$(VERSION)
	rm -f $(NAME).spec.in
