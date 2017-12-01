#
# $Id: Makefile,v 1.24 2012/11/27 00:48:08 phil Exp $
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
# Revision 1.24  2012/11/27 00:48:08  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.23  2012/05/06 05:48:18  phil
# Copyright Storm for Mamba
#
# Revision 1.22  2012/01/23 19:52:33  phil
# Build on 5 or 6. Exact version to be build dependent on VERSION.MAJOR of Rocks itself
#
# Revision 1.21  2011/07/23 02:30:23  phil
# Viper Copyright
#
# Revision 1.20  2011/04/15 19:41:58  phil
# Updates to build under CentOS 5.6 and new anaconda version.
# Calling this version5.4.3. Codename Viper.
#
# Had to rebuild our own kudzu lib because the CentOS 5.6 version on initial
# release was bad. See bug ID 4813 on bugs.centos.org. That was a not fun debug.
#
# Splash screen is work in progress.
#
# Revision 1.19  2011/04/04 04:57:29  phil
# The Centos 5.5 update to gtk2 breaks anaconda-runtime's ability to
# properly wire gtk2 support into initrd. A one-line patch to an internal
# script works for both original 5.5 and updated 5.5 package.
# Makefile changes supports general patching of anaconda files in
# case we have to do this again for a future version.
#
# Revision 1.18  2010/09/07 23:52:48  bruno
# star power for gb
#
# Revision 1.17  2010/06/22 21:26:22  mjk
# Build env is now from src/devel package, nothing outside of base roll.
#
# Revision 1.16  2009/05/01 19:06:50  mjk
# chimi con queso
#
# Revision 1.15  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.14  2008/03/06 23:41:32  mjk
# copyright storm on
#
# Revision 1.13  2007/12/10 21:28:34  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.12  2007/06/23 04:03:20  mjk
# mars hill copyright
#
# Revision 1.11  2007/06/04 22:23:44  bruno
# do patching right
#
# Revision 1.10  2007/06/02 16:11:32  bruno
# patch anaconda 10.1.1.63
#
# Revision 1.9  2006/12/06 00:20:20  anoop
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
# Revision 1.8  2006/12/02 01:04:53  anoop
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
# Revision 1.7  2006/09/11 22:47:02  mjk
# monkey face copyright
#
# Revision 1.6  2006/08/10 00:09:26  mjk
# 4.2 copyright
#
# Revision 1.5  2006/06/15 23:07:34  bruno
# vnc for monitoring installations is ready for the beta
#
# Revision 1.4  2006/06/07 18:08:17  bruno
# added latest anaconda package
#
# needed to patch spec file in order to build on i386 to *not* use diet libraries
#
#

REDHAT.ROOT     = $(CURDIR)/../../
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

rpm::	$(HOME)/.rpmmacros patch
	rpmbuild -ba $(REDHAT.ROOT)/SPECS/$(NAME).spec

#
# Unpack the source tree, patch it, rebundle
patch:
	rpm -Uvh $(NAME)-$(VERSION)-$(SRPMRELEASE).src.rpm
	bunzip2 -c $(REDHAT.ROOT)/SOURCES/$(NAME)-$(VERSION).tar.bz2 | $(TAR) xvf -
	(								\
		if [ ! -d patch-files/anaconda-$(VERSION) ]; then exit; fi; \
		cd patch-files/anaconda-$(VERSION) ;			\
		for i in `find . -type f | grep -v CVS` ; do 		\
			cp $$i ../../$(NAME)-$(VERSION)/$$i;			\
		done							\
	)
	$(TAR) cf $(REDHAT.ROOT)/SOURCES/$(NAME)-$(VERSION).tar $(NAME)-$(VERSION)
	bzip2 -f $(REDHAT.ROOT)/SOURCES/$(NAME)-$(VERSION).tar

clean::
	$(RM) -rf $(NAME)-$(VERSION)	
