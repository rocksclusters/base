# $Id: Makefile,v 1.15 2008/03/06 23:41:40 mjk Exp $
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
# Revision 1.15  2008/03/06 23:41:40  mjk
# copyright storm on
#
# Revision 1.14  2007/08/13 19:47:22  bruno
# cleanup of rocks-config
#
# no longer uses a SPEC file
#
# Revision 1.13  2007/06/23 04:03:20  mjk
# mars hill copyright
#
# Revision 1.12  2007/05/07 22:15:45  bruno
# ganglia restore rrds moved to ganglia roll
#
# Revision 1.11  2006/12/06 00:20:20  anoop
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
# Revision 1.10  2006/12/02 01:04:53  anoop
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
# Revision 1.9  2006/09/11 22:47:04  mjk
# monkey face copyright
#
# Revision 1.8  2006/08/10 00:09:27  mjk
# 4.2 copyright
#
# Revision 1.7  2006/06/23 19:58:04  nadya
# sh does not understand brace expansion
#
# Revision 1.6  2005/12/13 01:49:07  bruno
# added the kickstart graph visualization and database management links back
# to the frontend's web site.
#
# Revision 1.5  2005/10/12 18:08:33  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/20 20:35:13  bruno
# removed the CGI method of building the default rocks homepage
#
# Revision 1.3  2005/09/16 01:02:13  mjk
# updated copyright
#
# Revision 1.2  2005/05/24 21:21:49  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/01 02:02:42  mjk
# moved from core to base
#
# Revision 1.99  2004/03/25 03:15:27  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.98  2003/12/22 19:20:17  mjk
# added rocks-dmesg
#
# Revision 1.97  2003/12/19 18:39:10  fds
# Correct permissions for CGI scripts.
#
# Revision 1.96  2003/12/18 21:34:32  fds
# I'm an awk maniac.
#
# Revision 1.95  2003/09/24 17:08:45  fds
# Bruno's changes for RH 9
#
# Revision 1.94  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.93  2003/08/11 17:40:50  fds
# Including dot-graph.php in homepage.
#
# Revision 1.92  2003/07/23 21:29:19  fds
# Added ganglia RRD restore.
#
# Revision 1.91  2003/06/27 23:18:25  fds
# Adding Kickstart graph functionality.
#
# Revision 1.90  2003/05/22 16:39:27  mjk
# copyright
#
# Revision 1.89  2003/04/03 18:28:09  bruno
# bumped RELEASE to 2
#
# Revision 1.88  2003/02/17 19:57:47  bruno
# removed bssh
#
# Revision 1.87  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.86  2003/02/06 19:15:22  fds
# Simpler, more logic in makefile, normalized.
#
# Revision 1.85  2003/01/25 05:41:20  bruno
# bumped revision number to 1
#
# Revision 1.84  2002/10/18 21:33:25  mjk
# Rocks 2.3 Copyright
#
# Revision 1.83  2002/10/04 05:33:26  mjk
# more rpm target fixes
#
# Revision 1.82  2002/10/03 23:06:08  mjk
# futzed with CVS repository structure
#
# Revision 1.81  2002/08/27 23:32:01  bruno
# updated version number to 2.3
#
# Revision 1.80  2002/05/07 22:54:37  bruno
# added -t flag for ssh-keygen profile.d
#
# Revision 1.79  2002/02/21 21:33:27  bruno
# added new copyright
#
# Revision 1.78  2001/11/08 18:59:03  mjk
# Bumped version number
#
# Revision 1.77  2001/11/08 18:42:07  mjk
# NPACI Rocks 2.1.1 Release Copyright Notice
#
# Revision 1.76  2001/10/24 20:14:18  mjk
# Synced with bruno's changes
#
# Revision 1.75  2001/07/28 23:14:40  bruno
# bumped rev for new patched loader
#
# Revision 1.74  2001/07/03 15:02:14  bruno
# release number bump
#
# Revision 1.73  2001/06/28 22:24:20  bruno
# added 'watchdog' timer in the form of sliming loader
#
# Revision 1.72  2001/06/13 21:21:34  bruno
# added loader-rocks (a watchdog for the installation)
#
# modified cluster-kickstart to add 'file:' to the command line (use this to
# trick anaconda into getting kickstart files over the network)
#
# bumped the version number
#
# Revision 1.71  2001/06/05 00:32:13  mjk
# RPM now hold all bootdist for a given architecture
#
# Revision 1.70  2001/05/09 20:17:11  bruno
# bumped copyright 2.1
#
# Revision 1.69  2001/05/08 21:12:48  bruno
# 7.1 changes
#
# Revision 1.68  2001/05/05 01:14:55  bruno
# bumped version number for new cluster-[ps|kill|fork]
#
# Revision 1.67  2001/04/27 21:26:37  bruno
# fixes for 7.1
#
# Revision 1.66  2001/04/13 23:44:33  mjk
# *** empty log message ***
#
# Revision 1.65  2001/04/11 20:59:06  mjk
# Frontend fixes again
#
# Revision 1.64  2001/04/10 14:16:27  bruno
# updated copyright
#
# Revision 1.63  2001/04/04 17:11:32  mjk
# bump version
#
# Revision 1.62  2001/04/03 22:43:15  mjk
# Frontend store DNS dhcp derived data in the database
#
# Revision 1.61  2001/03/26 23:07:43  mjk
# *** empty log message ***
#
# Revision 1.60  2001/03/15 15:20:34  bruno
# release number bumped for bssh bug fix
#
# Revision 1.59  2001/03/06 18:31:21  bruno
# bumped version number to signify inclusion of gm 1.4
#
# Revision 1.58  2001/02/21 05:22:15  mjk
# Added web docs
#
# Revision 1.57  2001/02/17 01:32:15  mjk
# *** empty log message ***
#
# Revision 1.56  2001/02/14 21:43:04  mjk
# bumb version
#
# Revision 1.55  2001/02/14 20:16:29  mjk
# Release 2.0 Copyright
#
# Revision 1.54  2001/02/14 17:57:10  mjk
# Removed the SSL cert-creat stuff
#
# Revision 1.53  2001/02/10 00:41:51  mjk
# bump version
#
# Revision 1.52  2001/02/03 15:51:39  bruno
# added code to gracefully shutdown the node.
#
# this umounts all filesystems, so on the next boot after the reinstall, all
# the non-root filesystem will be clean when they're remounted.
#
# Revision 1.51  2001/01/29 23:46:48  bruno
# support for 'noreboot'
#
# Revision 1.50  2001/01/17 05:14:46  bruno
# bumped release # for new cluster-kickstart.c tweaks
#
# Revision 1.49  2001/01/12 22:26:28  bruno
# cleaned up the hack which required us to build this package twice
#
# Revision 1.48  2001/01/11 05:19:04  bruno
# redhat 7.0 updates
#
# Revision 1.47  2000/12/21 18:58:11  bruno
# cleanup
#
# Revision 1.46  2000/12/21 18:28:25  bruno
# removed root's identity.pub from package
#
# Revision 1.45  2000/12/21 16:10:56  bruno
# bump release number to signify bug fixes for bssh
#
# Revision 1.44  2000/12/18 18:34:58  bruno
# bumped version number to 1.19 to signify added 'bssh-*' scripts
#
# Revision 1.43  2000/11/09 16:48:23  bruno
# bumped the release number
#
# Revision 1.42  2000/11/02 04:44:32  mjk
# *** empty log message ***
#
# Revision 1.41  2000/11/02 00:28:24  bruno
# removed bootdisk making -- only needed when distdev wants to build a cd
# distribution. not needed for the common case of rebuilding a distribution
#
# Revision 1.40  2000/10/31 19:26:32  mjk
# post config changes
#
# Revision 1.39  2000/10/31 18:18:09  mjk
# Even more frontend changes
#
# Revision 1.38  2000/10/30 21:03:26  bruno
# bumped version
#
# Revision 1.37  2000/10/23 16:52:33  mjk
# *** empty log message ***
#
# Revision 1.36  2000/10/23 14:12:52  bruno
# comment update
#
# Revision 1.35  2000/10/20 21:03:16  mjk
# Ownership of the nfsdiag cron file is now done in the postconfig
# script.  This is needed since the user doesn't exist at kickstart
# time.
#
# Revision 1.34  2000/10/13 23:32:02  mjk
# DHCP Interfaces turn on multicast route
# Bumped version number
#
# Revision 1.33  2000/10/11 19:54:06  bruno
# changes to handle redhat 6.2 directory structure (in anticipation of
# supporting future redhat releases).
#
# Revision 1.32  2000/10/09 18:43:55  mjk
# Added option-129 DHCP option for usher flags
#
# Revision 1.31  2000/10/06 23:55:58  mjk
# Added nfsdiag for NFS/AutoFS heartbeat
#
# Revision 1.30  2000/10/06 18:21:38  bruno
# bumped revision number
#
# Revision 1.29  2000/09/28 21:51:25  bruno
# added 'bootdisk' making
#
# Revision 1.28  2000/09/28 21:41:58  bruno
# bumped version and added 'create-account'
#
# Revision 1.27  2000/09/26 14:02:53  bruno
# added 'snmpd.conf' to clean directive
#
# Revision 1.26  2000/09/17 22:53:46  bruno
# small tweak to remove my dumbassness
#
# Revision 1.25  2000/09/17 22:47:04  bruno
# many changes (and a *huge* hack) in an attempt to clean up this process
#
# Revision 1.24  2000/09/12 22:35:46  mjk
# Bumped version number
#
# Revision 1.23  2000/09/12 20:39:02  mjk
# *** empty log message ***
#
# Revision 1.22  2000/08/30 20:49:03  mjk
# Added postconfig script to fix file perms on cluster-kickstart
#
# Revision 1.21  2000/08/29 19:51:07  mjk
# Converted cluster-kickstart script to C code
# Added Copyright notices
#
# Revision 1.20  2000/08/16 23:59:27  bruno
# added gm to the SRPMS directory
#
# Revision 1.19  2000/08/09 22:13:52  bruno
# added inetd.conf to install directive
#
# Revision 1.18  2000/08/09 20:56:23  mjk
# Added blank inetd.conf file to sanitize frontend kickstart
#
# Revision 1.17  2000/07/11 18:23:55  mjk
# Added NIS support
# Added dhclient.conf config
# Added log-server and some other minor dhcp options
#
# Revision 1.16  2000/07/08 05:11:36  mjk
# Added ifup ifdown
#
# Revision 1.15  2000/07/07 18:58:59  mjk
# Force include of local Rules.mk
#
# Revision 1.14  2000/07/06 20:58:08  mjk
# Removed $(CONFIG) references from Config.mk
#
# Revision 1.13  2000/07/06 20:50:47  mjk
# Created Config.mk for kickstart post config
#
# Revision 1.12  2000/07/06 19:08:16  mjk
# Bumped version number
# Cleaned up spec file
#
# Revision 1.11  2000/07/06 18:39:53  mjk
# Extract common stuff into Rules.mk
# Added rpm: target
# Spec file now generated from .spec.in
#
# Revision 1.10  2000/07/06 00:15:07  bruno
# cleanup
#
# Revision 1.9  2000/07/05 22:32:43  mjk
# Added /etc/inittab config file
#
# Revision 1.8  2000/07/05 19:59:35  mjk
# Fixed snmpd.conf copy
#
# Revision 1.7  2000/07/05 19:09:43  mjk
# Move config file copies into Makefile
#
# Revision 1.6  2000/06/30 20:32:19  mjk
# No pumpaction
#
# Revision 1.5  2000/06/30 20:25:36  mjk
# Add snmp config file
#
# Revision 1.4  2000/06/27 00:30:38  mjk
# Work with bash|tcsh
#
# Revision 1.3  2000/06/23 18:59:02  mjk
# initial
#
# Revision 1.2  2000/06/15 20:47:00  bruno
# cleaned up the tar portion of the file
#
# Revision 1.1  2000/06/15 20:22:12  bruno
# initial release
#
#

SCRIPTS  = cd-label
ROOT = 

default: $(NAME).spec ../$(NAME)-$(VERSION).tar.gz

REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../../../../..
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build:

install::

	mkdir -p $(ROOT)/etc/rc.d
	$(INSTALL) -m700 rocksconfig.d/rc.rocksconfig.py \
		$(ROOT)/etc/rc.d/rc.rocksconfig

	mkdir -p $(ROOT)/etc/rc.d/rocksconfig.d
	$(INSTALL) -m700 rocksconfig.d/pre* $(ROOT)/etc/rc.d/rocksconfig.d/
	$(INSTALL) -m700 rocksconfig.d/post* $(ROOT)/etc/rc.d/rocksconfig.d/

	mkdir -p $(ROOT)/etc/profile.d/
	$(INSTALL) -m755 etc/profile.d/*sh $(ROOT)/etc/profile.d/

	mkdir -p $(ROOT)/etc/rc.d/init.d
	$(INSTALL) -m700 init.d/rocks-dmesg $(ROOT)/etc/rc.d/init.d/

clean::
	-rm -f *.spec



