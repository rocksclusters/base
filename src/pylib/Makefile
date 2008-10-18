# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.22 2008/10/18 00:56:02 mjk Exp $
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
# Revision 1.22  2008/10/18 00:56:02  mjk
# copyright 5.1
#
# Revision 1.21  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.20  2007/10/02 23:58:20  anoop
# Remove all references to solaris, and added references to sunos.
# This is to standardize the naming between the python scripts and
# the Makefiles. One less variable that I'll have to deal with.
#
# Revision 1.19  2007/09/04 19:00:16  anoop
# Makefile now dynamically changes the MySQL socket path during building the
# package on Solaris. On linux, it does not change the path.
#
# NOTE: rcs tags generation commented out for now. Must be re-enabled before
# release
# NOTE: Writing to /root/install.log commented out for now. Must be re-enabled
# before release
#
# Revision 1.18  2007/06/23 04:03:24  mjk
# mars hill copyright
#
# Revision 1.17  2007/06/06 18:32:31  bruno
# two-word release name fixes
#
# Revision 1.16  2007/02/28 03:06:29  mjk
# - "rocks list host xml" replaces kpp
# - kickstart.cgi uses "rocks list host xml"
# - indirects in node xml now works
#
# Revision 1.15  2007/02/27 19:17:21  mjk
# Added release/version vars to rocks.__init__
#
# Revision 1.14  2006/12/06 00:20:22  anoop
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
# Revision 1.13  2006/12/02 01:04:55  anoop
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
# Revision 1.12  2006/09/11 22:47:22  mjk
# monkey face copyright
#
# Revision 1.11  2006/08/10 00:09:40  mjk
# 4.2 copyright
#
# Revision 1.10  2006/01/16 23:14:10  mjk
# - more source built foundations
# - scipy stuff is here now (may move to hpc roll)
#
# Revision 1.9  2006/01/16 06:25:03  mjk
# use INSTALL var
#
# Revision 1.8  2005/12/31 06:19:01  mjk
# python.mk already included
#
# Revision 1.7  2005/10/12 18:08:42  mjk
# final copyright for 4.1
#
# Revision 1.6  2005/09/16 01:02:21  mjk
# updated copyright
#
# Revision 1.5  2005/09/02 00:05:49  bruno
# pushing toward 4.1 beta
#
# Revision 1.4  2005/07/13 01:22:03  mjk
# more foundation changes
#
# Revision 1.3  2005/05/24 21:21:57  mjk
# update copyright, release is not any closer
#
# Revision 1.2  2005/03/01 00:29:22  mjk
# new paths for roll
#
# Revision 1.1  2005/03/01 00:22:08  mjk
# moved to base roll
#
# Revision 1.26  2004/03/25 03:15:47  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.25  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.24  2003/08/06 21:17:52  mjk
# - Added rocksrc base XML config file
# - Backed out of file.py tabs vs. spaces bogus fix
# - Moved mkdir from spec into makefile
#
# Revision 1.23  2003/07/07 20:28:52  bruno
# roll enablers
#
# Revision 1.22  2003/05/22 16:39:28  mjk
# copyright
#
# Revision 1.21  2003/04/03 20:57:03  bruno
# initialize some variables in the 'patch' section -- thanks najib!
#
# Revision 1.20  2003/04/01 00:07:00  mjk
# more mirror changes
#
# Revision 1.19  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.18  2002/12/21 02:03:22  bruno
# support for frontend patching -- the 'patch' command
#
# Revision 1.17  2002/12/18 17:40:29  bruno
# bump release
#
# Revision 1.16  2002/12/12 17:39:46  bruno
# updated RELEASE to 1
#
# Revision 1.15  2002/10/18 21:33:26  mjk
# Rocks 2.3 Copyright
#
# Revision 1.14  2002/10/04 05:33:26  mjk
# more rpm target fixes
#
# Revision 1.13  2002/10/03 23:06:08  mjk
# futzed with CVS repository structure
#
# Revision 1.12  2002/10/03 20:01:43  mjk
# move everything to /opt/rocks
#
# Revision 1.11  2002/06/17 19:50:02  bruno
# 7.3-isms
#
# Revision 1.10  2002/03/19 23:03:36  bruno
# added multi cdrom building when select 'cdrom'
#
# Revision 1.9  2002/02/21 21:33:28  bruno
# added new copyright
#
# Revision 1.8  2001/11/08 19:37:26  mjk
# *** empty log message ***
#
# Revision 1.7  2001/11/08 18:59:03  mjk
# Bumped version number
#
# Revision 1.5  2001/10/26 17:31:56  bruno
# rocks-dist now respects the RPMHOME environment variable
#
# Revision 1.4  2001/10/25 21:41:44  bruno
# changes for new rocks sql schema
#
# Revision 1.3  2001/05/21 19:29:50  mjk
# - Cleanup
# - Don't create symlink for the ekv and piece-pipe packages anymore
#
# Revision 1.2  2001/05/09 22:55:28  mjk
# RPM builds
#
# Revision 1.1  2001/05/09 22:43:09  mjk
# initial checkin
#

PYLIB		= $(wildcard *.py)
PKGROOT		= /opt/rocks
REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT	= ../../../../..
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

RCFILES		= rocksrc
SEDSCRIPT +=	-e s%@VERSION_MAJOR@%$(VERSION.MAJOR)%g \
		-e s%@VERSION_MINOR@%$(VERSION.MINOR)%g \
		-e s%@VERSION_MICRO@%$(VERSION.MICRO)%g \
		-e s%@VERSION_NAME@%$(VERSION_NAME)%g

build: $(RCFILES) __init__.py
	mkdir -p $(ROOT)/$(PY.ROCKS)/rocks
	mkdir -p $(ROOT)/$(PKGROOT)/etc
	

install:: build
	$(INSTALL) -m 0444 $(PYLIB) $(ROOT)/$(PY.ROCKS)/rocks
	(\
		if [ $(OS) == 'sunos' ]; then \
		sed -e 's/var.lib.mysql/var\/opt\/rocks\/mysql/g' sql.py > \
		$(ROOT)/$(PY.ROCKS)/rocks/sql.py; \
		fi ;\
	);
	$(INSTALL) -m 0444 rocksrc $(ROOT)/$(PKGROOT)/etc
	@echo "version = \"$(ROCKS_VERSION)\"" >> \
		$(ROOT)/$(PY.ROCKS)/rocks/__init__.py
	@echo "release = \"$(VERSION_NAME)\"" >> \
		$(ROOT)/$(PY.ROCKS)/rocks/__init__.py


clean::
	rm -f *.pyc
	rm -f rocksrc
