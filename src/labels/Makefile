# $Id: Makefile,v 1.10 2008/10/18 00:56:01 mjk Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		           version 5.1  (VI)
# 
# Copyright (c) 2000 - 2008 The Regents of the University of California.
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
# Revision 1.10  2008/10/18 00:56:01  mjk
# copyright 5.1
#
# Revision 1.9  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.8  2007/06/23 04:03:24  mjk
# mars hill copyright
#
# Revision 1.7  2006/12/06 00:20:21  anoop
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
# Revision 1.6  2006/12/02 01:04:55  anoop
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
# Revision 1.5  2006/09/11 22:47:20  mjk
# monkey face copyright
#
# Revision 1.4  2006/08/10 00:09:39  mjk
# 4.2 copyright
#
# Revision 1.3  2006/06/05 20:07:24  anoop
# Bug fixes of the rather irritating kind
#
# Revision 1.2  2006/05/31 23:19:13  anoop
# Removed spec file dependency. Modified Makefiles to reflect this. Changed all
# python and cgi scripts to use the system default rocks rather than hardcoding
# the path
#
# Revision 1.1  2006/05/31 23:02:24  anoop
# Moving the labels report to the base roll from the hpc roll
#
# Revision 1.4  2005/10/12 18:09:47  mjk
# final copyright for 4.1
#
# Revision 1.3  2005/09/16 01:03:24  mjk
# updated copyright
#
# Revision 1.2  2005/05/24 21:22:49  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/02/17 04:16:56  bruno
# moved source to the hpc roll
#
# Revision 1.6  2004/03/25 03:15:44  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.5  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.4  2003/05/22 16:39:28  mjk
# copyright
#
# Revision 1.3  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.2  2003/02/04 05:53:29  bruno
# we've got label making
#
# Revision 1.1  2003/02/04 05:18:18  bruno
# initial release
#
#
REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../../../../..
SCRIPTS	=	labels www/index

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

include version.mk

build:	$(SCRIPTS)
	mkdir -p $(ROOT)/$(PY.ROCKS)/rocks/reports
	mkdir -p $(ROOT)/var/www/html/homepage
	mkdir -p $(ROOT)/var/www/html/labels
	
install::
	$(INSTALL) -m 0444 www/*.html $(ROOT)/$(PKGROOT)/var/www/html/homepage
	$(INSTALL) -m 0444 www/Makefile $(ROOT)/$(PKGROOT)/var/www/html/labels
	$(INSTALL) -m 0555 www/index $(ROOT)/$(PKGROOT)/var/www/html/labels/index.cgi
	$(INSTALL) -m 0555 www/rocks.png $(ROOT)/$(PKGROOT)/var/www/html/labels
	$(INSTALL) -m 0555 labels \
		$(ROOT)/$(PY.ROCKS)/rocks/reports/labels.py


clean::
	-rm -f *.spec
	rm -rf $(SCRIPTS)

