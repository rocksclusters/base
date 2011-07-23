# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.30 2011/07/23 02:30:23 phil Exp $
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
# Revision 1.30  2011/07/23 02:30:23  phil
# Viper Copyright
#
# Revision 1.29  2011/06/08 19:47:23  anoop
# Moved script for setting up rocks db table access to
# admin scripts from node XML files
#
# Revision 1.28  2011/05/10 17:15:12  anoop
# Stupid permissions
#
# Revision 1.27  2011/05/10 00:45:27  anoop
# Random password generator
#
# Revision 1.26  2010/09/07 23:52:48  bruno
# star power for gb
#
# Revision 1.25  2010/06/22 21:26:22  mjk
# Build env is now from src/devel package, nothing outside of base roll.
#
# Revision 1.24  2009/05/01 19:06:50  mjk
# chimi con queso
#
# Revision 1.23  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.22  2008/03/06 23:41:32  mjk
# copyright storm on
#
# Revision 1.21  2008/01/14 19:58:37  bruno
# converted from spec file based to Makefile based.
#
# nuked dead scripts.
#
# nuked rocks-admin-frontend package.
#
# Revision 1.20  2007/10/02 23:58:20  anoop
# Remove all references to solaris, and added references to sunos.
# This is to standardize the naming between the python scripts and
# the Makefiles. One less variable that I'll have to deal with.
#
# Revision 1.19  2007/08/14 20:07:30  anoop
# Removed cluster-kickstart-solaris.
# No need for this anymore as we just
# use PXE first now
#
# Revision 1.18  2007/06/23 04:03:19  mjk
# mars hill copyright
#
# Revision 1.17  2007/05/30 20:47:30  anoop
# Make sure solaris utils build on solaris only. Trying to build them
# on Linux will fail
#
# Revision 1.16  2007/04/27 23:45:44  anoop
# Added the rocks-console-solaris command. This will be folded back into
# rocks console once more changes come into place
#
# Revision 1.15  2007/01/23 01:45:05  anoop
# Completed move of cluster-kickstart-solaris.c from kernel roll to base roll
#
# Revision 1.14  2006/12/06 00:20:20  anoop
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
# Revision 1.13  2006/12/02 01:04:53  anoop
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
# Revision 1.12  2006/09/11 22:47:02  mjk
# monkey face copyright
#
# Revision 1.11  2006/08/10 00:09:25  mjk
# 4.2 copyright
#
# Revision 1.10  2006/07/13 17:49:11  bruno
# only root can run shoot-node, big-red-button and rocks-user-sync
#
# Revision 1.9  2006/06/27 20:50:11  bruno
# replaced create-account and delete-account with a new method of maintaining
# user home directories. we now use the standard useradd and then call
# rocks-user-sync to push the user data to the nodes
#
# Revision 1.8  2006/06/22 22:53:44  nadya
# add empty build target
#
# Revision 1.7  2006/06/15 21:28:47  bruno
# new command to get the vnc and ekv consoles on an installing node
#
# Revision 1.6  2005/10/12 18:08:32  mjk
# final copyright for 4.1
#
# Revision 1.5  2005/09/16 01:02:11  mjk
# updated copyright
#
# Revision 1.4  2005/05/24 21:21:47  mjk
# update copyright, release is not any closer
#
# Revision 1.3  2005/05/23 23:59:22  fds
# Frontend Restore
#
# Revision 1.2  2005/03/26 01:04:04  fds
# Moved to rocks-security
#
# Revision 1.1  2005/03/01 02:02:41  mjk
# moved from core to base
#
# Revision 1.41  2004/10/06 21:39:46  fds
# Added insert-sheep
#
# Revision 1.40  2004/09/14 23:48:48  fds
# Utility to control WAN access to rolls
#
# Revision 1.39  2004/06/23 17:50:32  fds
# Added insert-ethers, cluster-fork now on compute nodes (meant to do this before).
#
# Revision 1.38  2004/04/26 20:20:49  fds
# Added bruno's big-red-button. Does not rely on PXE. Non-destructive, many
# of ways to avoid accidently hurting yourself. If you have not
# installed over wan, the button simply reboots the machine. If you go into
# Reinstall mode, you can back out in any step before formatting drives.
#
# Revision 1.37  2004/03/25 03:15:14  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.36  2004/02/12 00:39:58  fds
# More inline with rocks-config, easier.
#
# Revision 1.35  2003/10/30 02:35:15  fds
# New compute subpackage for rocksrc utilities.
#
# Revision 1.34  2003/09/23 19:33:25  fds
# Moved in rocksrc-lookuprc
#
# Revision 1.33  2003/09/23 18:59:42  fds
# Moved rocksrc-* scripts here from the sql package.
#
# Revision 1.32  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.31  2003/05/22 16:39:27  mjk
# copyright
#
# Revision 1.30  2003/03/10 21:35:59  bruno
# added delete-account, so you can now, you know, delete an account
#
# Revision 1.29  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.28  2002/10/18 21:33:25  mjk
# Rocks 2.3 Copyright
#
# Revision 1.27  2002/10/04 01:27:20  mjk
# rpm builds
#
# Revision 1.26  2002/10/03 23:06:08  mjk
# futzed with CVS repository structure
#
# Revision 1.25  2002/10/03 20:01:43  mjk
# move everything to /opt/rocks
#
# Revision 1.24  2002/06/26 19:06:39  phil
# Removed print statement
#
# Revision 1.23  2002/06/26 18:39:39  phil
# added arguments so that it performs like useradd
#
# Revision 1.22  2002/06/17 19:50:02  bruno
# 7.3-isms
#
# Revision 1.21  2002/04/22 20:20:38  mjk
# added busynodes
#
# Revision 1.20  2002/02/22 23:08:08  mjk
# added cluster-probe
#
# Revision 1.19  2002/02/21 21:33:27  bruno
# added new copyright
#
# Revision 1.18  2001/11/08 18:59:03  mjk
# Bumped version number
#
# Revision 1.17  2001/11/08 18:42:07  mjk
# NPACI Rocks 2.1.1 Release Copyright Notice
#
# Revision 1.16  2001/11/01 20:50:02  bruno
# update to cluster-kill
#
# Revision 1.15  2001/10/02 03:53:04  mjk
# - Added DISPLAY check for shoot-node
# - Moved over cluster-* suite of tools from cluster-config
#
# Revision 1.14  2001/05/09 20:17:10  bruno
# bumped copyright 2.1
#
# Revision 1.13  2001/04/10 14:16:26  bruno
# updated copyright
#
# Revision 1.12  2001/02/21 01:31:20  mjk
# Added webpage
#
# Revision 1.11  2001/02/21 00:33:44  mjk
# Nuke usermod bs
#
# Revision 1.10  2001/02/14 20:16:28  mjk
# Release 2.0 Copyright
#
# Revision 1.9  2001/02/07 00:55:15  mjk
# - Bump version number
# - Now works even if autofs is really lame.
#
# Revision 1.8  2001/02/06 21:11:14  mjk
# Bump version
#
# Revision 1.7  2001/02/06 20:08:37  mjk
# Abort is user alread exists
#
# Revision 1.6  2000/11/17 00:46:04  mjk
# *** empty log message ***
#
# Revision 1.5  2000/11/16 23:45:53  mjk
# Trimmed Makefile
# Cleaned up manpages
#
# Revision 1.4  2000/11/06 23:22:44  mjk
# Added shoot-node
#
# Revision 1.3  2000/11/03 06:10:48  mjk
# Added manpage
#
# Revision 1.2  2000/10/31 17:48:56  mjk
# Added --noyp flag to turn of rebuilding of the NIS database.  This is usefull
# when kickstarting a frontend machine so we can add account before NIS is
# turned on.
#
# Revision 1.1  2000/09/29 18:41:03  mjk
# *** empty log message ***
#

PKGROOT		= /opt/rocks
REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../devel/devel
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

ROOTONLY	= big-red-button rocks-user-sync shoot-node rocks-db-perms
ANYONE		= cluster-fork cluster-kill rocks-console gen_root_pw
SCRIPTS		= $(ANYONE) $(ROOTONLY)

build::

install:: $(SCRIPTS)
	mkdir -p $(ROOT)/$(PKGROOT)/sbin/
	$(INSTALL) -m0555 $(ANYONE) $(ROOT)/$(PKGROOT)/sbin/
	$(INSTALL) -m0500 $(ROOTONLY) $(ROOT)/$(PKGROOT)/sbin/

clean::
	rm -f $(SCRIPTS) cluster-kickstart-solaris.o
	rm -f $(NAME).spec.in

