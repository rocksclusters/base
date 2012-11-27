#! /opt/rocks/bin/python
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.6 (Emerald Boa)
# 		         version 6.1 (Emerald Boa)
# 
# Copyright (c) 2000 - 2013 The Regents of the University of California.
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
# $Log: dist.py,v $
# Revision 1.26  2012/11/27 00:48:40  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.25  2012/05/06 05:48:46  phil
# Copyright Storm for Mamba
#
# Revision 1.24  2011/07/23 02:30:49  phil
# Viper Copyright
#
# Revision 1.23  2010/09/07 23:53:08  bruno
# star power for gb
#
# Revision 1.22  2009/05/01 19:07:08  mjk
# chimi con queso
#
# Revision 1.21  2008/12/18 21:41:17  bruno
# add the 'enabled' field to the rolls selection code while building a distro.
#
# Revision 1.20  2008/10/18 00:56:02  mjk
# copyright 5.1
#
# Revision 1.19  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.18  2007/06/23 04:03:24  mjk
# mars hill copyright
#
# Revision 1.17  2006/09/11 22:47:23  mjk
# monkey face copyright
#
# Revision 1.16  2006/08/10 00:09:41  mjk
# 4.2 copyright
#
# Revision 1.15  2006/06/05 17:57:37  bruno
# first steps towards 4.2 beta
#
# Revision 1.14  2006/01/16 06:48:59  mjk
# fix python path for source built foundation python
#
# Revision 1.13  2005/10/12 18:08:42  mjk
# final copyright for 4.1
#
# Revision 1.12  2005/09/16 01:02:21  mjk
# updated copyright
#
# Revision 1.11  2005/09/02 00:05:49  bruno
# pushing toward 4.1 beta
#
# Revision 1.10  2005/07/21 17:42:43  bruno
# fix to enable multiple versions of a roll in the roll mirror. now, all rolls
# found within the mirror are returned from getRolls()
#
# prior to this fix, if you had two versions of a roll (e.g., 4.0.0 and 4.1)
# in your mirror, this code would list only one. and worse, if there was not
# an <arch> directory under one of the directories, you could get an empty
# list retured.
#
# Revision 1.9  2005/07/11 23:51:35  mjk
# use rocks version of python
#
# Revision 1.8  2005/06/02 23:44:11  mjk
# 64bit means 32 also
#
# Revision 1.7  2005/05/25 00:24:40  fds
# Fixed previous commit log
#
# Revision 1.6  2005/05/25 00:23:38  fds
# Fixed roll merging on frontends during install
#
# Revision 1.5  2005/05/24 21:21:57  mjk
# update copyright, release is not any closer
#
# Revision 1.4  2005/04/29 01:14:25  mjk
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
# Revision 1.3  2005/03/21 23:46:30  bruno
# everything's a roll support added
#
# Revision 1.2  2005/03/15 07:07:22  bruno
# AMD64 is dead -- long live x86_64
#
# Revision 1.1  2005/03/01 00:22:08  mjk
# moved to base roll
#
# Revision 1.80  2004/10/04 19:20:00  fds
# getArchList gives a list of binary compatible architectures.
#
# Revision 1.79  2004/09/16 17:35:34  bruno
# so close
#
# Revision 1.78  2004/09/14 19:47:38  bruno
# pretty close to making a working CD
#
# Revision 1.77  2004/08/30 23:35:40  bruno
# comment says it all
#
# Revision 1.76  2004/08/28 17:04:29  bruno
# nocona support -- make sure to pick up packages in the 'ia32e' directories.
#
# Revision 1.75  2004/08/11 19:03:33  fds
# WANReleasePath shows up in paths.
#
# Revision 1.74  2004/08/09 23:38:22  fds
# Allows empty mirrors.
#
# Revision 1.73  2004/07/13 19:14:29  fds
# Secure kickstart
#
# Revision 1.72  2004/05/25 01:54:05  fds
# Multiple mirror support for rocks-dist parser. Comparator used to ensure we
# do not read the same mirror twice, a danger when multiple rocks-distrc files
# are in the lookup path.
#
# Revision 1.71  2004/05/23 15:24:16  bruno
# support for rebuilding SRPMS out of the rebuild tree
#
# Revision 1.70  2004/04/28 04:06:26  bruno
# make sure rebuild directory structure is absolute and not relative to current
# working directory
#
# Revision 1.69  2004/04/28 01:52:08  bruno
# updated rebuild tree to point to the rebuilt packages
#
# Revision 1.68  2004/04/20 03:28:43  fds
# Move copyroll guts into dist where it should be. Allows it to show
# up in rocks-dist paths and to be used elsewhere.
#
# Revision 1.67  2004/04/18 04:17:19  bruno
# only get the ISOs if you're the beta -- but check if you are a beta first
#
# Revision 1.66  2004/03/25 03:15:48  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.65  2004/03/23 19:29:45  fds
# Tweaks
#
# Revision 1.64  2004/03/23 19:24:24  fds
# Support for building central roll links.
#
# Revision 1.63  2004/03/09 21:22:54  mjk
# includes all found rolls now
#
# Revision 1.62  2004/03/08 23:26:12  mjk
# - Rolls are off to the side
# - Pristine distribution building
# - Files support chmod
# - Profiles are distribution local
#
# Revision 1.61  2004/03/03 19:31:57  fds
# Push ugly stuff into dist, tools are cleaner.
#
# Revision 1.60  2004/03/02 00:22:14  mjk
# added Roll path methods
#
# Revision 1.59  2003/11/13 05:31:25  mjk
# typo
#
# Revision 1.58  2003/11/12 22:36:36  mjk
# fix bin updates to new scheme
#
# Revision 1.57  2003/11/12 22:32:31  mjk
# better encapsulation
#
# Revision 1.56  2003/11/12 22:22:41  mjk
# more of the same
#
# Revision 1.55  2003/11/12 22:07:05  mjk
# get SRPMS from WS for updates
#
# Revision 1.54  2003/10/23 00:57:25  fds
# Mirror constructor respects distArch.
#
# Revision 1.53  2003/10/21 23:44:45  fds
# We need this now. DistArch is a first class attribute.
#
# Revision 1.52  2003/10/17 00:01:00  mjk
# get ISOs for beta
#
# Revision 1.51  2003/10/16 20:41:13  fds
# Small fixes
#
# Revision 1.50  2003/10/16 20:06:37  fds
# Fixed some architecture issues.
#
# Revision 1.49  2003/10/02 20:04:00  fds
# Setting arch type for self.distro in kickstart.Application. Added
# DistRPMList exception to getRPM so we can choose the correct kernel
# in dist.py. Small changes to app.py.
#
# Revision 1.48  2003/09/28 19:42:43  fds
# Removed uneeded accessor methods, and
# made base class more aware of HomePath. Also fixed Taroon arch mismatch.
#
# Revision 1.47  2003/09/26 22:32:52  fds
# Correctly mirrors the taroon beta release.
# Tested on all mirrors on NAS.
#
# Revision 1.46  2003/09/12 23:08:18  fds
# Added comps.xml parsing. More Exception handling.
#
# Revision 1.45  2003/09/11 18:55:33  fds
# Putting three newlines before a class makes the code
# more readable, not such a jumble.
#
# Revision 1.44  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.43  2003/08/15 18:31:59  mjk
# - Gave into FDS and put some formatting into ci/co "compiler output"
# - Some more arch fixes for rocks-dist
#
# Revision 1.42  2003/08/14 20:30:49  mjk
# legacy x86 architecture fix
#
# Revision 1.41  2003/08/13 22:12:54  mjk
# gingin changes
#
# Revision 1.40  2003/08/11 21:17:36  mjk
# Opteron feels very fast
#
# Revision 1.39  2003/07/25 21:18:48  mjk
# - Fixed some files to tab spacing
# - Support rolls on the first CD
# - DVD building fixes
#
# Revision 1.38  2003/07/07 22:20:50  bruno
# neuvo
#
# Revision 1.37  2003/07/07 16:25:07  mjk
# IA64 redux
#
# Revision 1.36  2003/07/01 16:55:10  mjk
# i386 fix
#
# Revision 1.35  2003/06/30 23:47:16  mjk
# ia64 source distro building changes
#
# Revision 1.34  2003/05/22 16:39:28  mjk
# copyright
#
# Revision 1.33  2003/03/28 19:05:07  mjk
# put release in contrib path
#
# Revision 1.32  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.31  2002/12/18 17:38:54  bruno
# added a routine to generate an integer from a version number -- this enables
# version numbers to be reliably compared.
#
# Revision 1.30  2002/12/12 17:38:39  bruno
# added check for 8.0 with the comps file
#
# Revision 1.29  2002/10/28 20:16:20  mjk
# Create the site-nodes directory from rocks-dist
# Kill off mpi-launch
# Added rocks-backup
#
# Revision 1.28  2002/10/18 21:33:26  mjk
# Rocks 2.3 Copyright
#
# Revision 1.27  2002/10/18 19:20:11  mjk
# Support for multiple mirrors
# Fixed insert-copyright for new CVS layout
#
# Revision 1.26  2002/06/17 19:50:02  bruno
# 7.3-isms
#
# Revision 1.25  2002/02/26 01:12:52  mjk
# - Remove more of the --cdrom stuff from bruno, thanks to my screwup
# - Added audiofile rpm back the x11 config (gnome needs sound, piece of crap)
# - Burned down a frontend and compute nodes looks pretty good.
#
# Revision 1.24  2002/02/23 00:10:46  bruno
# updates to handle 'negative' packages. the cdrom builder needs them and
# kickstarting nodes don't.
#
# Revision 1.23  2002/02/21 21:33:28  bruno
# added new copyright
#
# Revision 1.22  2002/02/16 00:04:12  mjk
# Use rocks-dist to create /home/install/contrib directories
#
# Revision 1.21  2001/11/09 00:19:02  mjk
# ia64 changes
#
# Revision 1.19  2001/11/03 00:05:50  bruno
# first steps into 7.2 land
#
# Revision 1.18  2001/10/30 02:17:54  mjk
# - Were cooking with CGI kickstart now
# - added popen stuff to ks.py
# - verify command is dead
#
# Revision 1.17  2001/10/26 17:31:57  bruno
# rocks-dist now respects the RPMHOME environment variable
#
# Revision 1.16  2001/09/10 18:31:12  mjk
# wish I remembered what changed...
#
# Revision 1.15  2001/05/29 17:12:21  mjk
# Added verify command support
#
# Revision 1.14  2001/05/16 21:44:40  mjk
# - Major changes in CD building
# - Added ip.py, sql.py for SQL oriented scripts
#
# Revision 1.13  2001/05/11 18:12:09  bruno
# cd building
#
# Revision 1.12  2001/05/09 20:17:21  bruno
# bumped copyright 2.1
#
# Revision 1.11  2001/05/07 22:29:14  mjk
# - Release candidate 1
#
# Revision 1.10  2001/05/04 22:58:53  mjk
# - Added 'cdrom' command, and CDBuilder class.
# - CDBuilder uses RedHat's source to parse the hdlist/comps file so we can
#   trim the set of RPMs on our CD.
# - Weekend!
#
# Revision 1.9  2001/04/27 01:08:50  mjk
# - Created working 7.0 and 7.1 distibutions (in same tree even)
# - Added symlink() method to File object.  Trying to get the File object
#   to make the decision on absolute vs. relative symlinks.  So far we are
#   absolute everywhere.
# - Still missing CD making code.  Need to figure out how to read to
#   comps files using RedHat's anaconda python code.  Then we can decide
#   which RPMs can go on the second CD based on what is required in the
#   kickstart files.
#
# Revision 1.8  2001/04/24 20:59:22  mjk
# - Moved Bruno's eKV 2nd stage patching code over.  And I even understand it.
# - The DistributionBuilder now changes the File object in the distribution as
#   the links, or copies are done.  This means the Tree always reflects what
#   is on the disk, like it should have been in the first place.
# - Added CVS Log from cluster-dist to show the history of the monster
# - Last missing piece is CD building.
#
# Revision 1.7  2001/04/21 01:50:49  mjk
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
# Revision 1.6  2001/04/20 22:27:02  mjk
# - always apply the genhdlist rpm and run it
# - removed the newdist object from the DistributionBuilder
# - added template for RocksDistributionBuilder
# - Mirror code works
# - Added 'paths' command for learing how to find pathnames
#
# Revision 1.5  2001/04/20 01:53:18  mjk
# - Basic distribution building works.  We now do either all symlink or
# all copies.  The hybrid case wasn't needed and is a big mess-o-code.
#
# - CVS checkout for build directory works
#
# - Need to decide how to add Bruno's changes to cluster-dist back in.
#
# Revision 1.4  2001/04/18 23:17:10  mjk
# - Fixed some low level design bugs in Tree, and Distribution
#
# - The DistributionBuilder can now gather RPMS from all the correct
# sources.  Still need version resolving code the the File and RPMFile
# objects.  Also need to figure how to effeciently traverse this long
# List the RPMFiles.
#
# Revision 1.3  2001/04/18 02:17:37  mjk
# All objects now know how to dump(), so we can debug the mirror and
# distribution datastructres.
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
#

import os
import types
import string
import rocks.file
import rocks.ks
import xml.sax

class DistError(Exception):
	pass
	
class DistRPMList(DistError):
	def __init__(self, list):
		Exception.__init__(self, list)
		self.list = list

	
# All the 'get()' functions return None on failure.

class Arch:
	"""Base class that understands Linux architecture strings and nothing
	else.  All distributions needs this information as do other code
	that handles rpms"""
	
	def __init__(self):
		self.arch	= ''
		self.distArch	= ''
		self.cpus	= []
		self.i86cpus	= [ 'athlon', 'i686', 'i586', 'i486', 'i386' ]
		
	def getCPUs(self):
		return self.cpus
		
	def getArch(self):
		return self.arch
		
	def getDistArch(self):
		return self.distArch

	def setArch(self, arch, distArch=None):
		"""The two architectures are to handle trends like
		the AMD64 dist arch, where the true arch is x86_64.
		NOTE: This trend does not exist with RHEL."""
		
		self.arch = arch
		if arch in self.i86cpus:
			self.cpus = self.i86cpus
			self.arch = 'i386'
		elif arch == 'x86_64':
			self.cpus = [ arch ]
			self.cpus.extend([ 'ia32e' ])
			self.cpus.extend(self.i86cpus)
		else:
			self.cpus = [ arch ]

		self.cpus.extend([ 'src', 'noarch' ])
		
		if distArch:
			self.distArch = distArch
		else:
			self.distArch = arch



		
class Base(Arch):
	"""Understands how to navigate the sometimes arcane 
	RedHat linux distribution directory paths. Used to build
	and manipulate custom RedHat-compatible distributions."""

	def __init__(self):
		Arch.__init__(self)
		self.root       = ''
		self.distdir	= ''
		self.trees	= {}

	def isBuilt(self):
		if self.trees != {}:
			return 1
		else:
			return 0

	def build(self):
		self.trees['release'] = rocks.file.Tree(self.getReleasePath())

	def setRoot(self, s):
		self.root = s
		
	def setDist(self, d):
		self.distdir = d
		
	def getDist(self):
		return self.distdir

	def getRootPath(self):
		return self.root

	def getHomePath(self):
		return os.path.join(self.root, self.distdir)

	def getReleasePath(self):
		return os.path.join(self.getHomePath(), self.getDistArch())

	def getWANReleasePath(self, client='all'):
		return os.path.join(self.getHomePath(), client, 
			self.getDistArch())

	def getRPMSPath(self):
		return os.path.join(self.getReleasePath(), 'RedHat', 'RPMS')

	def getSRPMSPath(self):
		return os.path.join(self.getReleasePath(), 'SRPMS')
    
	def getBasePath(self):
		return os.path.join(self.getReleasePath(), 'RedHat', 'base')
		

	def getRollCentralPath(self):
		return str(os.path.join(self.getHomePath(), 'rolls'))

        
	def getBaseFile(self, name):
		for file in self.getFiles('release',
					  os.path.join('RedHat', 'base')):
			if file.getName() == name:
				return file
		return None

	def getTreeNames(self):
		return self.trees.keys()

	def getTree(self, name):
		if name in self.trees.keys():
			return self.trees[name]
		else:
			return None

	def setFiles(self, name, path, list):
		self.trees[name].setFiles(path, list)

	def getFiles(self, name, path):
		try:
			value = self.trees[name]
		except KeyError:
			return []
		list = [] 
		if type(value) == types.ListType:
			for tree in value:
				list.extend(tree.getFiles(path))
			return list
		else:
			return value.getFiles(path)

	def setBaseFiles(self, list):
		self.setFiles('release', os.path.join('RedHat', 'base'), list)

	def setRPMS(self, list):
		self.setFiles('release', os.path.join('RedHat', 'RPMS'), list)
        
	def setSRPMS(self, list):
		self.setFiles('release', 'SRPMS', list)

	def getPackage(self, name, list):
		matches = []
		for file in list:
			if file.getBaseName() == name:
				matches.append(file)
		
		if not matches:
			return None
		elif len(matches) == 1:
			return matches[0]
		else:
			raise DistRPMList(matches)

	def getRPM(self, name):
		return self.getPackage(name, self.getRPMS())
		
	def getSRPM(self, name):
		return self.getPackage(name, self.getSRPMS())
        
	def getRPMS(self):
		return self.getFiles('release', os.path.join('RedHat', 'RPMS'))

	def getSRPMS(self):
		return self.getFiles('release', os.path.join('SRPMS'))

	def getReleaseTree(self):
		return self.getTree('release')

	def dumpDirNames(self):
		for key in self.trees.keys():
			value = self.trees[key]
			if type(value) == types.ListType:
				for e in value:
					e.dumpDirNames()
			else:
				value.dumpDirNames()
        
	def dump(self):
		for key in self.trees.keys():
			value = self.trees[key]
			if type(value) == types.ListType:
				for e in value:
					e.dump()
			else:
				value.dump()


        
class Mirror(Base):

	def __init__(self, mirror=None):
		Base.__init__(self)
		if mirror:
			self.setHost(mirror.host)
			self.setPath(mirror.dir)
			self.setRoot(mirror.root)
			self.setArch(mirror.arch, mirror.distArch)
		else:
			self.host	= ''
			self.dir	= ''
		self.getRelease = 1



	def __str__(self):
		s = "Rocks Mirror Distribution\n"
		s += "Host: %s\n" % self.getHost()
		s += "Path: %s\n" % self.getPath()
		return s

	def __cmp__(self, other):
		if not other:
			return -1
		elif other.getHost() == self.getHost() and \
			other.getPath() == self.getPath():
			return 0
		else:
			return -1

	def build(self):
		Base.build(self)
		self.trees['rolls'] = rocks.file.Tree(self.getRollsPath())

	def getRootPath(self):
		return self.root

	def setHost(self, s):
		self.host = s

	def setPath(self, s):
		self.dir = s

	def getHost(self):
		return self.host

	def getPath(self):
		return self.dir
    
	def getHomePath(self):
		return os.path.join(self.root, self.host, self.dir)

	def getRemoteReleasePath(self):
		return os.path.join(self.dir, self.getDistArch())

	def getRollsPath(self):
		#return os.path.join(self.getHomePath(), 'rolls')
		return os.path.join(self.getRootPath(), 'rolls')


	def getRollRPMS(self, roll, version, arch):
		path = os.path.join(roll, version, arch, 'RedHat', 'RPMS')
		return self.getFiles('rolls', path)


	def getRollBaseFiles(self, roll, version, arch):
		path = os.path.join(roll, version, arch, 'RedHat', 'base')
		return self.getFiles('rolls', path)
		

	def getRollSRPMS(self, roll, version, arch):
		path = os.path.join(roll, version, arch, 'SRPMS')
		return self.getFiles('rolls', path)

		
	def getRolls(self):
		rolls = {}
		rollsPath = self.getRollsPath()
		if not os.path.exists(rollsPath):
			return rolls
		for r in os.listdir(rollsPath):
			rolls[r] = []
			rdir = os.path.join(self.getRollsPath(), r)
			if not os.path.isdir(rdir):
				continue
			for v in os.listdir(rdir):
				vdir = os.path.join(rdir, v)
				if not os.path.isdir(vdir):
					continue
				for a in os.listdir(vdir):
					adir = os.path.join(vdir, a)
					if not os.path.isdir(adir):
						continue
					rolls[r].append((a, v))
		return rolls


class Distribution(Base):

	def __init__(self, m, v):
		Base.__init__(self)
		self.contrib	= ''
		self.local	= ''
		self.mirrors	= m
		self.root	= self.mirrors[0].root
		self.arch	= self.mirrors[0].arch
		self.distArch 	= self.mirrors[0].distArch
		self.cpus	= self.mirrors[0].cpus
		self.version	= v

	def build(self):
		Base.build(self)
		self.trees['contrib'] = rocks.file.Tree(self.contrib)
		self.trees['force'] = rocks.file.Tree(self.getForceRPMSPath())
		self.trees['site-profiles'] = rocks.file.Tree(
			self.getSiteProfilesPath())
		self.trees['local'] = []
		self.trees['local_srpms'] = []
		self.trees['cdrom'] = []
		self.trees['rolls'] = []
		for e in self.getSiteRPMSPath():
			self.trees['local'].append(rocks.file.Tree(e))
		for e in self.getSiteSRPMSPath():
			self.trees['local_srpms'].append(rocks.file.Tree(e))
		# make the force tree imortal
		for f in self.trees['force'].getFiles(''):
			f.setImortal()

    
	def setContrib(self, s):
		self.contrib = s

	def setLocal(self, s):
		self.local = s
		
	def getRocksRelease(self):
		return self.version
    
	def getBuildPath(self):
		return os.path.join(self.getReleasePath(), 'build')
    
	def getKickstartFile(self, file, distdir=None):
		cwd = os.getcwd()
		os.chdir(self.getRootPath())
		retval = rocks.ks.KickstartFile(file, self.arch, distdir)
		os.chdir(cwd)
		return retval

	def getSiteRPMSPath(self):
		l = []
		if self.local:
			for cpu in self.cpus:
				l.append(os.path.join(self.local, 'RPMS', cpu))
		if os.environ.has_key('RPMHOME'):
			for cpu in self.cpus:
				l.append(os.path.join(os.environ['RPMHOME'],
						      'RPMS', cpu))
		return l

	def getSiteSRPMSPath(self):
		l = []
		if self.local:
			l.append(os.path.join(self.local, 'SRPMS'))
		if os.environ.has_key('RPMHOME'):
			l.append(os.path.join(os.environ['RPMHOME'], 'SRPMS'))
		return l

	def getForceRPMSPath(self):
		return os.path.join(self.getReleasePath(), 'force', 'RPMS')

	def getRollsPath(self):
		return os.path.join(self.getReleasePath(), 'rolls')

	def getContribRPMSPath(self):
		return os.path.join(self.contrib, self.arch, 'RPMS')

	def getContribSRPMSPath(self):
		return os.path.join(self.contrib, self.arch, 'SRPMS')

	def getSiteProfilesPath(self):
		return os.path.join(self.getRootPath(), 'site-profiles',
				    self.getRocksRelease())

	def getMirrors(self):
		return self.mirrors

	def getContribRPMS(self):
		return self.getFiles('contrib', os.path.join(self.arch, 'RPMS'))

	def getContribSRPMS(self):
		return self.getFiles('contrib', os.path.join(self.arch, 'SRPMS'))

	def getLocalRPMS(self):
		return self.getFiles('local', '')

	def getLocalSRPMS(self):
		return self.getFiles('local_srpms', '')

	def getForceRPMS(self):
		return self.getFiles('force', '')

	def getSiteProfilesTree(self):
		return self.getTree('site-profiles')

	def syncMirror(self):
		for mirror in self.mirrors:
			tree = mirror.getTree('release')
			for key in tree.getDirs():
				self.getTree('release').\
				setFiles(key, tree.getFiles(key))


