#
# $Id: Makefile,v 1.26 2010/06/22 21:26:22 mjk Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
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
# Revision 1.26  2010/06/22 21:26:22  mjk
# Build env is now from src/devel package, nothing outside of base roll.
#
# Revision 1.25  2009/05/01 19:07:05  mjk
# chimi con queso
#
# Revision 1.24  2008/10/18 00:55:59  mjk
# copyright 5.1
#
# Revision 1.23  2008/08/01 18:47:16  bruno
# nuke 'patch' code
#
# Revision 1.22  2008/03/26 18:24:55  bruno
# another whack at ejecting the CD early
#
# Revision 1.21  2008/03/06 23:41:41  mjk
# copyright storm on
#
# Revision 1.20  2007/12/10 21:28:34  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.19  2007/06/23 04:03:22  mjk
# mars hill copyright
#
# Revision 1.18  2006/12/06 00:20:20  anoop
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
# Revision 1.17  2006/12/02 01:04:53  anoop
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
# Revision 1.16  2006/09/11 22:47:09  mjk
# monkey face copyright
#
# Revision 1.15  2006/08/10 00:09:31  mjk
# 4.2 copyright
#
# Revision 1.14  2006/07/07 20:45:35  bruno
# suppress error at end of install
#
# Revision 1.13  2006/07/06 17:59:38  anoop
# Making check_port more rocks-friendly
#
# Revision 1.12  2006/06/30 18:48:49  anoop
# Added a check_port script to check if a TCP port is open or closed.
#
# Revision 1.11  2006/06/15 21:25:54  bruno
# tweaks for vnc-based installation console
#
# Revision 1.10  2006/06/05 17:57:36  bruno
# first steps towards 4.2 beta
#
# Revision 1.9  2005/10/12 18:08:38  mjk
# final copyright for 4.1
#
# Revision 1.8  2005/10/07 03:09:42  bruno
# add partitions.py to the ekv package
#
# Revision 1.7  2005/09/16 01:02:18  mjk
# updated copyright
#
# Revision 1.6  2005/07/27 01:54:38  bruno
# checkpoint
#
# Revision 1.5  2005/05/24 21:21:53  mjk
# update copyright, release is not any closer
#
# Revision 1.4  2005/04/27 18:26:44  bruno
# added libraries for 'parted' -- this is used for ia64 partitioning
#
# Revision 1.3  2005/03/31 04:47:47  bruno
# suppress ugly warning messages during the recomputation of the package
# ordering
#
# Revision 1.2  2005/03/12 00:01:51  bruno
# minor checkin
#
# Revision 1.1  2005/03/01 02:02:47  mjk
# moved from core to base
#
# Revision 1.48  2005/02/14 21:58:42  bruno
# make sure all the disks are 'bootable' (that is, visible to the kernel)
# before calling the real anaconda.
#
# also, removed an 'echo' statement
#
# Revision 1.47  2004/12/13 14:45:37  bruno
# took away the DHCP and 'activate on boot' option from eth0 and eth1
# for a frontend installation.
#
# Revision 1.46  2004/09/10 01:49:45  bruno
# one small tweak to enable one big release
#
# Revision 1.45  2004/09/03 23:10:56  bruno
# added utility 'make-unbootable-disks'
#
# this is useful during development -- when a node fails during installation,
# you can ssh into a node and run this command. the next time the node boots,
# it will PXE.
#
# Revision 1.44  2004/08/10 17:26:13  bruno
# need the real 'find' command in order to support the '-exec' flag that is
# used when making a new distro during a frontend install
#
# Revision 1.43  2004/05/20 00:17:11  fds
# New sshd needs these libraries in netstg2.
#
# Revision 1.42  2004/04/14 01:55:36  bruno
# add telnet client to ekv
#
# Revision 1.41  2004/03/25 03:15:39  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.40  2003/12/17 01:29:17  bruno
# dear phil,
#
# here is the public/private network messages for the install screens
#
# Revision 1.39  2003/10/21 21:07:44  bruno
# more of last update
#
# Revision 1.38  2003/10/21 21:05:07  bruno
# hdrlist goes in /usr/lib/anaconda for all architectures
#
# Revision 1.37  2003/10/15 22:19:47  bruno
# fixes for taroon
#
# Revision 1.36  2003/10/01 02:11:15  bruno
# fixes for anaconda 9
#
# Revision 1.35  2003/09/24 17:08:45  fds
# Bruno's changes for RH 9
#
# Revision 1.34  2003/09/15 17:50:08  fds
# Builds as root.
#
# Revision 1.33  2003/09/15 17:25:58  fds
# Using python.mk in /etc to find Py version.
#
# Revision 1.32  2003/09/12 22:33:41  fds
# More changes for Opteron.
#
# Revision 1.31  2003/09/12 21:58:01  fds
# Added arch.mk include
#
# Revision 1.28  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.27  2003/05/22 16:39:27  mjk
# copyright
#
# Revision 1.26  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.25  2002/10/29 21:36:04  bruno
# added make-bootable-disks
#
# Revision 1.24  2002/10/18 21:33:26  mjk
# Rocks 2.3 Copyright
#
# Revision 1.23  2002/10/04 05:33:26  mjk
# more rpm target fixes
#
# Revision 1.22  2002/10/03 23:06:08  mjk
# futzed with CVS repository structure
#
# Revision 1.21  2002/06/17 19:50:02  bruno
# 7.3-isms
#
# Revision 1.20  2002/03/07 18:52:51  bruno
# bug fix - wasn't discovering all devices
#
# Revision 1.19  2002/03/01 06:02:58  bruno
# put revision back
#
# Revision 1.18  2002/03/01 06:00:57  bruno
# changed revision
#
# Revision 1.17  2002/02/21 21:33:27  bruno
# added new copyright
#
# Revision 1.16  2001/11/08 18:42:08  mjk
# NPACI Rocks 2.1.1 Release Copyright Notice
#
# Revision 1.15  2001/10/05 16:35:24  bruno
# added 'killall'
#
# Revision 1.14  2001/07/28 23:29:07  bruno
# changes for new patched loader that natively get the ks.cfg with http
#
# Revision 1.13  2001/06/28 22:25:25  bruno
# changed ekv to deal with new watchdog mechanism from 'cluster-config'
#
# Revision 1.12  2001/06/14 22:27:35  bruno
# anaconda now gets ks.cfg with wget calling kickstart.cgi.
#
# damn our shit is cool.
#
# Revision 1.11  2001/06/13 21:23:25  bruno
# changes to get kickstart files via http
#
# Revision 1.10  2001/05/09 20:17:17  bruno
# bumped copyright 2.1
#
# Revision 1.9  2001/04/10 14:16:30  bruno
# updated copyright
#
# Revision 1.8  2001/03/26 22:54:32  bruno
# added 'rocks.py' to figure out what motherboards are SMP enabled
#
# Revision 1.7  2001/03/08 21:51:16  bruno
# bumped revision # for <CR> fix
#
# Revision 1.6  2001/02/14 20:16:33  mjk
# Release 2.0 Copyright
#
# Revision 1.5  2001/01/25 23:22:19  bruno
# new anaconda tweaks
#
# Revision 1.4  2001/01/18 20:07:34  bruno
# bumped version
#
# Revision 1.3  2001/01/12 21:35:29  bruno
# added 'diff' to spec file
#
# Revision 1.2  2000/12/21 18:46:51  bruno
# bumped release number to signify pty-wrapper fixes
#
# Revision 1.1  2000/11/05 23:36:26  bruno
# initial release
#
#

LIB		= lib
CPPFLAGS	= -DVERSION="\"$(VERSION)\""
MAKE.rpmflag	= -bb --define "__spec_install_post :"

PKGROOT		= /
REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../devel/devel
-include $(ROCKSROOT)/etc/Rules.mk
# Need this include for when we build as root.
include Rules.mk

# We need to know about Python locations.
-include $(ROCKSROOT)/etc/python.mk
include python.mk


build:	make-bootable-disks make-unbootable-disks check_port

make-bootable-disks: make-bootable-disks.o
	$(CC) $(CFLAGS) -o$@ $^

make-unbootable-disks: make-unbootable-disks.o
	$(CC) $(CFLAGS) -o$@ $^

#
# add the system utilities which ekv needs and are not provided
# in the standard red hat installation
#
install::
	mkdir -p $(ROOT)/$(PKGROOT)/rocks/bin/
	cp /bin/sleep $(ROOT)/$(PKGROOT)/rocks/bin/
	cp /bin/date $(ROOT)/$(PKGROOT)/rocks/bin/
	cp /sbin/halt $(ROOT)/$(PKGROOT)/rocks/bin/reboot
	cp /usr/bin/tee $(ROOT)/$(PKGROOT)/rocks/bin/
	cp /bin/cpio $(ROOT)/$(PKGROOT)/rocks/bin/
	cp /bin/bash $(ROOT)/$(PKGROOT)/rocks/bin/
	cp /bin/rpm $(ROOT)/$(PKGROOT)/rocks/bin/
	cp /usr/bin/wget $(ROOT)/$(PKGROOT)/rocks/bin/
	cp /bin/gawk $(ROOT)/$(PKGROOT)/rocks/bin/
	cp /bin/stty $(ROOT)/$(PKGROOT)/rocks/bin/
	cp /bin/dd $(ROOT)/$(PKGROOT)/rocks/bin/
	cp /usr/bin/volname $(ROOT)/$(PKGROOT)/rocks/bin/
	cp /usr/bin/killall $(ROOT)/$(PKGROOT)/rocks/bin/
	cp /usr/bin/telnet $(ROOT)/$(PKGROOT)/rocks/bin/
	cp /usr/bin/find $(ROOT)/$(PKGROOT)/rocks/bin/

	cp /usr/sbin/sshd $(ROOT)/$(PKGROOT)/rocks/bin/
	cp /usr/bin/ssh-keygen $(ROOT)/$(PKGROOT)/rocks/bin/

	#
	# ssh needs libutil and libpam. Called /lib64 for Opteron.
	#
	mkdir -p $(ROOT)/$(PKGROOT)/usr/$(LIB)
	cp /$(LIB)/libresolv.so* $(ROOT)/$(PKGROOT)/usr/$(LIB)/
	cp /$(LIB)/libutil* $(ROOT)/$(PKGROOT)/usr/$(LIB)/
	cp /$(LIB)/libpam.so* $(ROOT)/$(PKGROOT)/usr/$(LIB)/
	cp /$(LIB)/security/pam_permit.so $(ROOT)/$(PKGROOT)/usr/$(LIB)/
	cp /usr/$(LIB)/libwrap.so* $(ROOT)/$(PKGROOT)/usr/$(LIB)/

	mkdir -p $(ROOT)/$(PKGROOT)/usr/share/terminfo/v
	$(INSTALL) -m644 /usr/share/terminfo/v/vt100 \
				$(ROOT)/$(PKGROOT)/usr/share/terminfo/v/

	#
	# python files to support the pseudo tty
	#
	mkdir -p $(ROOT)/$(PKGROOT)/usr/sbin
	$(INSTALL) -m755 pty-wrapper.py $(ROOT)/$(PKGROOT)/usr/sbin/

	mkdir -p $(ROOT)/$(PKGROOT)/usr/bin
	$(INSTALL) -m755 anaconda $(ROOT)/$(PKGROOT)/usr/bin/

	#
	# library for 'parted'
	#
	cp /usr/$(LIB)/libreadline* $(ROOT)/$(PKGROOT)/usr/$(LIB)/

	#
	# executable that makes sure all disks are 'bootable'
	#
	cp make-bootable-disks $(ROOT)/$(PKGROOT)/rocks/bin/
	cp make-unbootable-disks $(ROOT)/$(PKGROOT)/rocks/bin/
	
	cp check_port $(ROOT)/$(PKGROOT)/rocks/bin/

	#
	# support files for telnet
	#
	cp /usr/$(LIB)/libncurses.so* $(ROOT)/$(PKGROOT)/usr/$(LIB)/
	cp /usr/$(LIB)/libgpm.so* $(ROOT)/$(PKGROOT)/usr/$(LIB)/


clean::
	rm -f *.o $(EXECS) make-bootable-disks make-unbootable-disks check_port
	rm -f $(SPECFILE).in

