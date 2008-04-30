# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.21 2008/04/02 16:59:37 bruno Exp $
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
# Revision 1.21  2008/04/02 16:59:37  bruno
# nuke dead commands
#
# put message in other commands that point the user to the appropriate rocks
# command-line command.
#
# Revision 1.20  2008/03/06 23:41:45  mjk
# copyright storm on
#
# Revision 1.19  2007/06/23 04:03:25  mjk
# mars hill copyright
#
# Revision 1.18  2007/05/30 22:58:10  anoop
# Removed unused utils from Makefile
#
# Revision 1.17  2006/12/06 00:20:22  anoop
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
# Revision 1.16  2006/12/02 01:04:55  anoop
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
# Revision 1.15  2006/09/11 22:47:27  mjk
# monkey face copyright
#
# Revision 1.14  2006/08/10 00:09:45  mjk
# 4.2 copyright
#
# Revision 1.13  2006/08/04 17:54:12  mjk
# fix phil's removal of dead code
#
# Revision 1.12  2006/03/25 18:05:54  bruno
# rocks scripts should only be executable by root -- thanks to Matt Wise for
# the bug report
#
# Revision 1.11  2006/01/24 01:06:15  yuchan
# remove miss-print in Makefile
#
# Revision 1.10  2006/01/24 00:55:17  yuchan
# add po for insert-ethers
#
# Revision 1.9  2005/12/30 19:35:26  mjk
# removed some of the specfiles
#
# Revision 1.8  2005/10/12 18:08:46  mjk
# final copyright for 4.1
#
# Revision 1.7  2005/10/11 05:36:20  phil
# Probe the ethernet hardware on the frontend and put it into the database
#
# Revision 1.6  2005/09/16 01:02:25  mjk
# updated copyright
#
# Revision 1.5  2005/05/24 21:22:00  mjk
# update copyright, release is not any closer
#
# Revision 1.4  2005/05/23 23:59:24  fds
# Frontend Restore
#
# Revision 1.3  2005/04/08 18:20:26  bruno
# added rocks-partition command-line program to delete partitions from the
# partitions table for a specific node
#
# Revision 1.2  2005/03/14 20:25:18  fds
# Plugin architecture: service control is modular. Rolls can add hooks without
# touching insert-ethers itself. Plugins can be ordered relative to each other by
# filename.
#
# Revision 1.1  2005/03/01 02:03:17  mjk
# moved from core to base
#
# Revision 1.61  2005/02/16 20:22:16  phil
# check for duplicateIP correctly when static ip is specified
#
# Revision 1.60  2005/02/16 06:03:50  phil
# Missing space on "--dump output"
#
# Revision 1.59  2005/02/11 03:19:30  phil
# hmmm...installed release on plain 3.3.0 is -13
#
# Revision 1.58  2005/02/11 03:14:10  phil
# Added add-appliance to mix
# bumped RELEASE
#
# Revision 1.57  2004/11/23 01:29:16  bruno
# mason type pretty one day
#
# Revision 1.56  2004/10/06 18:30:49  fds
# Support for security levels. Minimal changes to insert-ethers.
#
# Revision 1.55  2004/08/16 22:19:28  bruno
# support to include add-new-appliance into the package
#
# Revision 1.54  2004/04/13 03:21:05  fds
# Daily mysql cluster backup to RCS (phil's idea).
#
# Revision 1.53  2004/03/25 03:15:52  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.52  2003/12/17 18:51:40  mjk
# added lock file
#
# Revision 1.51  2003/09/23 19:34:05  fds
# Moved rocksrc-lookuprc into admin
#
# Revision 1.50  2003/09/23 19:06:57  fds
# Moved rocksrc-* scripts here from the sql package.
#
# Revision 1.49  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.48  2003/08/15 21:07:26  mjk
# - RC files only built one per directory (fixed)
# - Default CGI arch is native (used to be i386)
# - Added scheduler,nameservices to rocksrc.xml
# - insert-ethers know what scheduler and nameservice we use
# - I forget what else
#
# Revision 1.47  2003/05/22 16:39:28  mjk
# copyright
#
# Revision 1.46  2003/04/18 04:54:44  phil
# Added update-node-info script, manpage
#
# Revision 1.45  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.44  2002/11/27 04:57:53  bruno
# fix: update database, rebuild files, restart services, then pop window
#
# Revision 1.43  2002/10/18 21:33:26  mjk
# Rocks 2.3 Copyright
#
# Revision 1.42  2002/10/18 03:46:59  phil
# Added add-extra-nic to the mix
#
# Revision 1.41  2002/10/04 05:33:26  mjk
# more rpm target fixes
#
# Revision 1.40  2002/10/03 23:06:08  mjk
# futzed with CVS repository structure
#
# Revision 1.39  2002/10/03 20:01:43  mjk
# move everything to /opt/rocks
#
# Revision 1.38  2002/09/28 14:49:58  bruno
# added static ip address generation
#
# Revision 1.37  2002/07/30 20:03:24  bruno
# added makemachines to rebuild ethernet-based machines.LINUX file(s)
#
# Revision 1.36  2002/07/13 00:26:23  bruno
# fixed a bug in the restart loop
#
# Revision 1.35  2002/06/27 02:00:59  phil
# 	Added the entries that are in the networks table
#
# Revision 1.34  2002/05/21 00:11:43  bruno
# added 'pbs_server' restart for OpenPBS
#
# Revision 1.33  2002/02/21 21:33:27  bruno
# added new copyright
#
# Revision 1.32  2002/02/08 21:50:20  mjk
# removed newt
#
# Revision 1.31  2002/02/05 22:37:12  mjk
# - copy files from CDROM or Mirror
# - needs testing
#
# Revision 1.30  2002/01/14 20:22:06  bruno
# added 'state' to package
#
# Revision 1.29  2001/11/08 18:59:03  mjk
# Bumped version number
#
# Revision 1.28  2001/11/08 18:42:08  mjk
# NPACI Rocks 2.1.1 Release Copyright Notice
#
# Revision 1.27  2001/06/05 01:28:09  mjk
# Node names in the database are now optional.
#
# Revision 1.26  2001/06/04 21:14:00  mjk
# - Uses rocks-pylib
# - Does Aliases
#
# Revision 1.25  2001/05/11 23:03:24  bruno
# left a bunch of debug statements in insert-ethers
#
# Revision 1.24  2001/05/11 21:39:47  bruno
# cleanup
#
# Revision 1.23  2001/05/09 20:17:15  bruno
# bumped copyright 2.1
#
# Revision 1.22  2001/05/02 22:07:42  bruno
# updates for 'model' and 'rank' insert-ethers
#
# Revision 1.21  2001/04/03 21:26:45  bruno
# added '--replace' flag to insert-ethers
#
# Revision 1.20  2001/03/28 00:30:46  mjk
# Don't keep ',' delimited lists in the database any more.
#
# Revision 1.19  2001/03/22 20:40:59  mjk
# bumped version
#
# Revision 1.18  2001/02/21 01:32:02  mjk
# *** empty log message ***
#
# Revision 1.17  2001/02/15 00:46:58  mjk
# Added makeresolv.py
#
# Revision 1.16  2001/02/14 20:16:31  mjk
# Release 2.0 Copyright
#
# Revision 1.15  2001/02/06 22:53:17  mjk
# Bumped version number
#
# Revision 1.14  2001/02/03 02:37:05  bruno
# multi-cabinet fixes
#
# Revision 1.13  2001/02/01 22:43:04  bruno
# added automatic generation of /etc/hosts and /etc/dhcpd.conf if an
# entry is added
#
# Revision 1.12  2001/01/25 23:29:25  bruno
# added 'insert-ethers'
#
# Revision 1.11  2000/11/17 00:45:42  mjk
# added manpages
#
# Revision 1.10  2000/10/11 20:53:42  mjk
# bumped version number
#
# Revision 1.9  2000/10/09 18:42:59  mjk
# Added option-129 for usher flags
#
# Revision 1.8  2000/10/06 18:16:08  mjk
# Compute aliases now also support cabinet based names.
#
# Revision 1.7  2000/10/05 00:16:49  mjk
# IP addresses for compute nodes are now compute here, and not stored in
# the database.  Address are assigned in table order starting at the top
# of the subnet specified in the DHCP Options table and count down.
# Manually assigned addresses should be assigned at the bottom of the IP
# space and count up.  Never the two shall meet.
#
# Aliases for compute, frontend, and management nodes are now computed
# here, and not stored in the database.  Create-alias.py is no longer
# needed.
#
# Added makeethers to support annoying RARPing Myrinet hardware.
#
# Revision 1.6  2000/09/26 13:56:58  bruno
# bumped version number
#
# Revision 1.5  2000/09/19 21:23:54  mjk
# *** empty log message ***
#
# Revision 1.4  2000/09/19 21:18:59  mjk
# Added create-alias
# bumped version number
#
# Revision 1.3  2000/09/12 22:34:06  mjk
# bumped version number
#
# Revision 1.2  2000/09/08 16:59:07  mjk
# DHCP hostname and ip options don't want quotes, everything else does.
# Bumped version number
#
# Revision 1.1  2000/09/01 17:54:45  mjk
# Copyright notice
#
#


PKGROOT	  = /opt/rocks
SCRIPTS   = insert-ethers add-extra-nic
PLUGINS = $(wildcard plugins/*py)
PLUGINDIR = $(PKGROOT)/var/plugins/insertethers

REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../../../../..
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

RCFILES = add-new-appliancerc staterc \
	add-extra-nicrc insert-ethersrc
	
po ::
	$(MAKE) -C po

build: $(SCRIPTS) $(RCFILES) po

install:: build
	mkdir -p $(ROOT)/$(PKGROOT)/sbin/
	mkdir -p $(ROOT)/$(PKGROOT)/etc/
	mkdir -p $(ROOT)/var/db/RCS
	mkdir -p $(ROOT)/$(PLUGINDIR)
	mkdir -p $(ROOT)/etc/cron.daily
	$(INSTALL) -m 0544 $(SCRIPTS) $(ROOT)/$(PKGROOT)/sbin/
	$(INSTALL) -m 0644  $(RCFILES) $(ROOT)/$(PKGROOT)/etc/
	$(INSTALL) -m 0700 backup-cluster-db.sh \
		$(ROOT)/etc/cron.daily/backup-cluster-db
	$(INSTALL) -m 0644 $(PLUGINS) $(ROOT)/$(PLUGINDIR)

	$(MAKE) install -C po 


clean::
	rm -f $(SCRIPTS)
	rm -f $(NAME).spec.in


