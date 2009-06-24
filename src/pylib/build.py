#! /opt/rocks/bin/python
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
# $Log: build.py,v $
# Revision 1.38  2009/06/24 04:46:12  bruno
# restore roll tweaks
#
# Revision 1.37  2009/05/01 19:07:08  mjk
# chimi con queso
#
# Revision 1.36  2008/12/18 21:41:17  bruno
# add the 'enabled' field to the rolls selection code while building a distro.
#
# Revision 1.35  2008/10/18 00:56:02  mjk
# copyright 5.1
#
# Revision 1.34  2008/05/29 18:06:45  bruno
# add full path to mksquashfs
#
# Revision 1.33  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.32  2007/12/10 21:28:35  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.31  2007/06/23 04:03:24  mjk
# mars hill copyright
#
# Revision 1.30  2007/06/06 17:04:03  bruno
# nuke the "Couldn't find comps package" error message -- in the common case,
# it is a misleading message
#
# Revision 1.29  2006/09/12 21:56:58  bruno
# only apply RPMs from the current distro that is being built.
#
# this is a no-op when there is only a distro from one architecture, but when
# there are multiple architectures (e.g., for 'cross kickstarting'), then
# you want to apply the RPMS from the cross kickstarted distro when the
# 'arch' flag is present.
#
# Revision 1.28  2006/09/11 22:47:22  mjk
# monkey face copyright
#
# Revision 1.27  2006/08/10 00:09:41  mjk
# 4.2 copyright
#
# Revision 1.26  2006/07/19 01:33:27  bruno
# if the file is not an RPM, then just catch the exception
#
# Revision 1.25  2006/07/13 03:56:59  bruno
# make sure the critical RPMs that we build (anaconda, anaconda-runtime,
# kudzu and kudzu-devel) are included from the base roll.
#
# so, if those packages are present from an updated OS CD set and the
# timestamps on those packages are newer than the timestamps on the packages
# in the base roll, then we still will include the base roll packages.
#
# Revision 1.24  2006/06/13 21:48:48  bruno
# now using comps.xml file from native distro
#
# Revision 1.23  2006/06/05 17:57:37  bruno
# first steps towards 4.2 beta
#
# Revision 1.22  2006/01/16 06:48:59  mjk
# fix python path for source built foundation python
#
# Revision 1.21  2005/10/12 18:08:42  mjk
# final copyright for 4.1
#
# Revision 1.20  2005/09/23 04:51:21  bruno
# a workaround in order to build the OS roll
#
# Revision 1.19  2005/09/16 01:02:21  mjk
# updated copyright
#
# Revision 1.18  2005/08/18 22:09:01  bruno
# make torrent files in the resulting 'lan' distro
#
# Revision 1.17  2005/07/27 01:54:38  bruno
# checkpoint
#
# Revision 1.16  2005/07/11 23:51:35  mjk
# use rocks version of python
#
# Revision 1.15  2005/06/30 19:16:17  bruno
# patch netstg2.img in kernel roll, not with rocks-dist.
#
# this means the --public and --notouch flags are gone.
#
# Revision 1.14  2005/05/24 21:21:57  mjk
# update copyright, release is not any closer
#
# Revision 1.13  2005/04/29 01:14:25  mjk
# Get everything in before travel.  Rocks-roll is looking pretty good and
# can now build the os roll (centos with updates).  It looks like only the
# first CDROM of our os/centos roll is needed with 3 extra disks.
#
# - rocks-dist cleanup (tossed a ton of code)
# - rocks-roll growth (added 1/2 a ton of code)
# - bootable rolls do not work
# - meta rolls are untested
# - rocks-dist vs. rocks-roll needs some redesign but fine for 4.0.0
#
# Revision 1.12  2005/04/18 18:43:47  fds
# WAN kickstart authentication requires a different DN from the client than
# on the central's CA.
#
# Revision 1.11  2005/04/14 00:23:53  fds
# Keep it simple. Less throwing around keys.
#
# Revision 1.10  2005/04/01 21:04:49  fds
# Fixed wan distro building on new 4.0 beta frontends.
#
# Revision 1.9  2005/03/25 22:59:23  fds
# Added back boot ISO building. Cleaner and faster than before.
# Also keeping central's crpyto keys in USB key. Used if central is in
# lockdown.
#
# Revision 1.8  2005/03/21 23:46:30  bruno
# everything's a roll support added
#
# Revision 1.7  2005/03/16 20:49:10  fds
# Security and 411 keys on USB drive.
#
# Revision 1.6  2005/03/16 04:44:02  fds
# USB boot key image generator for rocks-dist
#
# Revision 1.5  2005/03/12 00:01:52  bruno
# minor checkin
#
# Revision 1.4  2005/03/10 01:18:21  fds
# Redoing brunos 1.2 diff that got lost. No kickstart-profiles.
#
# Revision 1.3  2005/03/10 00:08:14  fds
# Fix exception when we want to include all rolls, but dont have them
# all listed in the database.
#
# Revision 1.2  2005/03/02 21:19:02  bruno
# don't install rocks-kickstart-profiles -- it doesn't exist anymore
#
# Revision 1.1  2005/03/01 00:22:08  mjk
# moved to base roll
#
# Revision 1.170  2005/02/21 21:22:09  bruno
# now using 'rocks-build' to make all SRPMS
#
# Revision 1.169  2005/02/21 06:42:24  bruno
# the beginning of making a build-rocks.py script
#
# Revision 1.168  2005/01/26 23:09:39  mjk
# Rolls are indexed by name,version,arch.  Last release was just name so
# multiple versions of a roll could not be installed.  Now you can install
# whatever you want.  Rocks-dist keeps track of this in the DB but this
# code does not know about the DB.  For the install environment the
# rocks-dist --with-roll flag can be used inplace of the database.
#
# Revision 1.167  2005/01/18 16:36:08  fds
# rocks-dist mirror tries ftp first, then falls back to http. Now works
# with both ftp.rocksclusters.org, and centrals.
#
# Revision 1.166  2005/01/10 19:30:10  bruno
# netstg2.img is the default.
#
# this assumes we won't be going back to redhat 7.0 anytime soon.
#
# Revision 1.165  2004/11/29 21:14:47  fds
# Commit comment for version 163 got lost
#
# Revision 1.164  2004/11/04 23:52:04  fds
# Tweak
#
# Revision 1.163  2004/11/04 23:37:09  fds
# Support for notouch. Version support for cdrom isos. Build bootdisks.
#
# Revision 1.162  2004/11/03 19:37:09  fds
# Tweak: stay within your mirror tree.
#
# Revision 1.161  2004/11/02 02:11:48  fds
# Working towards bug 62: use http for rocks-dist mirror.
#
# Revision 1.160  2004/10/20 16:29:23  bruno
# set all references to 'ramdisk_size' to 150000
#
# Revision 1.159  2004/10/04 19:20:49  fds
# Uses getArchList to fix bug 25 (opteron installs i386 rolls). Also
# handles rolls with hyphens in name.
#
# Revision 1.158  2004/09/16 19:52:56  fds
# Dont die as easily.
#
# Revision 1.157  2004/09/16 17:35:34  bruno
# so close
#
# Revision 1.156  2004/09/14 19:47:38  bruno
# pretty close to making a working CD
#
# Revision 1.155  2004/08/10 14:37:26  bruno
# first pass at installing a frontend from a distribution that is housed
# on the frontend's local disk.
#
# Revision 1.154  2004/08/10 00:33:11  fds
# Handlers empty mirrors
#
# Revision 1.153  2004/04/28 21:05:44  fds
# Rocks-dist optimization for cross-kickstarting. Do not need the awkward
# --genhdlist flag anymore.
# o Will automatically find the native genhdlist executable, but
# o requires the native dist be made first.
#
# Revision 1.152  2004/04/27 23:50:35  fds
# Fixing rocks-dist cdrom
#
# Revision 1.151  2004/04/14 19:19:42  mjk
# select individual rolls
#
# Revision 1.150  2004/03/25 03:15:47  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.149  2004/03/23 19:46:02  fds
# Tweaks.
#
# Revision 1.148  2004/03/23 19:24:24  fds
# Support for building central roll links.
#
# Revision 1.147  2004/03/18 15:54:13  mjk
# fix patch profiles paths
#
# Revision 1.146  2004/03/16 22:10:33  mjk
# fix profile paths for netstg2
#
# Revision 1.145  2004/03/08 23:26:12  mjk
# - Rolls are off to the side
# - Pristine distribution building
# - Files support chmod
# - Profiles are distribution local
#
# Revision 1.144  2004/03/03 19:36:37  fds
# Changes for cross-kickstarting
#
# Revision 1.143  2004/02/25 17:55:53  bruno
# send error messages from applyRPM to /dev/null.
#
# this is because the intel roll adds a path to the intel libraries and
# everytime ldconfig was called, you see errors like:
#
# /sbin/ldconfig: File /opt/intel_fc_80/lib/libcprts.so is too small, not checked
#
# and the 'expat' package calls ldconfig (and expat is patched into the distro)
#
# Revision 1.142  2004/01/07 22:14:41  bruno
# nuke the code that removed the 'modules' directory on the netstg2.
#
# this caused the ext3 driver to not be loaded and, consequently, a
# user could select ext3 as a file system type.
#
# Revision 1.141  2003/12/10 19:47:53  fds
# Using a real XML parser to manipulate the comps file.
#
# Revision 1.140  2003/11/05 01:17:15  bruno
# moved the netstg2.img inserting into a different part of the cd building
# flow
#
# Revision 1.139  2003/11/05 01:07:34  bruno
# make sure rocks-boot-netstage is on the rocks base CD
#
# Revision 1.138  2003/11/05 00:35:59  bruno
# put in the netstg2.img built by us
#
# Revision 1.137  2003/10/29 00:36:49  mjk
# - Added rebuild lock file (log file locking breaks iteration)
# - All rebuild state goes in spool directory
#
# Revision 1.136  2003/10/29 00:13:43  mjk
# more RHEL changes
#
# Revision 1.135  2003/10/28 23:20:56  mjk
# more RHEL rocks-rebuild changes
#
# Revision 1.134  2003/10/28 20:30:38  mjk
# use product-release name
#
# Revision 1.133  2003/10/27 20:05:00  bruno
# rhel-3
#
# Revision 1.132  2003/10/21 15:44:40  bruno
# removed debug statement
#
# Revision 1.131  2003/10/17 00:01:00  mjk
# get ISOs for beta
#
# Revision 1.130  2003/10/15 22:18:21  bruno
# now can build a bootable taroon-based CD that installs on a frontend
#
# Revision 1.129  2003/10/10 17:44:45  fds
# Redirect comps warnings so they dont annoy us.
#
# Revision 1.128  2003/10/09 00:00:25  fds
# Added expat to patchRPMs list
#
# Revision 1.127  2003/10/08 23:17:29  bruno
# to build CDs under taroon
#
# Revision 1.126  2003/10/07 19:24:44  mjk
# debug prints use --debug flag
#
# Revision 1.125  2003/10/07 18:33:12  fds
# Added support for multiple rpm archs in applyRPM, using the DistRPMList
# exception. Forgive me mjk, but I added another line of output which will
# help in debugging new redhat products.
#
# Revision 1.124  2003/10/06 22:47:14  fds
# Added buildstamp file to allow
# loader to 'verify' the netstg2 image. This string will also be
# used in the boot process in several places.
#
# Revision 1.123  2003/10/01 02:11:15  bruno
# fixes for anaconda 9
#
# Revision 1.122  2003/09/28 23:43:34  fds
# Slightly cleaner.
#
# Revision 1.121  2003/09/28 19:41:27  fds
# Changes for Taroon
#
# Revision 1.120  2003/09/24 17:08:45  fds
# Bruno's changes for RH 9
#
# Revision 1.119  2003/09/12 23:08:18  fds
# Added comps.xml parsing. More Exception handling.
#
# Revision 1.118  2003/09/11 18:56:38  fds
# Introduced BuildError exception, put spinner-cmd into its own function.
#
# Revision 1.117  2003/09/03 00:29:37  bruno
# little tweak
#
# Revision 1.116  2003/09/03 00:27:52  bruno
# building multiple CDs via xml config file
#
# Revision 1.115  2003/09/02 23:37:28  bruno
# flag to make all media set
#
# Revision 1.114  2003/08/28 02:37:07  bruno
# needed comma
#
# Revision 1.113  2003/08/27 23:10:55  mjk
# - copyright update
# - rocks-dist uses getArch() fix the i686 distro bug
# - ganglia-python spec file fixes (bad service start code)
# - found some 80col issues while reading code
# - WAN ks support starting
#
# Revision 1.112  2003/08/26 22:44:20  mjk
# - File tag now takes "expr" attribute (command evaluation)
# - Conversion of old code to file tags
# - Added media-server (used to be server)
# - Killed replace-server on the hpc roll
# - Updated Server database membership (now a media-server)
# - Added Public field to the membership table
# - Insert-ethers only allows a subset of memberships (Public ones) to be
#   inserted.
# - Added getArch() to Application class
# - Kickstart trinity (kcgi,kpp,kgen) all updated self.arch initial value
#
# Revision 1.111  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.110  2003/08/13 22:12:54  mjk
# gingin changes
#
# Revision 1.109  2003/08/13 19:11:22  bruno
# changed media name to 'Rocks Base'
#
# Revision 1.108  2003/07/25 21:18:48  mjk
# - Fixed some files to tab spacing
# - Support rolls on the first CD
# - DVD building fixes
#
# Revision 1.107  2003/07/23 15:59:26  mjk
# - moved all disabled packages to node-thin
# - cdrecord is now less verbose
#
# Revision 1.106  2003/07/21 22:55:25  bruno
# added mini_httpd for rocks-boot building
#
# Revision 1.105  2003/07/19 00:34:09  bruno
# removed patching of CD and hard disk second stage loader
#
# Revision 1.104  2003/07/17 23:08:03  bruno
# pushing towards 2.3.3
#
# Revision 1.103  2003/07/10 15:28:04  bruno
# increased ramdisk size to 100000
#
# Revision 1.102  2003/07/07 20:28:52  bruno
# roll enablers
#
# Revision 1.101  2003/07/07 16:25:07  mjk
# IA64 redux
#
# Revision 1.100  2003/06/30 23:47:16  mjk
# ia64 source distro building changes
#
# Revision 1.99  2003/05/28 17:27:45  mjk
# overflow goes on 2nd CD
#
# Revision 1.98  2003/05/22 16:39:28  mjk
# copyright
#
# Revision 1.97  2003/04/24 16:56:13  mjk
# - Better DFS Graph traversing
# - Adding includes directory for the graph
#
# Revision 1.96  2003/04/03 20:57:03  bruno
# initialize some variables in the 'patch' section -- thanks najib!
#
# Revision 1.95  2003/04/01 00:07:00  mjk
# more mirror changes
#
# Revision 1.94  2003/03/28 20:40:56  bruno
# renamed CD disks to 1,2,3
#
# Revision 1.93  2003/03/28 19:09:27  bruno
# don't remove the 'modules' directory on the second stage loader
# if this is an ia64
#
# Revision 1.92  2003/03/26 20:40:52  bruno
# don't patch the modules into the second stage boot loaders
#
# Revision 1.91  2003/03/22 01:00:55  mjk
# RC 74.3245.32.fds.12
#
# Revision 1.90  2003/03/21 21:27:32  bruno
# mason likes this one
#
# Revision 1.89  2003/03/21 20:46:17  bruno
# mason says this is a good idea
#
# Revision 1.88  2003/02/28 18:43:10  bruno
# another fix to ia64 efi
#
# Revision 1.87  2003/02/28 17:40:32  bruno
# added more functionality to ia64 efi patching
#
# Revision 1.86  2003/02/22 17:39:27  bruno
# fixes to allow patching an ia64 frontend
#
# Revision 1.85  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.84  2003/02/10 22:21:16  bruno
# if the CD size is 0.00, don't print 'CDROM-n : size 0.00'
#
# Revision 1.83  2003/01/25 05:38:49  bruno
# fix to the CD 'backfilling' code
#
# Revision 1.82  2003/01/22 19:16:46  bruno
# code to backfill a CD or DVD
#
# Revision 1.81  2002/12/21 17:10:17  bruno
# fine tune 'patch'
#
# Revision 1.80  2002/12/21 16:56:56  bruno
# more fixes to 'patch'
#
# Revision 1.79  2002/12/21 15:52:14  bruno
# tuned the 'patch' command
#
# Revision 1.78  2002/12/21 02:15:36  bruno
# added grub manipulation to the end of the 'patch' script
#
# Revision 1.77  2002/12/21 02:03:22  bruno
# support for frontend patching -- the 'patch' command
#
# Revision 1.76  2002/12/18 17:40:05  bruno
# now patch hdstg1.img -- this enables patching the frontend from its own
# distribution
#
# Revision 1.75  2002/11/15 21:18:17  mjk
# added --dvd flag
#
# Revision 1.74  2002/11/14 18:50:08  mjk
# added expat parser to pathing image
#
# Revision 1.73  2002/11/07 18:44:01  mjk
# only generate kickstart files once
#
# Revision 1.72  2002/11/06 22:37:40  mjk
# force patch RPMS onto cd1
#
# Revision 1.71  2002/10/29 16:18:23  bruno
# had to take out patching of rocks-boot into the image
#
# Revision 1.70  2002/10/28 20:16:20  mjk
# Create the site-nodes directory from rocks-dist
# Kill off mpi-launch
# Added rocks-backup
#
# Revision 1.69  2002/10/21 22:07:59  mjk
# removed forms from CD
#
# Revision 1.68  2002/10/18 21:33:26  mjk
# Rocks 2.3 Copyright
#
# Revision 1.67  2002/10/18 20:31:31  mjk
# multiple mirror fixes
#
# Revision 1.66  2002/10/18 19:58:40  mjk
# multiple mirror fixes
#
# Revision 1.65  2002/10/18 19:54:35  mjk
# create site-nodes symlink
#
# Revision 1.64  2002/10/18 19:20:11  mjk
# Support for multiple mirrors
# Fixed insert-copyright for new CVS layout
#
# Revision 1.63  2002/10/09 21:05:14  bruno
# we can now build a cdrom again (after source tree reorganization)
#
# Revision 1.62  2002/10/03 20:01:43  mjk
# move everything to /opt/rocks
#
# Revision 1.61  2002/08/31 00:05:04  bruno
# found a bug during 'upgrade' -- the link to /home/install/profiles/nodes
# is there, but since autofs isn't running, it a call to os.path.exist() will
# return false, then the call to os.symlink will throw an exception -- because
# the file is there!
#
# Revision 1.60  2002/07/10 18:54:03  bruno
# changes to make 7.3 installation from CD work
#
# Revision 1.59  2002/07/03 23:33:59  bruno
# added many more packages to the 'patch ekv' section -- now that we build
# the kickstart file on the installing system
#
# Revision 1.58  2002/03/19 23:03:36  bruno
# added multi cdrom building when select 'cdrom'
#
# Revision 1.57  2002/02/26 01:12:52  mjk
# - Remove more of the --cdrom stuff from bruno, thanks to my screwup
# - Added audiofile rpm back the x11 config (gnome needs sound, piece of crap)
# - Burned down a frontend and compute nodes looks pretty good.
#
# Revision 1.56  2002/02/23 00:10:46  bruno
# updates to handle 'negative' packages. the cdrom builder needs them and
# kickstarting nodes don't.
#
# Revision 1.55  2002/02/21 21:33:28  bruno
# added new copyright
#
# Revision 1.54  2002/02/15 21:44:39  mjk
# remove debug lines
#
# Revision 1.53  2002/02/14 02:12:29  mjk
# - Removed CD copy gui code from insert-ethers
# - Added CD copy code back to install.xml (using rocks-dist)
# - Added copycd command to rocks-dist
# - Added '-' packages logic to kgen
# - Other file changed to support above
#
# Revision 1.52  2002/02/12 23:50:34  mjk
# Already forgot
#
# Revision 1.51  2002/02/12 18:40:30  bruno
# nukin' unused code
#
# Revision 1.50  2002/02/12 18:31:47  bruno
# added 'w' to file open for .info file
#
# Revision 1.49  2002/02/12 05:46:10  mjk
# added fixCompFile method
#
# Revision 1.48  2002/02/08 21:58:36  bruno
# made subroutine 'patchImage' because we patch so many damn redhat images.
#
# Revision 1.47  2002/02/07 02:16:59  bruno
# needed to patch stage2.img instead of hdstg1.img for cd install
#
# Revision 1.46  2002/02/06 21:22:44  bruno
# all the little things that releases find ...
#
# Revision 1.45  2002/02/05 22:40:53  mjk
# Red Hat's comps.py file changed to support dependencies.  The hdlist
# packages now supports the select()/unselect()/isSelected() methods --
# they weren't there before.  Changing to method access versus member
# access is good, and it fixed some problems we had with metapackages
# unselecting individual components.
#
# Revision 1.44  2002/02/05 16:43:47  bruno
# added 'deselecting' of packages -- for cdrom support
#
# Revision 1.43  2002/01/18 23:43:27  bruno
# added 'mkcramfs' tool for 7.2
#
# Revision 1.42  2001/11/09 23:50:54  mjk
# - Post release ia64 changes
#
# Revision 1.40  2001/11/08 18:27:21  mjk
# - ia64 vs. i386 cdrom building
#
# Revision 1.39  2001/11/07 19:21:37  mjk
# - moved phpMyAdmin the /var/www/html
# - nuke cluster-config-* as special case rpms in rocks-dist (build.py)
# - moved around code in rocks-boot
# - 2.1.1 copyright
#
# Revision 1.37  2001/11/06 23:30:32  bruno
# cleaned up the information line about where the rocks.iso file is located
#
# Revision 1.36  2001/11/06 22:59:19  bruno
# added fuckin' piece-pipe
#
# Revision 1.35  2001/11/06 22:06:56  bruno
# added mkisofs and isolinux goodies to cdrom building
#
# Revision 1.34  2001/11/05 23:10:18  bruno
# fixed syntax error
#
# Revision 1.33  2001/11/05 22:12:16  bruno
# fixes for 2.1.1
#
# Revision 1.32  2001/11/05 18:36:56  bruno
# more changes for redhat 7.2
#
# Revision 1.31  2001/11/03 00:05:50  bruno
# first steps into 7.2 land
#
# Revision 1.30  2001/10/30 02:59:27  mjk
# left in debug statements
#
# Revision 1.29  2001/10/30 02:17:54  mjk
# - Were cooking with CGI kickstart now
# - added popen stuff to ks.py
# - verify command is dead
#
# Revision 1.28  2001/10/24 20:23:32  mjk
# Big ass commit
#
# Revision 1.26  2001/09/10 18:31:12  mjk
# wish I remembered what changed...
#
# Revision 1.25  2001/07/24 21:11:14  mjk
# Put --ignorearch back in for ekv patching
#
# Revision 1.24  2001/06/27 22:32:17  mjk
# - Added pssh.py module
# - Application now work when the HOME env var is not set
#
# Revision 1.23  2001/06/14 17:19:05  mjk
# - removed --ignorearch flag from ekv-anaconda patching.  Need to by
#   done on the correct arch anyway.
#
# - fixed stage2 filesystem size calculation to allow 20% inode
#   overhead.
#
# Revision 1.22  2001/06/12 18:13:50  mjk
# - Added Force RPMS directory to docs
# - Always create a Force RPMS directory
#
# Revision 1.21  2001/05/29 17:12:21  mjk
# Added verify command support
#
# Revision 1.20  2001/05/23 22:42:25  mjk
# Preserve the force/RPMS dir
#
# Revision 1.19  2001/05/21 22:56:06  mjk
# Remove chroot code.  Back to relocate for RPMs.
#
# Revision 1.18  2001/05/21 19:29:50  mjk
# - Cleanup
# - Don't create symlink for the ekv and piece-pipe packages anymore
#
# Revision 1.17  2001/05/17 16:11:18  bruno
# applyRPM fixes -- i hate redhat
#
# Revision 1.16  2001/05/16 21:44:40  mjk
# - Major changes in CD building
# - Added ip.py, sql.py for SQL oriented scripts
#
# Revision 1.15  2001/05/11 18:12:08  bruno
# cd building
#
# Revision 1.14  2001/05/10 00:04:44  mjk
# Unset LANG for build cdrom
#
# Revision 1.13  2001/05/09 22:33:10  mjk
# - better paths commads
# - more cdrom cleanup
#
# Revision 1.12  2001/05/09 20:50:04  mjk
# Added ekv-anaconda to list of CD rpms
#
# Revision 1.11  2001/05/09 20:17:21  bruno
# bumped copyright 2.1
#
# Revision 1.10  2001/05/07 22:29:14  mjk
# - Release candidate 1
#
# Revision 1.9  2001/05/04 22:58:53  mjk
# - Added 'cdrom' command, and CDBuilder class.
# - CDBuilder uses RedHat's source to parse the hdlist/comps file so we can
#   trim the set of RPMs on our CD.
# - Weekend!
#
# Revision 1.8  2001/05/01 01:02:13  bruno
# added first pass at 'cd_distro' to build the cd-friendly directories.
# it's ugly -- katz, don't kill me.
#
# Revision 1.7  2001/04/27 01:08:50  mjk
# - Created working 7.0 and 7.1 distibutions (in same tree even)
# - Added symlink() method to File object.  Trying to get the File object
#   to make the decision on absolute vs. relative symlinks.  So far we are
#   absolute everywhere.
# - Still missing CD making code.  Need to figure out how to read to
#   comps files using RedHat's anaconda python code.  Then we can decide
#   which RPMs can go on the second CD based on what is required in the
#   kickstart files.
#
# Revision 1.6  2001/04/24 20:59:22  mjk
# - Moved Bruno's eKV 2nd stage patching code over.  And I even understand it.
# - The DistributionBuilder now changes the File object in the distribution as
#   the links, or copies are done.  This means the Tree always reflects what
#   is on the disk, like it should have been in the first place.
# - Added CVS Log from cluster-dist to show the history of the monster
# - Last missing piece is CD building.
#
# Revision 1.5  2001/04/21 01:50:49  mjk
# - Added imortality to files so we can force old RPMS to always be in
#   the distribution.
#
# - Added site/RPMS, site/SRPMS directories for local packages, as in Rocks
#   RPMS.
#
# - Also resolve versions for SRPMS.  The old cluster-dist didn't do this!
#
# - Added DistributionBuilder.applyRPM() method so make patching the
#   dist easier.
#
# - Everything still works fine.  But still missing Bruno's CD and eKV
#   changes.
#
# Revision 1.4  2001/04/20 22:27:02  mjk
# - always apply the genhdlist rpm and run it
# - removed the newdist object from the DistributionBuilder
# - added template for RocksDistributionBuilder
# - Mirror code works
# - Added 'paths' command for learing how to find pathnames
#
# Revision 1.3  2001/04/20 01:53:18  mjk
# - Basic distribution building works.  We now do either all symlink or
# all copies.  The hybrid case wasn't needed and is a big mess-o-code.
#
# - CVS checkout for build directory works
#
# - Need to decide how to add Bruno's changes to cluster-dist back in.
#
# Revision 1.2  2001/04/18 23:17:10  mjk
# - Fixed some low level design bugs in Tree, and Distribution
#
# - The DistributionBuilder can now gather RPMS from all the correct
# sources.  Still need version resolving code the the File and RPMFile
# objects.  Also need to figure how to effeciently traverse this long
# List the RPMFiles.
#
# Revision 1.1  2001/04/18 01:20:38  mjk
# - Added build.py, util.py modules
#
# - Getting closer.  I'm happy with the object model for building
# mirrors, and this will extend well to build the distributions.
#
# - Seriously needs a design document.
#
# Revision 1.1  2001/04/17 02:27:59  mjk
# Time for an initial checkin.  Datastructure and general layout of the
# code is correct.  Still need comparison code for File and RPM objects.
#

import sys
import os
import shutil
import re
import tempfile
import string
import time
import popen2
import xml
import socket
import rocks.dist
import rocks.file
import rocks.ks
import rocks.util


class BuildError(Exception):
	pass


class Builder:
    
	def __init__(self):
        	self.verbose = 0
		self.debug   = 0

	def build(self):
		pass

	def setVerbose(self, level=1):
		self.verbose = level

	def setDebug(self, level=1):
		self.debug = level



class MirrorBuilder(Builder):

	def __init__(self, m):
		Builder.__init__(self)
		self.mirrors	= m

	def build(self):
		for m in self.mirrors:
			dirs = []
			if m.getRemoteReleasePath():
				dirs.append(m.getRemoteReleasePath())
			for dir in dirs:
				self.buildMirror(m.getHost(), dir)


	def buildMirror(self, host, path):
		# Try FTP first, failover to HTTP
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			sock.connect((host, 21))
			sock.close()
        		cmd = 'wget -m -nv ftp://%s//%s/' % (host, path)
		except socket.error:
        		cmd = 'wget -m -nv -np http://%s//%s/' % (host, path)
		sock = None

                if self.verbose or self.debug:
                	print cmd
		if not self.debug:
			os.system(cmd)


#
# this will be copied to the rolls directory to reliably return directory
# listings
#
directory_listing_cgi = """#!/opt/rocks/bin/python

import os

try:
	dir = os.environ['DOCUMENT_ROOT'] + os.environ['REQUEST_URI']
except:
	dir = '.'
	pass

out = ''

out += '<html>'
out += '<body>'
out += '<table>'

for file in os.listdir(dir):
	if file not in [ 'index.cgi' ]:
		out += '<tr><td>\\n'

		if os.path.isdir(os.path.join(dir, file)):
			out += '<a href="%s/">%s/</a>\\n' % (file, file)
		else:
			out += '<a href="%s">%s</a>\\n' % (file, file)

		out += '</td></tr>'
		out += '\\n'

out += '</table>'
out += '</body>'
out += '</html>'

print 'Content-type: text/html'
print 'Content-length: %d' % (len(out))
print ''
print out
"""


class DistributionBuilder(Builder):

    def __init__(self, dist, links=1):
        Builder.__init__(self)
        self.dist		= dist
        self.useLinks		= links
        self.compsPath		= None
	self.useRolls		= {}
	self.allRolls		= 1
	self.onlyRolls		= 0
	self.withSiteProfiles   = 0
	self.version	 = '1.0'

        # Build the Tree objects for the Mirror and Distribution
        # trees.  The actual files for the distibution may or may not
        # exist.  We no longer nuke pre-existing distibutions before
        # building a new one.  This will make mirroring simpler.

        for mirror in self.dist.getMirrors():
            if not mirror.isBuilt():
                mirror.build()

        if not self.dist.isBuilt():
            self.dist.build()


    def setRolls(self, list, only=0):
	    if list:
		    for e in list:
			    self.useRolls[e[0]] = (e[1], e[2])
		    self.allRolls = 0
	    else:
		    self.useRolls = {}
		    self.allRolls = 1
	    self.onlyRolls = only


    def setVersion(self, ver):
    	self.version = ver

    def setSiteProfiles(self, bool):
	    self.withSiteProfiles = bool
	    
    def clean(self):
        # Nuke the previous distribution.  The cleaner() method will
        # preserve any build/ directory.
        print 'Cleaning distribution'
        self.dist.getTree('release').apply(self.cleaner)


    def useRoll(self, key, ver, arch):
    	"Returns true if we should include this roll"

	if arch == self.dist.arch:
		if self.allRolls:
			return 1
		if self.useRolls.has_key(key):
			version, enabled = self.useRolls[key]
			if enabled and version == ver:
				return 1
	return 0


    def getRollBaseFiles(self):
	    files = []
	    for m in self.dist.getMirrors():
		    for key, value in m.getRolls().items():
			    for arch, ver in value:
				    if self.useRoll(key, ver, arch):
					    print '    including "%s" (%s,%s) roll...' % \
						    (key, ver, arch)
					    files.extend(m.getRollBaseFiles(key,
								    ver,
								    arch))
	    return files


    def getRollRPMS(self):
	    rpms = []
	    for m in self.dist.getMirrors():
		    for key, value in m.getRolls().items():
			    for arch, ver in value:
				    if self.useRoll(key, ver, arch):
					    print '    including "%s" (%s,%s) roll...' % \
						    (key, ver, arch)
					    rpms.extend(m.getRollRPMS(key,
								    ver,
								    arch))
	    return rpms


    def getRollSRPMS(self):
	    rpms = []
	    for m in self.dist.getMirrors():
		    for key, value in m.getRolls().items():
			   for arch, ver in value:
				if self.useRoll(key,ver,arch):
					    print '    including "%s" (%s,%s) roll...' % \
						  (key, ver, arch)
					    rpms.extend(m.getRollSRPMS(key,
								       ver,
								       arch))
	    return rpms

    
    def buildRPMSList(self):

	    # Build and resolve the list of RPMS.  Then drop in all
	    # the other non-rpm directories from the Mirror's release.

	    rpms = self.getRollRPMS()
	    for mirror in self.dist.getMirrors():
		    rpms.extend(mirror.getRPMS())
	    if not self.onlyRolls:
	    	rpms.extend(self.dist.getContribRPMS())
	    	rpms.extend(self.dist.getLocalRPMS())
	    if not os.path.isdir(self.dist.getForceRPMSPath()):
		    os.makedirs(self.dist.getForceRPMSPath())
	    else:
		    rpms.extend(self.dist.getForceRPMS()) 
	    return rpms

    
    def buildSRPMSList(self):

	    # Build and resolve the list of SRPMS. 
        
	    rpms = self.getRollSRPMS()
	    for mirror in self.dist.getMirrors():
		    rpms.extend(mirror.getSRPMS())
	    rpms.extend(self.dist.getContribSRPMS())
	    rpms.extend(self.dist.getLocalSRPMS())
	    return rpms


    def buildRollLinks(self):
	"""Links all rolls from our mirrors into rocks-dist/rolls/"""
	
	print "Building Roll Links"
	rollLocation = self.dist.getRollsPath()
	os.system('mkdir -p %s' % rollLocation)

	rolls = []
	for mirror in self.dist.getMirrors():
		rolldir = mirror.getRollsPath()
		if not os.path.exists(rolldir):
			continue
		for d in os.listdir(rolldir):
			rollpath = os.path.join(rolldir,d)
			if os.path.isdir(rollpath):
				rolls.append(rollpath)

	here = os.getcwd()
	os.chdir(rollLocation)
	for r in rolls:
		os.system('ln -sf %s .' % (r))
	os.chdir(here)
	
	
    def buildWANLinks(self, lanbase):
    	"""Links in the stage2.img from lan/"""
    	
    	print "Linking boot stages from lan"
    	wanbase = self.dist.getBasePath()
    	os.system('rm -rf %s' % wanbase)
    	os.system('mkdir -p %s' % wanbase)
    	os.system('ln -s %s/* %s' % (lanbase, wanbase)) 
    	

    def buildBase(self):
        print 'Resolving versions (base files)'
        self.dist.setBaseFiles(self.resolveVersions(self.getRollBaseFiles()))


    def touchCriticalFiles(self, m, key, ver, arch):
	criticalfiles = [ 'anaconda', 'anaconda-runtime',
		'kudzu', 'kudzu-devel' ]

	for rpm in m.getRollRPMS(key,ver,arch):
		try:
			if rpm.getPackageName() in criticalfiles:
				rpm.timestamp = int(time.time())
		except:
			pass


    def includeCriticalRPMS(self):
        print 'Including critical RPMS'

	#
	# there are some standard RPMs that we build in order for our
	# modifcations to the installer to work correctly. this function
	# ensures that the rocks-built standard RPMs are always included
	# and the ones from OS CDs are not.
	#

	for m in self.dist.getMirrors():
		for key, value in m.getRolls().items():
			if key != 'base':
				continue

			for arch, ver in value:
				if self.useRoll(key, ver, arch):
					self.touchCriticalFiles(m,key,ver,arch)
					

    def buildRPMS(self):
        print 'Resolving versions (RPMs)'
        self.dist.setRPMS(self.resolveVersions(self.buildRPMSList()))


    def buildSRPMS(self):
        print 'Resolving versions (SRPMs)'
        self.dist.setSRPMS(self.resolveVersions(self.buildSRPMSList()))


    def insertNetstage(self):
	print 'Applying stage2.img'
	
	cmd = 'rm -f %s/RedHat/base/stage2.img' % (self.dist.getReleasePath())
	os.system(cmd)

	try:
		self.applyRPM('rocks-boot-netstage', self.dist.getReleasePath())
	except:
		print "Couldn't find the package rocks-boot-netstage"
		print "\tIf you are building the OS roll, this is not a problem"
		pass


	print 'Applying updates.img'
	cmd = 'rm -f %s/RedHat/base/updates.img' % (self.dist.getReleasePath())
	os.system(cmd)

	try:
		self.applyRPM('rocks-anaconda-updates',
			self.dist.getReleasePath())
	except:
		print "Couldn't find the package rocks-anaconda-updates"
		print "\tIf you are building the OS roll, this is not a problem"
		pass


	#print 'Applying comps.xml'
	#cmd = 'rm -f %s/RedHat/base/comps.xml' % (self.dist.getReleasePath())
	#os.system(cmd)

	#try:
		#self.applyRPM('comps', self.dist.getReleasePath())

		#cmd = 'cp %s/usr/share/comps/%s/comps.xml %s/RedHat/base/' % \
			#(self.dist.getReleasePath(), self.dist.getArch(),
				#self.dist.getReleasePath())
		#os.system(cmd)
	#except:
		#print "Couldn't find the package 'comps'"
		#print "\tIf you are building the OS roll, this is not a problem"
		#pass

	#
	# the comps package also installs hdlist and hdlist2 -- let's remove
	# those
	#
	#for i in [ 'hdlist', 'hdlist2' ]:
		#cmd = 'rm -f %s/RedHat/base/%s' % \
				#(self.dist.getReleasePath(), i)
		#os.system(cmd)

	return


    def build(self):
		self.clean()
		self.dist.syncMirror()
		self.buildBase()
		self.includeCriticalRPMS()
		self.buildRPMS()
		self.buildSRPMS()

		print 'Creating files',
		if self.useLinks:
			print '(symbolic links - fast)'
		else:
			print '(deep copy - slow)'
		self.dist.getReleaseTree().apply(self.builder)
		self.dist.getReleaseTree().apply(self.normalizer)

		self.insertNetstage()
		self.buildKickstart()
		self.buildProductImg()
		self.createrepo()
		self.makeDirListing()
	
		return


    def buildKickstart(self):
	print 'Installing XML Kickstart profiles'

	build   = self.dist.getBuildPath()

	for rpm in self.dist.getRPMS():
		tok = rpm.getBaseName().split('-')
		if tok[0] != 'roll':
			continue
		try:
			k = tok.index('kickstart')
			rollname = '-'.join(tok[1:k])
		except ValueError:
			continue
			
		print '    installing "%s" profiles...' % rollname
		self.applyRPM(rpm.getBaseName(), build)

	# Copy local profiles into the distribution.
	if self.withSiteProfiles:
		print '    installing "site" profiles...'
		tree = self.dist.getSiteProfilesTree()
		for dir in tree.getDirs():
			for file in tree.getFiles(dir):
				path = os.path.join(build, dir)
				if not os.path.isdir(path):
					os.makedirs(path)
				shutil.copy(file.getFullName(),
					os.path.join(path, file.getName()))
				# make sure apache can read site XML
				file.chmod(0664)


    def applyRPM(self, name, root, flags=''):
        """Used to 'patch' the new distribution with RPMs from the
        distribution.  We use this to always get the correct
        genhdlist, and to apply eKV to Rocks distributions.
        
        Throws a ValueError if it cannot find the specified RPM, and
        BuildError if the RPM was found but could not be installed."""

	rpm = None
	try:
        	rpm = self.dist.getRPM(name)
	except rocks.dist.DistRPMList, e:
		for r in e.list:
			if r.getPackageArch() == self.dist.getArch():
				rpm = r
				break

        if not rpm:
            raise ValueError, "could not find %s" % name

        dbdir = os.path.join(root, 'var', 'lib', 'rpm')
        if not os.path.isdir(dbdir):
            os.makedirs(dbdir)

        reloc = os.system("rpm -q --queryformat '%{prefixes}\n' -p " +
                        rpm.getFullName() + "| grep none > /dev/null")

	cmd = 'rpm -i --ignoresize --nomd5 --force --nodeps --ignorearch '
	cmd += '--dbpath %s ' % dbdir
        if reloc:
	    cmd = cmd + '--prefix %s %s %s' % (root, flags,
					       rpm.getFullName())
        else:
	    cmd = cmd + '--badreloc --relocate /=%s %s %s' % (root, flags,
							      rpm.getFullName())
        retval = os.system(cmd + ' > /dev/null 2>&1')

        shutil.rmtree(os.path.join(root, 'var'))
		
        if retval == 256:
            raise BuildError, "could not apply RPM %s" % (name)

        return retval


    def buildProductImg(self):
	#
	# the directory where the python files exist that are used to
	# extend anaconda
	#
	product = '../../images/product.img'
	productfilesdir = os.path.join(self.dist.getBuildPath(), 'include')

	if not os.path.exists(productfilesdir):
		#
		# there are no 'product' files, so there's nothing to do.
		# let's just return
		#
		return

	cwd = os.getcwd()
	os.chdir(productfilesdir)

	if not os.path.exists('../../images'):
		os.makedirs('../../images')

	os.system('rm -f %s' % (product))
	cmd = '/sbin/mksquashfs installclass/*py installclasses %s ' % (product)
	cmd += '-keep-as-directory > /dev/null 2>&1'
	os.system(cmd)

	if os.path.exists(product):
		#
		# on a server installation (e.g., frontend), mksquashfs
		# fails, but it is not important that product.img is built
		# during the installation. product.img was already downloaded
		# off the CD, so it will not be needed for the remainder of
		# the server installation.
		#
		os.chmod(product, 0666)

	os.chdir(cwd)
	return


    def createrepo(self):
	print 'Creating repository'

	cwd = os.getcwd()
	releasedir = self.dist.getReleasePath()
	os.chdir(releasedir)

	#
	# make sure the cache directory exists
	#
	cachedir = os.path.join(self.dist.getRootPath(), 'cachedir')
	if not os.path.exists(cachedir):
		os.makedirs(cachedir)

	#
	# first check in the install environment (/tmp/updates), then
	# look in the 'normal' place (on a running frontend).
	#
	createrepo = '/tmp/updates/usr/share/createrepo/genpkgmetadata.py'
	if not os.path.exists(createrepo):
		createrepo = '/usr/share/createrepo/genpkgmetadata.py'

	os.system('%s ' % (createrepo) + 
		'--groupfile %s/RedHat/base/comps.xml ' % (releasedir) + 
		'--cachedir %s --quiet .' % (cachedir))

	os.chdir(cwd)

	return


    def makeDirListing(self):	
	#
	# make sure a known CGI exists in the roll directory so we can
	# reliably list all the rolls present on a system. this is useful
	# when the directory listing output is different between different
	# web servers
	#
	path = os.path.join(self.dist.getRootPath(), 'rolls')
	if os.path.exists(path):
		filename = os.path.join(path, 'index.cgi')

		file = open(filename, 'w')
		file.write('%s' % (directory_listing_cgi))
		file.close()

		os.chmod(path, 755)
		os.chmod(filename, 755)

	return


    def cleaner(self, path, file, root):
        if not root:
            root = self.dist.getReleasePath()
        dir = os.path.join(root, path)
        if dir not in [ self.dist.getForceRPMSPath() ]:
            os.unlink(os.path.join(dir, file.getName()))

    def builder(self, path, file, root):
        if not root:
            root = self.dist.getReleasePath()
        dir	 = os.path.join(root, path)
        fullname = os.path.join(dir, file.getName())

        if file.getFullName() == fullname:
            return

        if not os.path.isdir(dir):
            os.makedirs(dir)

        # Create the new distribution either with all symbolic links
        # into the mirror, contrib, and local rpms.  Or copy
        # everything.  The idea is local distributions should be all
        # symlinks, but a published base distribution (like the NPACI
        # Rocks master) should be copys.  This keeps the FTP chroot
        # environment happy, extends the lifetime of the release past
        # that of scattered RPMS.  It may also make sense to have your
        # master distribution for your cluster done by copy.
        
        if self.useLinks:
            file.symlink(fullname, self.dist.getRootPath())
        else:

            # For copied distributions, the timestamps of the new
            # files are forced to that of the source files.  This
            # keeps wget happy.

            if os.path.islink(file.getFullName()):
                os.symlink(os.readlink(file.getFullName()), fullname)
            else:
                shutil.copy(file.getFullName(), fullname)
                os.utime(fullname, (file.getTimestamp(), file.getTimestamp()))

    def normalizer(self, path, file, root):
        if not root:
            root = self.dist.getReleasePath()
        dir	 = os.path.join(root, path)
        fullname = os.path.join(dir, file.getName())

        # Reset the File to represent the one we just created in the new
        # distribution.
        
        if file.getFullName() != fullname:
            file.setFile(fullname)

    def resolveVersions(self, files):

        # Use a dictionary (hash table) to find and resolve all the
        # version conflict in the list of files.  We use a dictionary
        # to avoid an O(n) list based approach.  Burn memory, save
        # time.

        dict = {}
        for e in files:
            name = e.getUniqueName() # name w/ arch string appended
            if not dict.has_key(name) or e >= dict[name]:
                dict[name] = e

        # Extract the File objects from the dictionary and return
        # them as a list.
        
        list = []
        for e in dict.keys():
            list.append(dict[e])
        return list

    def setComps(self, path):
    	self.compsPath = path
    	

class USBBuilder(DistributionBuilder):
	"Builds a filesytem image for a Bootable USB Key."
	
	dn = '/CN=anonymous'

	def build(self, dn=None, size=20000):
		"""Assumes a valid rocks-dist, will throw an 
		exception if missing. Size is number of blocks (1block = 1KB)
		in the filesystem."""
		
		print 'Creating Bootable USB filesystem ...'

		if dn:
			self.dn = dn
		cd = os.path.normpath(
			os.path.join(self.dist.getReleasePath(), '..'))
		thisdir = os.path.join(cd,'usb-key')
		os.system('mkdir -p %s' % thisdir)
		os.chdir(thisdir)
		
		self.applyRPM('rocks-boot-cdrom', thisdir)
		os.system('/sbin/mkfs.vfat -C usb.img '
			+ '-n "Rocks USB Boot" %s > /dev/null' % size)
		os.system('rm -rf key-img')
		os.system('mkdir -p key-img')
		os.system('mount -o loop usb.img key-img')
		os.system('cp -a isolinux/* key-img/')
		os.rename('key-img/isolinux.cfg','key-img/syslinux.cfg')
		os.system('touch key-img/rocks-usbkey')
		try:
			self.writeKeys('key-img')
		except Exception, msg:
			print 'warning - could not find key: %s' % msg
		os.system('umount key-img')
		os.system('/usr/bin/syslinux usb.img')
		imgname = 'rocks-usb-%s.%s.img' %  \
				(self.version, self.dist.getArch())
		imgpath = os.path.join(cd,imgname)
		os.rename('usb.img', imgpath)
		os.chmod(imgpath,0444)
		os.system('rm -rf %s' % thisdir)
			
		print "Wrote:", imgpath
		print "Copy this image directly onto a usb key: "
		print " # dd < %s > /dev/sda" % imgname
		
		
	def writeKeys(self, root):
		"Copy essential cluster keys to usb drive"

		os.system('mkdir -p %s/security/server' % root)
		os.system('mkdir -p %s/security/client' % root)
		self.newCert('%s/security' % root)
		
		# For Server: our CA and 411 master.
		ca = '/etc/security/ca'
		for k in ('ca.crt','ca.key','ca.serial'):
			shutil.copy(os.path.join(ca,k), 
				'%s/security/server/' % root)

		# sacerdoti: The 411 shared key is saved for the frontend,
		# so 411 and the CA can be recovered a catastrophe (disk or node
		# destroyed. Computes never need the shared 411 key, since
		# it is in the kickstart file.  The 411 master public key is
		# always generated from the private key.

		shutil.copy('/etc/411-security/master.key', 
			'%s/security/server/411-master.key' % root)

		shutil.copy('/etc/411-security/shared.key', 
			'%s/security/server/411-shared.key' % root)	
			
		# Keep central's keys if we installed over WAN.
		for k in ('ca.crt','cert.crt','cert.key'):
			try:
				shutil.copy('/etc/security/cluster-%s' % k, 
					'%s/security/server' % root)
			except IOError:
				pass

		# Everyone
		shutil.copy('%s/ca.crt' % ca, 
			'%s/security/cluster-ca.crt' % root)
		
		
	def newCert(self, root):
		"""Generates a Certificate signed by our CA, for use
		by compute nodes to prove their membership in the cluster."""
		
		ca = '/etc/security/ca'
		
		print ' Making new certificate keypair'
		
		cwd = os.getcwd()
		os.chdir(root)
		
		cmd = ('/usr/bin/openssl req -new -nodes '
			+ '-config %s/ca.cfg -batch -subj "%s" ' % (ca, self.dn)
			+ '-keyout cluster-cert.key > cert.csr 2> /dev/null')
		os.system(cmd)
		os.chmod('cluster-cert.key',0400)
		
		print ' Signing the certificate with our CA'
		
		cmd = ('/usr/bin/openssl x509 -req -days 1000 '
			+ '-CA %s/ca.crt -CAkey %s/ca.key -CAserial %s/ca.serial ' 
				% (ca, ca, ca)
			+ ' < cert.csr > cluster-cert.crt 2> /dev/null')
		os.system(cmd)
		os.chmod('cluster-cert.crt', 0444)
		os.unlink('cert.csr')
		
		os.chdir(cwd)
		return

