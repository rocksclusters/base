#! @PYTHON@
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
# $Log: rocks-dist.py,v $
# Revision 1.48  2008/03/06 23:41:41  mjk
# copyright storm on
#
# Revision 1.47  2008/02/13 01:20:05  anoop
# rocks-dist now can handle the additional os column in the rolls table
# when creating distribution
#
# Revision 1.46  2007/12/10 21:28:34  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.45  2007/06/23 04:03:21  mjk
# mars hill copyright
#
# Revision 1.44  2007/05/11 21:17:25  bruno
# timestamp is now a flag when building torrent files
#
# Revision 1.43  2006/12/19 22:20:32  bruno
# make torrent files with the rocks command line
#
# Revision 1.42  2006/11/30 00:38:20  bruno
# make sure to copy the comps RPMS from rolls
#
# Revision 1.41  2006/09/11 22:47:08  mjk
# monkey face copyright
#
# Revision 1.40  2006/09/08 18:30:42  bruno
# if the database is up, dynamically get the versions of the kernel and
# base roll in order to build the wan distro correctly. if the database is
# not accessible, use the version number that is compiled into rocks-dist.
#
# Revision 1.39  2006/08/10 00:09:31  mjk
# 4.2 copyright
#
# Revision 1.38  2006/06/26 22:49:36  bruno
# make sure the permissions on the rolls directories are always traversable
# by all
#
# Revision 1.37  2006/06/23 18:01:54  bruno
# update paths to new rolls directory
#
# Revision 1.36  2006/06/23 17:04:36  anoop
# Fixes permissions for all directories under /export/home/install/rolls
#
# Revision 1.35  2006/06/22 23:36:09  anoop
# Removed the mirror command from rocks-dist
#
# Revision 1.34  2006/06/21 03:09:53  bruno
# updates to put the frontend networking info in the database just like
# a compute node
#
# Revision 1.33  2006/06/13 21:48:48  bruno
# now using comps.xml file from native distro
#
# Revision 1.32  2006/06/05 17:57:36  bruno
# first steps towards 4.2 beta
#
# Revision 1.31  2006/06/01 01:11:19  anoop
# Changed rocks-dist to not report an error if unlinking of the rocks-file fails
# Also removed yum code from rocks-dist.
# Changed graph generation to generate jpeg rather than gif of default size approx. 6000*700 pixels
#
# Revision 1.30  2006/05/03 18:08:43  anoop
# Minor bug fix
#
# Revision 1.29  2006/05/01 20:38:51  anoop
# Added code to create the yum header repository if the xen roll is present
#
# Revision 1.28  2006/01/16 06:48:58  mjk
# fix python path for source built foundation python
#
# Revision 1.27  2005/10/12 18:08:37  mjk
# final copyright for 4.1
#
# Revision 1.26  2005/09/16 01:02:17  mjk
# updated copyright
#
# Revision 1.25  2005/09/15 22:08:40  bruno
# don't run insert-ethers until rocks-dist completes
#
# Revision 1.24  2005/09/02 00:05:49  bruno
# pushing toward 4.1 beta
#
# Revision 1.23  2005/08/19 05:44:20  bruno
# final touches on bittorrent code
#
# Revision 1.22  2005/08/18 22:09:01  bruno
# make torrent files in the resulting 'lan' distro
#
# Revision 1.21  2005/07/11 23:51:34  mjk
# use rocks version of python
#
# Revision 1.20  2005/06/30 19:16:17  bruno
# patch netstg2.img in kernel roll, not with rocks-dist.
#
# this means the --public and --notouch flags are gone.
#
# Revision 1.19  2005/05/26 01:42:11  fds
# Fixed rolls table delete
#
# Revision 1.18  2005/05/24 21:21:53  mjk
# update copyright, release is not any closer
#
# Revision 1.17  2005/05/23 23:59:23  fds
# Frontend Restore
#
# Revision 1.16  2005/04/29 01:14:25  mjk
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
# Revision 1.15  2005/04/18 18:46:45  fds
# WAN kickstart authentication requires a different DN from the client than
# on the central's CA. Relevant for USB key certs.
#
# Revision 1.14  2005/04/01 21:04:49  fds
# Fixed wan distro building on new 4.0 beta frontends.
#
# Revision 1.13  2005/03/31 06:22:09  bruno
# need the 'short' flag for the cp that is in the install environment
#
# Revision 1.12  2005/03/31 05:00:38  bruno
# foreign roll tuning
#
# Revision 1.11  2005/03/30 15:27:25  bruno
# make sure timestamps are preserved for foreign rolls
#
# Revision 1.10  2005/03/29 23:18:43  fds
# Added --clean flag to copyroll. Used for development.
#
# Revision 1.9  2005/03/25 23:00:49  fds
# Added bootiso command
#
# Revision 1.8  2005/03/25 02:19:24  bruno
# more files that we don't want from foreign rolls
#
# Revision 1.7  2005/03/25 01:55:58  bruno
# don't bring over anaconda packages from foreign rolls
#
# Revision 1.6  2005/03/24 22:45:01  bruno
# added code to:
# - correctly look at the 'enabled' field when building rolls
# - make sure the directory permissions are correct in the mirror when
#   executing copyroll
# - take a 'foreign' piece of media and make it look like a rocks roll
#
# Revision 1.5  2005/03/21 23:46:29  bruno
# everything's a roll support added
#
# Revision 1.4  2005/03/16 04:44:01  fds
# USB boot key image generator for rocks-dist
#
# Revision 1.3  2005/03/16 04:02:51  fds
# More durable to schema change with this style inserts.
#
# Revision 1.2  2005/03/12 00:01:51  bruno
# minor checkin
#
# Revision 1.1  2005/03/01 02:02:47  mjk
# moved from core to base
#
# Revision 1.113  2005/02/10 23:27:44  fds
# connect does not throw an exception.
#
# Revision 1.112  2005/01/31 23:58:22  mjk
# don't rerun rocks-dist dist on copyroll
#
# Revision 1.111  2005/01/26 23:07:25  mjk
# - Now an SQL application, but still works w/o it
# - Rolls installed go into DB
# - Rolls can be enabled or disabled in the DB
# - Copyroll does a bunch of SQL stuff now
# - Rolls are indexed by name,version,arch (previously just name)
#
# Revision 1.110  2004/11/29 21:13:24  fds
# public and notouch flags merged. public has original meaning. Tricker to
# merge than readily apparent.
#
# Revision 1.109  2004/11/05 18:59:18  mjk
# Last two versions first changed and then removed the --public flag that
# is used by other pieces of Rocks.  Back out of these two changes and
# try again.
# Revision 1.108  2004/11/04 23:36:21  fds
#
# No more --public. New --notouch option means dont rebuild or touch the
# netstg.img and others.
#
# Revision 1.107  2004/11/03 23:18:28  fds
# Keep build dir on --public so we can make ks files.
#
# Revision 1.106  2004/11/03 19:37:35  fds
# More precise copyroll. Enables rolls on the base media.
#
# Revision 1.105  2004/11/02 02:11:48  fds
# Working towards bug 62: use http for rocks-dist mirror.
#
# Revision 1.104  2004/11/02 00:35:06  fds
# for bug 70. Fix for --path=
#
# Revision 1.103  2004/08/25 21:52:04  fds
# Cleaner copyroll command. Will work with any and meta rolls.
#
# Revision 1.102  2004/08/25 05:25:40  bruno
# move from ssh v1 to ssh v2
#
# (bug 17)
#
# Revision 1.101  2004/08/19 20:14:51  fds
# Support for any/metarolls. Roll interface 2.0
#
# Revision 1.100  2004/08/11 19:03:08  fds
# --path= option for Greg.
#
# Revision 1.99  2004/08/10 00:33:00  fds
# Handles multiple mirrors better
#
# Revision 1.98  2004/07/27 21:19:55  fds
# rocks-dist/wan permissions opened just
# enough to allow apache to create per-client access dirs.
#
# Revision 1.97  2004/07/15 18:26:02  fds
# Missed this piece.
#
# Revision 1.96  2004/07/14 23:13:02  fds
# dist2mirror fixed, cmdline mirror defs supported. Rocks-distrc won't
# get blown away every time you update this package.
#
# Revision 1.95  2004/07/07 16:36:03  mjk
# - Rolls in dist (wan/lan) not fully tested
# - This matches to FDS changes for wan-kickstart
# - Nuked some unused commands
#
# Oh no where did our 3.2 bridge go, all I see are flames.
# Burn burn burn!
#
# Revision 1.94  2004/05/25 01:51:50  fds
# Multiple mirror support for rocks-dist parser.
#
# Revision 1.93  2004/05/19 21:01:20  fds
# Fixes a subtle bug that causes Rocks base mirror to fail when a package
# has changed on central. Basically forces Apache to dynamically generate
# the index.html like we expect.
#
# Revision 1.92  2004/04/30 00:22:35  fds
# You will not always be in /home/install for copyroll
#
# Revision 1.91  2004/04/28 04:06:26  bruno
# make sure rebuild directory structure is absolute and not relative to current
# working directory
#
# Revision 1.90  2004/04/27 23:50:34  fds
# Fixing rocks-dist cdrom
#
# Revision 1.89  2004/04/22 14:34:09  mjk
# phat phingerz
#
# Revision 1.88  2004/04/22 14:31:44  mjk
# new kpp dot options
#
# Revision 1.87  2004/04/20 03:29:49  fds
# Copyroll is much simpler. Moved the roll-name.xml parsing into dist.py.
# Will help with multiple mirrors, and keeps all path manipulations in dist
# class.
#
# Revision 1.86  2004/04/14 23:17:42  fds
# Fixing central target
#
# Revision 1.85  2004/04/14 21:29:12  mjk
# fix pristine again
#
# Revision 1.84  2004/04/14 19:28:39  mjk
# added the option
#
# Revision 1.83  2004/04/14 19:19:49  mjk
# select individual rolls
#
# Revision 1.82  2004/03/25 03:15:36  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.81  2004/03/24 21:34:54  fds
# mjk had it almost right. The += stuff is for clarity. We are programming in Python 2.2 now.
#
# Revision 1.80  2004/03/24 15:01:08  fds
# mjk is right, central command is simpler.
#
# Revision 1.79  2004/03/24 00:30:08  fds
# Roll info file not always right in front of us.
#
# Revision 1.78  2004/03/23 19:22:22  fds
# New central command makes rolls link.
#
# Revision 1.77  2004/03/20 03:51:23  fds
# Tweaks.
#
# Revision 1.76  2004/03/20 03:39:16  fds
# Copyroll command. This reads the roll-name.xml file to get roll arch, etc.
# Also moved copycd and copyroll method bodies to all-tab indents because it
# was driving me crazy.
#
# Revision 1.75  2004/03/09 23:51:40  mjk
# added graph command
#
# Revision 1.74  2004/03/08 23:26:46  mjk
# Added --pristine flag
#
# Revision 1.73  2004/03/03 19:31:57  fds
# Push ugly stuff into dist, tools are cleaner.
#
# Revision 1.72  2004/03/02 00:42:36  mjk
# cleaner try block
#
# Revision 1.71  2004/03/02 00:38:33  mjk
# added paths try blocks
#
# Revision 1.70  2004/02/24 02:22:46  fds
# Command cleanexternal renamed to dist2mirror, and
# improved to be closer to a true mapping function (computable).
#
# Revision 1.69  2004/02/12 00:40:20  fds
# For WAN Kickstart
#
# Revision 1.68  2004/02/02 18:39:09  fds
# Allow a more flexible copycd cmd, suitable for wan kickstart.
#
# Revision 1.67  2003/10/22 21:29:47  fds
# Copy CD respects distArch.
#
# Revision 1.66  2003/10/16 20:22:13  fds
# Handling distArch for opteron.
#
# Revision 1.65  2003/10/15 22:19:46  bruno
# fixes for taroon
#
# Revision 1.64  2003/09/04 17:37:49  fds
# Fixed RC file value ordering, and null option attributes.
#
# Revision 1.63  2003/09/03 00:27:52  bruno
# building multiple CDs via xml config file
#
# Revision 1.62  2003/09/02 23:37:28  bruno
# flag to make all media set
#
# Revision 1.61  2003/09/02 23:30:14  bruno
# make the whole media set
#
# Revision 1.60  2003/08/27 23:10:55  mjk
# - copyright update
# - rocks-dist uses getArch() fix the i686 distro bug
# - ganglia-python spec file fixes (bad service start code)
# - found some 80col issues while reading code
# - WAN ks support starting
#
# Revision 1.59  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.58  2003/08/13 22:11:35  mjk
# gingin changes
#
# Revision 1.57  2003/08/11 20:48:22  mjk
# *** empty log message ***
#
# Revision 1.56  2003/07/25 21:18:10  mjk
# ia64 rolls
#
# Revision 1.55  2003/07/07 22:20:50  bruno
# neuvo
#
# Revision 1.54  2003/07/07 16:25:07  mjk
# IA64 redux
#
# Revision 1.53  2003/06/27 22:27:42  mjk
# ia64 enterprise edition support
#
# Revision 1.52  2003/05/22 16:39:27  mjk
# copyright
#
# Revision 1.51  2003/04/02 17:57:38  bruno
# copycd now preserves timestamps -- thanks najib
#
# Revision 1.50  2003/04/01 00:07:00  mjk
# more mirror changes
#
# Revision 1.49  2003/03/31 22:35:52  mjk
# fixed ftp mirror
#
# Revision 1.48  2003/03/28 23:22:06  mjk
# fix contrib
#
# Revision 1.47  2003/03/28 19:05:07  mjk
# put release in contrib path
#
# Revision 1.46  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.45  2003/02/13 16:36:03  bruno
# can now copy multiple CDs into the mirror
#
# Revision 1.44  2003/02/11 17:10:45  bruno
# increased cdrom size to 650MB
#
# Revision 1.43  2003/01/31 00:02:43  fds
# Now lists available commands on --help.
#
# Revision 1.42  2003/01/22 19:16:46  bruno
# code to backfill a CD or DVD
#
# Revision 1.41  2002/12/21 02:03:02  bruno
# support for 'patch' -- the frontend patch command
#
# Revision 1.40  2002/11/15 21:24:16  mjk
# switched to dvd command
#
# Revision 1.39  2002/11/15 21:18:04  mjk
# added --dvd flag
#
# Revision 1.38  2002/10/28 20:16:20  mjk
# Create the site-nodes directory from rocks-dist
# Kill off mpi-launch
# Added rocks-backup
#
# Revision 1.37  2002/10/18 21:33:26  mjk
# Rocks 2.3 Copyright
#
# Revision 1.36  2002/10/18 20:32:16  mjk
# multiple mirror fixes
#
# Revision 1.35  2002/10/18 19:20:11  mjk
# Support for multiple mirrors
# Fixed insert-copyright for new CVS layout
#
# Revision 1.34  2002/09/03 20:43:00  bruno
# had to put a try/except guard around rmtree()
#
# Revision 1.33  2002/08/30 23:42:31  bruno
# remove the tree in the mirror before we copy the contents of the CD
# down onto the disk.
#
# Revision 1.32  2002/05/15 18:57:09  bruno
# removed hard-coded 'arch' -- now programmatically determine it
#
# Revision 1.31  2002/02/25 22:43:23  mjk
# - Removed --sdsc flag from rocks-dist
# - Changed ganglia xml file to new RPMS
#
# Revision 1.30  2002/02/21 21:33:28  bruno
# added new copyright
#
# Revision 1.29  2002/02/16 00:04:12  mjk
# Use rocks-dist to create /home/install/contrib directories
#
# Revision 1.28  2002/02/14 23:11:45  mjk
# - Changed -x to -e test in install.xml for cdrom device
# - Fixed insert-ethers bad gui
# - Fixed copycd command
#
# Revision 1.27  2002/02/14 02:12:29  mjk
# - Removed CD copy gui code from insert-ethers
# - Added CD copy code back to install.xml (using rocks-dist)
# - Added copycd command to rocks-dist
# - Added '-' packages logic to kgen
# - Other file changed to support above
#
# Revision 1.26  2002/02/12 23:48:36  mjk
# - Added copycd command
#
# Revision 1.25  2002/02/12 21:43:59  bruno
# always patch ekv
#
# Revision 1.24  2002/02/12 05:45:58  mjk
# added genhdlist command
#
# Revision 1.23  2002/02/06 21:22:44  bruno
# all the little things that releases find ...
#
# Revision 1.22  2001/11/06 22:12:10  bruno
# added ISO building to cdrom
#
# Revision 1.21  2001/10/30 02:18:27  mjk
# - killed off verify command
# - killed off server RPM
#
# Revision 1.20  2001/10/24 20:23:32  mjk
# Big ass commit
#
# Revision 1.19  2001/05/29 17:12:41  mjk
# Added Verify command
#
# Revision 1.18  2001/05/21 19:30:11  mjk
# Cleanup
#
# Revision 1.17  2001/05/16 21:48:14  mjk
# Bumped version number
#
# Revision 1.16  2001/05/14 22:35:45  bruno
# cd building fixes
#
# Revision 1.15  2001/05/09 22:33:10  mjk
# - better paths commads
# - more cdrom cleanup
#
# Revision 1.14  2001/05/09 20:17:21  bruno
# bumped copyright 2.1
#
# Revision 1.13  2001/05/08 21:08:23  mjk
# --sdsc was coded backwards (don't know when this happened)
#
# Revision 1.12  2001/05/04 22:58:53  mjk
# - Added 'cdrom' command, and CDBuilder class.
# - CDBuilder uses RedHat's source to parse the hdlist/comps file so we can
#   trim the set of RPMs on our CD.
# - Weekend!
#
# Revision 1.11  2001/05/01 01:02:13  bruno
# added first pass at 'cd_distro' to build the cd-friendly directories.
# it's ugly -- katz, don't kill me.
#
# Revision 1.10  2001/04/27 01:08:50  mjk
# - Created working 7.0 and 7.1 distibutions (in same tree even)
# - Added symlink() method to File object.  Trying to get the File object
#   to make the decision on absolute vs. relative symlinks.  So far we are
#   absolute everywhere.
# - Still missing CD making code.  Need to figure out how to read to
#   comps files using RedHat's anaconda python code.  Then we can decide
#   which RPMs can go on the second CD based on what is required in the
#   kickstart files.
#
# Revision 1.9  2001/04/24 20:59:22  mjk
# - Moved Bruno's eKV 2nd stage patching code over.  And I even understand it.
# - The DistributionBuilder now changes the File object in the distribution as
#   the links, or copies are done.  This means the Tree always reflects what
#   is on the disk, like it should have been in the first place.
# - Added CVS Log from cluster-dist to show the history of the monster
# - Last missing piece is CD building.
#
# Revision 1.8  2001/04/21 01:50:49  mjk
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
# Revision 1.7  2001/04/20 22:27:02  mjk
# - always apply the genhdlist rpm and run it
# - removed the newdist object from the DistributionBuilder
# - added template for RocksDistributionBuilder
# - Mirror code works
# - Added 'paths' command for learing how to find pathnames
#
# Revision 1.6  2001/04/20 01:53:18  mjk
# - Basic distribution building works.  We now do either all symlink or
# all copies.  The hybrid case wasn't needed and is a big mess-o-code.
#
# - CVS checkout for build directory works
#
# - Need to decide how to add Bruno's changes to cluster-dist back in.
#
# Revision 1.5  2001/04/18 23:17:10  mjk
# - Fixed some low level design bugs in Tree, and Distribution
#
# - The DistributionBuilder can now gather RPMS from all the correct
# sources.  Still need version resolving code the the File and RPMFile
# objects.  Also need to figure how to effeciently traverse this long
# List the RPMFiles.
#
# Revision 1.4  2001/04/18 02:17:36  mjk
# All objects now know how to dump(), so we can debug the mirror and
# distribution datastructres.
#
# Revision 1.3  2001/04/18 01:32:44  mjk
# Command processing done through eval().  Very cool trick.
#
# Revision 1.2  2001/04/18 01:20:38  mjk
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
# Rocks-dist is a re-write of cluster-dist.  It grew too complex for us too
# keep hacking at it.  Here is the CVS log from cluster-dist.
#
# Revision 1.44  2001/04/10 14:16:28  bruno
# updated copyright
#
# Revision 1.43  2001/04/09 21:58:33  mjk
# First pass at fixing for RedHat's new tree
#
# Revision 1.42  2001/03/29 23:55:54  bruno
# cleanup disk1/build directory when a CD is built (--cd) flag
#
# Revision 1.41  2001/02/22 22:14:10  mjk
# Fixed comps file not getting picked up into FTP distribution.
#
# Revision 1.40  2001/02/17 06:41:13  mjk
# Packages are now installed with the following priority
#
# - local
# - contrib
# - stock
# - updates
#
# This was needed to force the lastest local RPMS to be picked up even
# when the developer is too lazy to bump the version number.
#
# Revision 1.39  2001/02/17 00:10:52  mjk
# Give contrib dir priority
#
# Revision 1.38  2001/02/15 01:17:53  bruno
# fix katz's dyslexia
#
# Revision 1.37  2001/02/14 20:16:31  mjk
# Release 2.0 Copyright
#
# Revision 1.36  2001/02/14 17:53:21  mjk
# - Bumped version to 2.0 for release
# - Change defaults in script and .rc files to 7.0
#
# Revision 1.35  2001/02/06 18:02:20  bruno
# added "--cd" which makes CD friendly directories inside the distro
#
# Revision 1.34  2001/02/05 05:55:38  mjk
# - Allow multiple RedHat versions in the same tree.  This was supposed to
#   work in the first place, but I messed it up.
# - Stop creating the RPMS and RPMS directories of the rocks packages
#   when using the --norocks flags.
#
# Revision 1.33  2001/02/05 05:29:56  mjk
# - Added --norocks for generic distributions.
# - Man this is a crappy X-Files...
#
# Revision 1.32  2001/02/05 05:11:13  mjk
# Added preview directory to skip list for mirror building
#
# Revision 1.31  2001/02/05 01:08:15  mjk
# - Fixup new problems building a distribution with all absolute
# pathnames, this is the way we build our official FTP distribution.
#
# - Bumped version numbers
#
# Revision 1.30  2001/02/03 00:39:59  mjk
# Use Site.h not Site.mk
#
# Revision 1.29  2001/02/03 00:01:59  bruno
# added genhdlist from 7.0 release
#
# Revision 1.28  2001/01/30 05:13:28  bruno
# fixes for non-existent 'hdlist'
#
# Revision 1.27  2001/01/27 00:39:26  bruno
# initial release
#
# Revision 1.26  2001/01/18 19:45:30  mjk
# bugfix
#
# Revision 1.25  2001/01/18 17:23:58  mjk
# Bug fix
#
# Revision 1.24  2001/01/17 16:54:34  mjk
# - Added --rpms flag to take the RPMS from a different release than the
# rest of the installation.  This allows us to use 7.0 Kickstart with
# 6.2 RPMS.
#
# - Symbolic link are now relative when the target is in the same tree
# as the destination.  All other symbolic links are still absolute.
# When kickstarting over FTP or HTTP it is now possible to use relative
# symbolic links and we can skip the 'explode' step which is still
# required for NFS kickstarts.  Cluster-dist will always do the right
# thing.  If you build your distribution in the same tree as the mirror
# you get to save disk space.  If you build your distribution in a
# different tree you will get only absolute symbolic links.
#
# Revision 1.23  2001/01/10 23:52:46  mjk
# changes for 7.0
#
# Revision 1.22  2000/11/29 22:46:13  mjk
# Changed remote-viewing to ekv
# Fixed bad_mirror_dirs list
# Bumped version number
#
# Revision 1.20  2000/11/03 05:40:29  mjk
# Updated manpage
#
# Revision 1.19  2000/11/02 22:15:48  mjk
# Can now be run to create the master rocks distribution and by client
# sites to base their distribution of ours.  Also added ability to read
# command line arguments from various files.
#
# Revision 1.18  2000/10/19 22:55:24  bruno
# piece-pipe and remote-viewing rpm additions
#
# Revision 1.17  2000/10/19 17:41:55  mjk
# Change explode logic to not explode symlinks to files in the same
# directory.
#
# Revision 1.16  2000/10/10 18:42:32  bruno
# fixed a weird bug in the version comparison code
#
# Revision 1.15  2000/10/05 00:19:47  mjk
# Fortran mode, fixed some sloppy whitespace.
#
# Revision 1.14  2000/10/05 00:11:33  mjk
# Fixed genhdlist command
#
# Added aliases command create versionless rpm filenames symlinked to
# the versioned filenames.  One more nail in the coffin for kickstart.
#
# Revision 1.13  2000/09/29 21:59:55  mjk
# *** empty log message ***
#
# Revision 1.12  2000/09/29 18:20:35  mjk
# Cleanup from Bruno and Myself shooting each other.  Viva la CVS.
#
# Revision 1.10  2000/09/27 21:35:15  mjk
# Bumped version number
# First attempt at allowing concurrent redhat releases is distribution
#
# Revision 1.9  2000/09/21 18:05:55  mjk
# *** empty log message ***
#
# Revision 1.8  2000/09/21 18:00:26  mjk
# Rebuild kickstart config files if Site.mk found, otherwise build
# using the Site.mk in our repository.
#
# Revision 1.7  2000/09/21 17:52:16  mjk
# Bumped version number
# Start at create a client/server for this
# Uses a local Site.mk for kickstart configs
# Hostname used for access to CVS repository (need anon access still)
#
# Revision 1.6  2000/08/29 16:38:18  mjk
# Added copyright notice
#
# Revision 1.5  2000/08/09 23:39:09  mjk
# fixed version string again
#
# Revision 1.4  2000/08/09 23:38:01  mjk
# Work around for non RPMs in the mirror RPM directories.
#
# Revision 1.3  2000/08/09 20:27:20  mjk
# Cleanup docs
#
# Revision 1.2  2000/08/09 20:25:40  mjk
# Got with the program and made into a RPM
#
# Revision 1.1  2000/06/21 23:07:40  mjk
# *** empty log message ***



import os
import sys
import getopt
import types
import string
import re
import shutil
import rocks.sql
import rocks.dist
import rocks.util
import rocks.build
import xml.sax

class App(rocks.sql.Application):

    def __init__(self, argv):
        rocks.sql.Application.__init__(self, argv)
        self.rcfileHandler = RCFileHandler

        # Setup the application defaults (these come for rc file now)

        self.path			= {}
        self.path['local']		= ''
        self.path['dist']		= ''
        self.path['root']		= ''
        self.path['cdrom']		= ''
	self.mirrors			= []

        self.arch		= ''
        self.verbose		= 0
        self.debug		= 0
        self.withRolls		= []
        self.withRollsOnly	= 0
        self.withSiteProfiles	= 1
        self.graphOptions	= ''
        self.graphFormat        = 'plain'
        self.use_links		= 1
	self.onepath		= ''
        self.rollInstall	= 0
        self.doTorrent		= 1
        self.clean		= 0
	self.lockFile		= '/var/lock/rocks-dist'
        
        # Add application flags to inherited flags

        self.getopt.s.extend([('a:', 'arch'),
                              'c',
                              ('d:', 'dirname'),
                              ('g:', 'path'),
                              ('l:', 'lang'),
                              'p',
                              ('r:', 'release'),
                              'v'])
        self.getopt.l.extend([('arch=', 'architecture'),
                              ('comps=', 'path'),
                              'copy',
                              ('dist=', 'dirname'),
                              'debug',
                              'graph-draw-invis-edges',
                              'graph-draw-order',
                              'graph-draw-edges',
                              'graph-draw-key',
                              'graph-draw-all',
                              'graph-draw-landscape',
                              'graph-draw-size=',
                              'graph-draw-format=',
                              'install',
                              ('mirror-dir=', 'dirname'),
                              ('mirror-host=', 'hostname'),
                              ('root=', 'dirname'),
                              ('cdrom=', '/mnt/cdrom'),
                              'verbose',
                              ('with-roll=', 'rollname-rollversion'),
                              'with-rolls-only',
                              'clean',
			      ('path=', 'single path item'),
			      'notorrent'
			      ])

    def usageTail(self):
        return ' command \nAvailable commands:'
    
    def parseArg(self, c):
        if c[0] in ('-h', '--help'):
            self.help()
            print string.join(self.commands())
            sys.exit(0)
        elif rocks.app.Application.parseArg(self, c):
            return 1
        elif c[0] in ('-a', '--arch'):
            self.arch = c[1]
        elif c[0] == '--comps':
            self.path['comps'] = c[1]
        elif c[0] in ('-c', '--copy'):
            self.use_links = 0
        elif c[0] in ('-d', '--dist'):
            self.path['dist'] = c[1]
        elif c[0] == '--debug':
            self.debug = self.debug + 1
        elif c[0] in ( '--graph-draw-invis-edges',
                       '--graph-draw-order',
                       '--graph-draw-edges',
                       '--graph-draw-key',
                       '--graph-draw-all',
                       '--graph-draw-landscape',
                       '--graph-draw-size' ):
            tokens = string.split(c[0], '-')
            flag   = string.join(tokens[3:], '-')
            if c[1]:
                self.graphOptions += ' --%s=%s' % (flag, c[1])
            else:
                self.graphOptions += ' --%s' % flag
        elif c[0] == '--graph-draw-format':
            self.graphFormat = c[1]
        elif c[0] == '--install':
            self.rollInstall = 1
        elif c[0] == '--notorrent':
            self.doTorrent = 0
        elif c[0] == '--mirror-dir':
	    m = self.getFirstMirror()
	    m.setPath(c[1])
        elif c[0] == '--mirror-host':
	    m = self.getFirstMirror()
	    m.setHost(c[1])
        elif c[0] == '--root':
            self.path['root'] = c[1]
        elif c[0] in ('--cdrom',):
            self.path['cdrom'] = c[1]
        elif c[0] in ('-v', '--verbose'):
            self.verbose = self.verbose + 1
        elif c[0] == '--with-roll':
            self.withRolls.append(string.split(c[1], ','))
        elif c[0] == '--with-rolls-only':
            self.withRollsOnly = 1
        elif c[0] == '--path':
		self.onepath = c[1]
        elif c[0] == '--clean':
		self.clean = 1
        else:
            return 0
        return 1


    def setPristine(self):
	base_version = self.usage_version
	kernel_version = self.usage_version

	if self.connect():
		self.execute('select version from rolls where name="base" ' +
			'and enabled="yes"')
		try:
			base_version = self.fetchone()[0]
		except:
			base_version = self.usage_version
			pass

		self.execute('select version from rolls where name="kernel"' +
			'and enabled="yes"')
		try:
			kernel_version = self.fetchone()[0]
		except:
			kernel_version = self.usage_version
			pass

		self.close()

        self.withRolls = [('base', base_version), ('kernel', kernel_version)]
        self.withSiteProfiles = 0
	return
        

    def mirrorLikeMe(self, mirror):
	"Init a mirror with our attributes"
	mirror.setArch(self.arch)
	mirror.setRoot(self.path['root'])
	return


    def getFirstMirror(self):
	if not self.mirrors:
		m = rocks.dist.Mirror()
		self.mirrorLikeMe(m)
		self.mirrors.append(m)
	else:
		m = self.mirrors[0]
	return m


    def chooseRolls(self):

        # If we have a DB try to get a list of rolls from there.
        # For the installation environment the --with-roll flag
        # will need to be used for this information.
        
        if not self.connect():
            return self.withRolls
        
        rolls = self.withRolls

        # If user specified rolls on the command line only use
        # those rolls. Otherwsie get the list of enabled rolls
        # out of the database.
        
        if len(rolls) == 0:
            self.execute('select name,version,arch,enabled from rolls '
	    	'where site=0 and OS="linux"')
            for name,version,arch,enabled in self.fetchall():
                if enabled == 'yes' and arch == self.arch:
                    rolls.append([name, version])

        self.close()
        return rolls
        



    def run(self):

	os.system('touch %s' % self.lockFile)

        if not self.arch:
            self.arch = self.getArch()

	# Set global mirror attributes (perhaps these too are per-mirror)

	for mirror in self.mirrors:
		self.mirrorLikeMe(mirror)
		if self.debug or self.verbose:
			print mirror

        dist = rocks.dist.Distribution(self.mirrors, self.usage_version)
        dist.setRoot(os.getcwd())
        dist.setDist(os.path.join(self.path['dist'], 'lan')) # LAN is default
        dist.setLocal(self.path['local'])
        dist.setContrib(os.path.join(self.path['root'], 'contrib',
		self.usage_version))
	
        for command in self.args:
            # This method of resolving functions is more robust.
            try:
                cmd_function = getattr(self, "command_%s" % (command))
            except AttributeError:
                print 'error - bad command:', command
                return
            cmd_function(dist)

	try:
		os.unlink(self.lockFile)
	except:
		pass

    def commands(self):

        # Create a list of all the command_ functions.  This might
        # break as Python changes.
        
        list = []
        for e in App.__dict__.keys():
            if type(App.__dict__[e]) == types.FunctionType:
                if string.find(e, 'command_') == 0:
                    list.append(e[8:])
        return list

    	

    def commandDist(self, dist):    	
        withRolls = self.chooseRolls()
        builder   = rocks.build.DistributionBuilder(dist, self.use_links)
        builder.setVerbose(self.verbose)
        builder.setDebug(self.debug)
        builder.setRolls(withRolls, self.withRollsOnly)
        builder.setSiteProfiles(self.withSiteProfiles)
        if self.path.has_key('comps'):
            builder.setComps(self.path['comps'])
        builder.build()
        return builder


    def makeTorrents(self, dist):    	
	import time

	print 'making "torrent" files for RPMS'

	#
	# mark each torrent file with the current time
	#
	timestamp = time.time()

	for dir in [ dist.getBasePath(), dist.getRPMSPath() ]:
		cmd = '/opt/rocks/bin/rocks create ' + \
			'torrent %s ' % (dir) + \
			'timestamp=%d' % (timestamp)
		os.system(cmd)

	return


    def command_dist(self, dist):
    
    	# LAN - this is the default distribution 
	builder = self.commandDist(dist)
	lanbase = dist.getBasePath()
	try:
		if self.doTorrent:
			self.makeTorrents(dist)
	except:
		pass
	
	# Create Yum Repository
	# self.makeYumRepository(dist)

	# WAN - switch to WAN and layout (rolls are not in RPMS directory)
	wandist = os.path.join(self.path['dist'], 'wan')
        dist.setDist(wandist)
        dist.build() # force a rebuild to move to WAN
    	self.setPristine()
	builder = self.commandDist(dist)
	
	# This is a hack to get the patched base/ from the lan distribution.
	# Clean this up for Rocks 4.1.0 and make the lan/wan completely
	# independent of each other again.
	
	builder.buildWANLinks(lanbase)
	builder.buildRollLinks()

	# WAN - just enough to allow kcgi to create dirs.
	os.system('chmod 1775 %s' % wandist)
	os.system('chgrp apache %s' % wandist)

	# make sure everyone can traverse the the rolls directories
	mirrors = dist.getMirrors()
	fullmirror = mirrors[0].getRollsPath()
	os.system('find %s -type d ' % (fullmirror) + \
		'-exec chmod -R 0755 {} \;')

	return


    def command_cdrom(self, dist, size=0):
    	print 'ERROR - command no longer supported'

    def command_usb(self, dist):
	"""Makes a bootable USB drive image. Makes a set of certificates
	suitable for securely retrieving a kickstart file from this machine."""

	# The DN for the certificate

	dn = '/OU=anonymous'
	try:
		self.connect()
		clustername = self.getGlobalVar('Info','ClusterName')
		dn = '/OU=%s' % clustername[:64]
	except:
		print 'warning - could not find cluster name'
	dn += '/CN=rocks-key-cert'
	builder = rocks.build.USBBuilder(dist)
	builder.setVerbose(self.verbose)
	builder.setDebug(self.debug)
	builder.setVersion(self.usage_version)
	builder.build(dn)
	
	
    def command_copycd(self, dist):
    	print 'ERROR - command no longer supported'


    def getCDInfo(self):
	try:
		file = open('/mnt/cdrom/.discinfo', 'r')
		t = file.readline()
		n = file.readline()
		a = file.readline()
		d = file.readline()
		file.close()

		timestamp = t[:-1]
		name = n[:-1].replace(' ', '_')
		archinfo = a[:-1]
		diskid = d[:-1]
	except:
		timestamp = None
		name = None
		archinfo = None
		diskid = None
		pass

	return (timestamp, name, archinfo, diskid)


    def copyForeignCD(self, destdir, arch):
	if not os.path.exists(destdir):
		os.makedirs(destdir)

	cdtree = rocks.file.Tree('/mnt/cdrom')
	for dir in cdtree.getDirs():
		for rpm in cdtree.getFiles(dir):
			try:
				if rpm.getPackageArch() != 'src' and \
					rpm.getBaseName() != 'anaconda' and \
					rpm.getBaseName() != \
							'anaconda-runtime' \
					and not (arch == 'i386' and \
						re.match('^kudzu.*', \
							rpm.getBaseName())):

					os.system('cp -p %s %s' % (
						rpm.getFullName(), 
							destdir))
			except:
				pass
			
	return


    def command_copyroll(self, dist):
	"""Copy a roll into the proper place in our primary mirror.
	Assumes roll has been mounted in our cdrom directory."""

	rolls = {}
	src = self.path['cdrom']
	print 'Copying roll from media (directory "%s") into mirror' \
		% (src)	
	cwd = os.getcwd()
	os.chdir(src)
	flags = "mpdu"        # make sure the timestamps are preserved
	if self.verbose:
		flags += "v"  # allow verbose output for progress bars.
	dstMirror = dist.getMirrors()[0]
	try:
		os.system('mkdir -p %s' % dst)
		os.system('find | cpio -%s %s' % (flags, dst))
	except:
		# Try roll 2.0 dir structure
		dst = dstMirror.getRollsPath()

		# Remove the directories from our dst which we are about 
		# to copy from src.

		cleanFind = 'find . -maxdepth 3 -mindepth 3 -type d'
		for line in os.popen(cleanFind).readlines():
			line = line[:-1]
                        # ./<rollname>/<rollversion>/<rollarch>
			dot,name,version,arch  = line.split(os.sep)
			if os.path.exists(os.path.join(line, 
					'roll-%s.xml' % name)):
				rolls[name] = (version, arch)
			if self.clean:
				print ' Cleaning old "%s" (%s,%s) ' % \
					(name, version, arch)
				os.system('rm -rf %s/%s' % (dst, line))
				
		for name in rolls.keys():
			print 'Copying "%s" (%s,%s) roll...' % (name,
                        	rolls[name][0], rolls[name][1])
                        dir = os.path.join(dst, name)
			os.system('find %s | cpio -%s %s ' % (name, flags, dst))
                        os.system('find %s -name "TRANS.TBL" -exec rm -f {} \;'
                                  % dir)
                        # make sure everyone can traverse the new directories
                        os.system('find %s -type d -exec chmod a+rx {} \;'
                                  % dir)

		if not rolls:
			#
			# if we here, then the media is not a rocks roll.
			# let's turn it into one
			#
			(timestamp, name, archinfo, diskid) = self.getCDInfo()

			if (timestamp, name, archinfo, diskid) != \
						(None, None, None, None):

				version = dist.getRocksRelease()
				rolls[name] = (version, archinfo)

				destdir = os.path.join(dst, name, version,
						archinfo, 'RedHat', 'RPMS')

				print 'Copying "%s" (%s,%s) roll...' % (name,
					rolls[name][0], rolls[name][1])

				self.copyForeignCD(destdir, archinfo)

	os.chdir(cwd)

	# Bail out right now if no rolls were copied into the mirror
        
        if not rolls:
        	print 'Warning - could not find any rolls'
        	return

        # Update the database to include all the rolls we just added.
        # The --install flag will enable the roll (and rebuild the distro).
        # Still allow this code to run w/o the database.
        # Duplicate roll copies do not modify the initial enabled state
        # unless the --install flag is used.

        try:
        	self.connect()
                for name in rolls.keys():
                    	version = rolls[name][0]
                        arch    = rolls[name][1]
                        self.execute('select enabled from rolls where '
                               	'name="%s" and version="%s" and '
                                'arch="%s" and site=0' % (name, version, arch))
                        row = self.fetchone()
                        if row:
                        	enabled = row[0]
                        else:
                        	enabled = 'no'
                        if self.rollInstall:
                        	enabled = 'yes'

                      	self.execute('delete from rolls where '
                               	'name="%s" and version="%s" and '
                                'arch="%s" and site=0' % (name, version, arch))

                      	self.execute('insert rolls (name,version,arch,enabled) '
				'values ("%s","%s","%s","%s")' %
                                (name, version, arch, enabled))
                self.close()
        except:
              	print 'Warning - database not updated'

	return


    def command_dist2mirror(self, dist):
	print 'Cleaning local mirrors...'
	for mirror in dist.getMirrors():
		root = mirror.getReleasePath()

		# Remove anaconda-runtime package contents and others.
		os.system('rm -rf %s/usr' % root)
		os.system('rm -rf %s/build' % root)
		os.system('rm -rf %s/force' % root)

		# Remove wget's index.html?* files left over from the mirror.
		root = os.path.join(mirror.getRootPath(), mirror.getHost())
		os.system('find %s -name "index.html*" -exec rm {} \;' % root)


    def command_makecontrib(self, dist):
        print 'Creating public and private contrib directories'
        for path in [ dist.getContribRPMSPath(),
                      dist.getContribSRPMSPath() ]:
            if not os.path.exists(path):
                os.makedirs(path)

    def command_makesitenodes(self, dist):
        print 'Creating site-nodes directory'
        path = dist.getSiteNodesPath()
        if not os.path.exists(path):
            os.makedirs(path)

    def command_dvd(self, dist):
        self.command_cdrom(dist)


    def command_graph(self, dist):
        """Draws the DOT kickstart graph"""
        cwd = os.getcwd()
        os.chdir(dist.getBuildPath())
        if self.graphFormat == 'pdf':
            self.graphFormat = 'ps2'
            postStep =  '| ps2pdf - -'
        else:
            postStep = ''
            
        os.system('/opt/rocks/sbin/kpp %s | /opt/rocks/bin/dot -T%s %s' % 
		(self.graphOptions, self.graphFormat, postStep))
        os.chdir(cwd)

        
    def command_paths(self, dist):
    
        # Look into the Mirror and Dist objects and print the result
        # of all the get.*Path() methods.  This is really ugly, and
        # should be moved into the objects themselves.

	mirrors = dist.getMirrors()

	if self.onepath:
		if self.onepath.count('()'):
			f = self.onepath
		else:
			f = '%s()' % self.onepath
		try:
			p = eval(f)
			if type(p) in (types.StringType, types.UnicodeType):
				print p
			elif type(p) == types.ListType:
				for path in p:
					print path
		except:
			pass
		return

        for i in range(0, len(mirrors)):
            for o in [ rocks.dist.Base, rocks.dist.Mirror ]:
                for e in o.__dict__.keys():
                    if type(o.__dict__[e]) == types.FunctionType:
                        if re.match('^get.*Path$', e):
                            f = 'mirrors[%d].%s()' % (i, e)
                            try:
                                path = eval(f)
                                print f, '->', path
                            except:
                                pass

        for o in [ rocks.dist.Base, rocks.dist.Distribution ]:
            for e in o.__dict__.keys():
                if type(o.__dict__[e]) == types.FunctionType:
                    if re.match('^get.*Path$', e):
                        f = 'dist.%s()' % e
                        try:
                            path = eval(f)
                            print f, '->', path
                        except:
                            pass


class RCFileHandler(rocks.app.RCFileHandler):

    def __init__(self, application):
        rocks.app.RCFileHandler.__init__(self, application)
	self.inMirror = 0
	self.mirror = rocks.util.Struct
	self.mirror.host = ''
	self.mirror.path = ''

    def startElement_host(self, name, attrs):
	if 'name' in attrs:
		self.app.host[attrs.get('name')] = attrs.get('value')
    	self.text = ''

    def endElement_host(self, name):
	if self.inMirror:
    		self.mirror.host = self.text

    def startElement_path(self, name, attrs):
	if 'name' in attrs:
		self.app.path[attrs.get('name')] = attrs.get('value')
	self.text = ''

    def endElement_path(self, name):
    	if self.inMirror:
		self.mirror.path = self.text

    def startElement_mirror(self, name, attrs):
	self.inMirror = 1

    def endElement_mirror(self, name):
	self.inMirror = 0

	mirror = rocks.dist.Mirror()
	mirror.setHost(self.mirror.host)
	mirror.setPath(self.mirror.path)

	if mirror not in self.app.mirrors:
		self.app.mirrors.append(mirror)



app = App(sys.argv)
app.parseArgs()
app.run()
