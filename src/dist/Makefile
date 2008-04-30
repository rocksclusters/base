# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.15 2008/03/06 23:41:41 mjk Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		            version 5.0 (V)
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
# Revision 1.15  2008/03/06 23:41:41  mjk
# copyright storm on
#
# Revision 1.14  2007/06/23 04:03:21  mjk
# mars hill copyright
#
# Revision 1.13  2007/06/06 18:32:31  bruno
# two-word release name fixes
#
# Revision 1.12  2006/12/06 00:20:20  anoop
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
# Revision 1.11  2006/12/02 01:04:53  anoop
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
# Revision 1.10  2006/09/11 22:47:08  mjk
# monkey face copyright
#
# Revision 1.9  2006/08/10 00:09:31  mjk
# 4.2 copyright
#
# Revision 1.8  2006/07/19 19:20:25  bruno
# removed all traces to mount-loop and umount-loop
#
# Revision 1.7  2005/12/30 19:35:25  mjk
# removed some of the specfiles
#
# Revision 1.6  2005/10/12 18:08:37  mjk
# final copyright for 4.1
#
# Revision 1.5  2005/09/16 01:02:17  mjk
# updated copyright
#
# Revision 1.4  2005/09/07 02:28:50  bruno
# get the rocks version in a generic way
#
# Revision 1.3  2005/05/24 21:21:53  mjk
# update copyright, release is not any closer
#
# Revision 1.2  2005/03/02 20:08:15  mjk
# - created rocks-roll package (roll utils go here now)
# - moved dead code out of rocks-dist package
#
# Revision 1.1  2005/03/01 02:02:47  mjk
# moved from core to base
#
# Revision 1.41  2004/03/25 03:15:36  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.40  2003/12/15 22:52:45  mjk
#  added rocks-rollrc.xml
#
# Revision 1.39  2003/12/15 22:40:24  mjk
# added rocks-roll util
#
# Revision 1.38  2003/10/17 00:29:42  mjk
# install lib/Makefile for mirror building
#
# Revision 1.37  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.36  2003/08/13 22:11:35  mjk
# gingin changes
#
# Revision 1.35  2003/08/06 22:52:18  mjk
# Changed default setting to mirror from a Rocks version specific rocks-dist
# mirror.  This will allow us to release multiple version based on the
# same RedHat version w/o breaking older users who choose to re-mirror.
#
# Revision 1.34  2003/07/08 21:49:53  mjk
# removed non-xml rc files
#
# Revision 1.33  2003/07/07 16:25:07  mjk
# IA64 redux
#
# Revision 1.32  2003/06/30 23:47:16  mjk
# ia64 source distro building changes
#
# Revision 1.31  2003/06/27 22:27:42  mjk
# ia64 enterprise edition support
#
# Revision 1.30  2003/05/22 16:39:27  mjk
# copyright
#
# Revision 1.29  2003/04/02 17:57:38  bruno
# copycd now preserves timestamps -- thanks najib
#
# Revision 1.28  2003/04/01 00:07:00  mjk
# more mirror changes
#
# Revision 1.27  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.26  2002/12/21 02:03:02  bruno
# support for 'patch' -- the frontend patch command
#
# Revision 1.25  2002/11/13 21:55:14  mjk
# ia64 changes
#
# Revision 1.24  2002/10/18 21:33:26  mjk
# Rocks 2.3 Copyright
#
# Revision 1.23  2002/10/04 18:40:09  mjk
# rocks packages all build now
#
# Revision 1.22  2002/10/04 05:33:26  mjk
# more rpm target fixes
#
# Revision 1.21  2002/10/03 23:06:08  mjk
# futzed with CVS repository structure
#
# Revision 1.20  2002/10/03 20:01:43  mjk
# move everything to /opt/rocks
#
# Revision 1.19  2002/06/17 19:50:02  bruno
# 7.3-isms
#
# Revision 1.18  2002/05/15 18:57:09  bruno
# removed hard-coded 'arch' -- now programmatically determine it
#
# Revision 1.17  2002/02/21 21:33:28  bruno
# added new copyright
#
# Revision 1.16  2002/02/02 02:21:27  bruno
# 7.2 rev
#
# Revision 1.15  2001/11/08 18:59:03  mjk
# Bumped version number
#
# Revision 1.14  2001/11/08 18:42:09  mjk
# NPACI Rocks 2.1.1 Release Copyright Notice
#
# Revision 1.13  2001/10/30 02:18:27  mjk
# - killed off verify command
# - killed off server RPM
#
# Revision 1.12  2001/06/20 17:58:44  mjk
# - Added kickstart.cgi to RPM
# - Added rocks-dist-server RPM
# - Bumped version number
#
# Revision 1.11  2001/06/12 18:13:50  mjk
# - Added Force RPMS directory to docs
# - Always create a Force RPMS directory
#
# Revision 1.10  2001/05/21 19:30:11  mjk
# Cleanup
#
# Revision 1.9  2001/05/16 21:48:14  mjk
# Bumped version number
#
# Revision 1.7  2001/05/09 22:56:04  mjk
# Split off the python library into rocks-pylib package
#
# Revision 1.6  2001/05/09 22:33:10  mjk
# - better paths commads
# - more cdrom cleanup
#
# Revision 1.5  2001/05/09 20:17:21  bruno
# bumped copyright 2.1
#
# Revision 1.4  2001/05/09 19:14:23  bruno
# added "rm *pyc"
#
# Revision 1.3  2001/05/07 22:29:13  mjk
# - Release candidate 1
#
# Revision 1.2  2001/04/27 01:08:49  mjk
# - Created working 7.0 and 7.1 distibutions (in same tree even)
# - Added symlink() method to File object.  Trying to get the File object
#   to make the decision on absolute vs. relative symlinks.  So far we are
#   absolute everywhere.
# - Still missing CD making code.  Need to figure out how to read to
#   comps files using RedHat's anaconda python code.  Then we can decide
#   which RPMs can go on the second CD based on what is required in the
#   kickstart files.
#


REDHAT_LANG	= en
SCRIPTS     	= rocks-dist
PKGROOT		= /opt/rocks

REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../../../../..
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk


SEDSCRIPT +=	-e s%@REDHAT_RELEASE@%$(REDHAT_RELEASE)%g \
		-e s%@REDHAT_PRODUCT@%$(REDHAT_PRODUCT)%g \
		-e s%@REDHAT_LANG@%$(REDHAT_LANG)%g \
		-e s%@ROCKS_VERSION@%$(ROCKS_VERSION)%g \
		-e s%@RELEASE_NAME@%$(VERSION_NAME)%g


build: $(SCRIPTS) $(RCFILES)


install:: build
	mkdir -p $(ROOT)/$(PKGROOT)/sbin
	mkdir -p $(ROOT)/$(PKGROOT)/lib/rocks-dist
	mkdir -p $(ROOT)/$(PKGROOT)/bin
	mkdir -p $(ROOT)/$(PKGROOT)/etc
	mkdir -p $(ROOT)/home/install
	$(INSTALL) -m 0555 $(SCRIPTS) $(ROOT)/$(PKGROOT)/bin/
	$(INSTALL) -m 0444  rocks-distrc $(ROOT)/$(PKGROOT)/etc/
	$(INSTALL) -m 0444  lib/Makefile $(ROOT)/$(PKGROOT)/lib/rocks-dist/

clean::
	rm -f $(SCRIPTS) $(CGI)
	rm -f *.o
	rm -f $(NAME).spec.in
