#
# $Id: Makefile,v 1.23 2012/11/27 00:48:42 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
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
# Revision 1.23  2012/11/27 00:48:42  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.22  2012/05/06 05:48:48  phil
# Copyright Storm for Mamba
#
# Revision 1.21  2012/03/13 06:05:58  phil
# Look at /tmp/interfaces and create list of interfaces so that user can
# select public and private interfaces.   On single physical interface frontends,
# create a virtual interface for the private.
#
# Revision 1.20  2011/07/23 02:30:49  phil
# Viper Copyright
#
# Revision 1.19  2011/07/19 22:22:41  phil
# Fixed dependency for build. Make sure rolls.html is created from
# rolls.html.in
#
# Revision 1.18  2011/07/18 21:53:15  phil
# Support version'ed centrals as
# central-rocksversion-arch.rocksclusters.org
#
# Revision 1.17  2010/09/07 23:53:09  bruno
# star power for gb
#
# Revision 1.16  2010/06/22 21:26:24  mjk
# Build env is now from src/devel package, nothing outside of base roll.
#
# Revision 1.15  2009/06/24 04:46:13  bruno
# restore roll tweaks
#
# Revision 1.14  2009/05/01 19:07:09  mjk
# chimi con queso
#
# Revision 1.13  2008/10/18 00:56:02  mjk
# copyright 5.1
#
# Revision 1.12  2008/03/06 23:41:45  mjk
# copyright storm on
#
# Revision 1.11  2007/06/23 04:03:25  mjk
# mars hill copyright
#
# Revision 1.10  2006/12/06 00:20:22  anoop
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
# Revision 1.9  2006/12/02 01:04:55  anoop
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
# Revision 1.8  2006/09/11 22:47:26  mjk
# monkey face copyright
#
# Revision 1.7  2006/09/08 18:52:03  bruno
# support to discover RHEL/CentOS/SL os disks
#
# Revision 1.6  2006/08/10 00:09:43  mjk
# 4.2 copyright
#
# Revision 1.5  2006/04/01 00:01:40  nadya
# change gif files to png
# update style
#
# Revision 1.4  2006/03/22 18:32:18  bruno
# make frames more self contained
#
# Revision 1.3  2006/03/15 01:07:30  bruno
# checkpoint
#
# Revision 1.2  2006/02/24 22:33:56  bruno
# closer
#
# Revision 1.1  2006/02/24 00:40:02  bruno
# the framework in which to run html-based screens during installation
#
#

PKGROOT		= /opt/rocks/screens
REDHAT.ROOT     = $(CURDIR)/../../
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

SCRIPTS		= rocks-buildscreens rocks-getroll.cgi sitexml2entities rocks-interface-menu rocks-mtu-menu


build: rolls.html
	$(MAKE) $(SCRIPTS)

rolls.html:	rolls.html.in
	$(SED) $(SEDSCRIPT) $^ > $@

rocks-getroll.cgi:	rocks-getroll.cgi.in
	$(SED) $(SEDSCRIPT) $^ > $@
	chmod +x $@

install::
	mkdir -p $(ROOT)/$(PKGROOT)
	(								\
		cp *html $(ROOT)/$(PKGROOT) ;				\
		cp *cgi $(ROOT)/$(PKGROOT) ;				\
		cp *png $(ROOT)/$(PKGROOT) ;				\
		cp *css $(ROOT)/$(PKGROOT) ;				\
		cp $(SCRIPTS) $(ROOT)/$(PKGROOT) ;			\
	)

clean::
	rm -f rocks-getroll.cgi rolls.html
	rm -f $(NAME).spec.in
	rm -f $(SCRIPTS)

