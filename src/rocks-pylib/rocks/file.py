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
# $Log: file.py,v $
# Revision 1.29  2012/11/27 00:48:40  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.28  2012/05/06 05:48:46  phil
# Copyright Storm for Mamba
#
# Revision 1.27  2011/12/22 22:14:19  phil
# Hopefully, only a temporary CentOS build problem, but some files in the base tree and updates tree have the same timestamp.  when we detect RPM files that are close in time, go look at the buildtime in the RPMs to make a determination.
#
# Revision 1.26  2011/07/23 02:30:49  phil
# Viper Copyright
#
# Revision 1.25  2010/09/07 23:53:08  bruno
# star power for gb
#
# Revision 1.24  2009/05/01 19:07:08  mjk
# chimi con queso
#
# Revision 1.23  2008/10/18 00:56:02  mjk
# copyright 5.1
#
# Revision 1.22  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.21  2007/10/28 00:39:40  anoop
# Added backward compatibility to rolls that do not have an OS parameter
# in the info tag in roll-<rollname>.xml file.
#
# Revision 1.20  2007/10/10 23:07:58  anoop
# Thinning down Pylib a little more. Moving classes that are used
# by single commands into the command structure away from pylib.
# The roll-<rollname>.xml file now supports "os" parameter
#
# Revision 1.19  2007/06/23 04:03:24  mjk
# mars hill copyright
#
# Revision 1.18  2006/09/11 22:47:23  mjk
# monkey face copyright
#
# Revision 1.17  2006/08/10 00:09:41  mjk
# 4.2 copyright
#
# Revision 1.16  2006/01/16 06:48:59  mjk
# fix python path for source built foundation python
#
# Revision 1.15  2005/10/12 18:08:42  mjk
# final copyright for 4.1
#
# Revision 1.14  2005/09/21 01:27:52  bruno
# beef up foundation support to build OS roll ISO(s)
#
# Revision 1.13  2005/09/16 01:02:21  mjk
# updated copyright
#
# Revision 1.12  2005/07/20 23:40:35  mjk
# installPackage can add to the flags
#
# Revision 1.11  2005/07/11 23:51:35  mjk
# use rocks version of python
#
# Revision 1.10  2005/07/11 21:55:48  mjk
# changes for foundation
#
# Revision 1.9  2005/06/03 03:45:32  bruno
# set the size of meta rolls to infinite
#
# Revision 1.8  2005/06/01 19:17:41  mjk
# added compat32 to rocks-roll
#
# Revision 1.7  2005/06/01 16:59:32  bruno
# only change the mode of a file if it exists
#
# Revision 1.6  2005/05/26 22:25:38  mjk
# meta rolls are back
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
# Revision 1.3	2005/03/29 02:44:20  bruno
# make rocks-roll cognizant of new roll iso naming scheme
#
# Revision 1.2	2005/03/28 19:49:09  bruno
# remove the 'roll-' assumption
#
# Revision 1.1	2005/03/01 00:22:08  mjk
# moved to base roll
#
# Revision 1.37	 2004/09/13 23:14:41  bruno
# ensure a string type is always returned -- some paths are encoded in unicode
# which breaks the reading of the comps file.
#
# Revision 1.36	 2004/03/25 03:15:48  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.35	 2004/03/08 23:26:12  mjk
# - Rolls are off to the side
# - Pristine distribution building
# - Files support chmod
# - Profiles are distribution local
#
# Revision 1.34	 2004/01/29 21:27:45  fds
# A way to override os.path.exists tests for use with remote files.
#
# Revision 1.33	 2003/12/13 00:09:43  mjk
# can't type
#
# Revision 1.32	 2003/12/13 00:07:54  mjk
# remove roll- from roll basename
#
# Revision 1.31	 2003/12/12 23:51:52  mjk
# added RollFile
#
# Revision 1.30	 2003/10/08 23:17:29  bruno
# to build CDs under taroon
#
# Revision 1.29	 2003/10/01 23:36:31  mjk
# had it backwards
#
# Revision 1.28	 2003/10/01 23:32:43  mjk
# added Package*String methods
#
# Revision 1.27	 2003/09/24 17:08:45  fds
# Bruno's changes for RH 9
#
# Revision 1.26	 2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.25	 2003/08/06 21:24:29  mjk
# back out off last commit
#
# Revision 1.24	 2003/08/04 20:40:18  fds
# Fixed block indent on line 290
#
# Revision 1.23	 2003/07/25 21:18:48  mjk
# - Fixed some files to tab spacing
# - Support rolls on the first CD
# - DVD building fixes
#
# Revision 1.22	 2003/05/22 16:39:28  mjk
# copyright
#
# Revision 1.21	 2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.20	 2002/10/18 21:33:26  mjk
# Rocks 2.3 Copyright
#
# Revision 1.19	 2002/02/21 21:33:28  bruno
# added new copyright
#
# Revision 1.18	 2002/02/14 02:12:29  mjk
# - Removed CD copy gui code from insert-ethers
# - Added CD copy code back to install.xml (using rocks-dist)
# - Added copycd command to rocks-dist
# - Added '-' packages logic to kgen
# - Other file changed to support above
#
# Revision 1.17	 2001/09/10 18:31:12  mjk
# wish I remembered what changed...
#
# Revision 1.16	 2001/05/29 17:12:21  mjk
# Added verify command support
#
# Revision 1.15	 2001/05/21 19:29:50  mjk
# - Cleanup
# - Don't create symlink for the ekv and piece-pipe packages anymore
#
# Revision 1.14	 2001/05/16 21:44:40  mjk
# - Major changes in CD building
# - Added ip.py, sql.py for SQL oriented scripts
#
# Revision 1.13	 2001/05/14 22:35:45  bruno
# cd building fixes
#
# Revision 1.12	 2001/05/09 20:17:22  bruno
# bumped copyright 2.1
#
# Revision 1.11	 2001/05/07 22:29:14  mjk
# - Release candidate 1
#
# Revision 1.10	 2001/05/04 22:58:53  mjk
# - Added 'cdrom' command, and CDBuilder class.
# - CDBuilder uses RedHat's source to parse the hdlist/comps file so we can
#   trim the set of RPMs on our CD.
# - Weekend!
#
# Revision 1.9	2001/04/27 01:08:50  mjk
# - Created working 7.0 and 7.1 distibutions (in same tree even)
# - Added symlink() method to File object.  Trying to get the File object
#   to make the decision on absolute vs. relative symlinks.  So far we are
#   absolute everywhere.
# - Still missing CD making code.  Need to figure out how to read to
#   comps files using RedHat's anaconda python code.  Then we can decide
#   which RPMs can go on the second CD based on what is required in the
#   kickstart files.
#
# Revision 1.8	2001/04/24 20:59:22  mjk
# - Moved Bruno's eKV 2nd stage patching code over.  And I even understand it.
# - The DistributionBuilder now changes the File object in the distribution as
#   the links, or copies are done.  This means the Tree always reflects what
#   is on the disk, like it should have been in the first place.
# - Added CVS Log from cluster-dist to show the history of the monster
# - Last missing piece is CD building.
#
# Revision 1.7	2001/04/21 01:50:49  mjk
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
# Revision 1.6	2001/04/20 22:27:02  mjk
# - always apply the genhdlist rpm and run it
# - removed the newdist object from the DistributionBuilder
# - added template for RocksDistributionBuilder
# - Mirror code works
# - Added 'paths' command for learing how to find pathnames
#
# Revision 1.5	2001/04/20 01:53:18  mjk
# - Basic distribution building works.	We now do either all symlink or
# all copies.  The hybrid case wasn't needed and is a big mess-o-code.
#
# - CVS checkout for build directory works
#
# - Need to decide how to add Bruno's changes to cluster-dist back in.
#
# Revision 1.4	2001/04/18 23:17:10  mjk
# - Fixed some low level design bugs in Tree, and Distribution
#
# - The DistributionBuilder can now gather RPMS from all the correct
# sources.  Still need version resolving code the the File and RPMFile
# objects.  Also need to figure how to effeciently traverse this long
# List the RPMFiles.
#
# Revision 1.3	2001/04/18 02:17:37  mjk
# All objects now know how to dump(), so we can debug the mirror and
# distribution datastructres.
#
# Revision 1.2	2001/04/18 01:20:38  mjk
# - Added build.py, util.py modules
#
# - Getting closer.  I'm happy with the object model for building
# mirrors, and this will extend well to build the distributions.
#
# - Seriously needs a design document.
#
# Revision 1.1	2001/04/17 02:27:59  mjk
# Time for an initial checkin.	Datastructure and general layout of the
# code is correct.  Still need comparison code for File and RPM objects.
#


import sys
import os
import string
import re
import shutil
import rocks.util
import xml.sax


class File:
    
	def __init__(self, file, timestamp=None, size=None):
		# Timestamp and size can be explicitly set for foreign files.
		self.setFile(file, timestamp, size)
		self.imortal = 0
	
	def __cmp__(self, file):

		if self.getBaseName() != file.getBaseName() or \
		 self.timestamp == file.timestamp:
			rc = 0
		elif self.timestamp > file.timestamp:
			rc = 1
		else:
			rc = -1

		# Override the inequality determination and base the decision
		# on the imortal flag.	If both files are divine, than don't
		# change anything.
	
		if rc and self.imortal + file.imortal == 1:
			if self.imortal:
				rc = 1
			else:
				rc = -1
		
		return rc

	def setFile(self, file, timestamp=None, size=None):
		self.pathname	= os.path.dirname(file)
		self.filename	= os.path.basename(file)

		# Get the timestamp of the file, or the derefereneced symbolic
		# link.	 If the dereferenced link does not exist set the
		# timestamp to zero.

		if None not in (timestamp, size):
			self.timestamp = timestamp
			self.size = size
		elif not os.path.islink(file):
			self.timestamp = os.path.getmtime(file)
			self.size	  = os.path.getsize(file)
		else:
			orig = os.readlink(file)
			if os.path.isfile(orig):
				self.timestamp = os.path.getmtime(orig)
				self.size		 = os.path.getsize(file)
			else:
				self.timestamp = 0
				self.size		 = 0

	def explode(self):

		# If the file is a symbolic link to a file, follow the link
		 # and copy the file.	 Links to directories are not exanded.

		file = self.getFullName()
		if os.path.islink(file):
			orig = os.readlink(file)
			if os.path.isfile(orig):
				os.unlink(file)
				shutil.copy2(orig, file)
		
				  # Fix the timestamp back to that of 
				  # the original file. The above copy seems 
				  # to do this for us, but I'm going to 
				  # leave this in to make sure it always works.
		
				tm = os.path.getmtime(orig)
				os.utime(file, (tm, tm))
		
	def setImortal(self):
		self.imortal = 1
	
	def getTimestamp(self):
		return self.timestamp

	def getSize(self):
		return float(self.size) / (1024*1024)
    
	def getUniqueName(self):
		return self.filename

	def getBaseName(self):
		return self.filename
    
	def getName(self):
		return self.filename

	def getShortName(self):
		return os.path.splitext(self.filename)[0]

	def getPath(self):
		return self.pathname

	def getFullName(self):
		return str(os.path.join(self.pathname, self.filename))

	def symlink(self, target, base=''):
		if os.path.isfile(target) or os.path.islink(target):
			os.unlink(target)
		os.symlink(self.getFullName(), target)

	def chmod(self, mode):
		if os.path.exists(self.getFullName()):
			os.chmod(self.getFullName(), mode)

	def dump(self):
		print '%s(%s)' % (self.filename, self.pathname)



class RPMBaseFile(File):

	def __init__(self, file, timestamp=None, size=None, ext=1):
		File.__init__(self, file, timestamp, size)
		self.list	= []

		# Remove ext count extensions, the default is 1, but for
		# rolls we remove two (.diskN.iso)
		
		s = self.filename	 # name-ver-rpmver.arch.rpm
		for x in range(0, ext):
			i = string.rfind(s, ".")
			s = self.filename[:i]
    
		i = string.rfind(s, ".")
		self.list.append(s[i+1:])	# get architecture string
		s = self.filename[:i]

		i = string.rfind(s, "-")	# get RPM version string
		self.release = s[i+1:]
		self.list.append(self.versionList(s[i+1:]))
		s = self.filename[:i]

		i = string.rfind(s, "-")	# get software version string
		self.version = s[i+1:]
		self.list.append(self.versionList(s[i+1:]))

	
		self.list.append(self.filename[:i]) # get package name
	
		self.list.reverse()		# we built the list backwards


	def versionList(self, s):
		list = []
		for e in re.split('\.+|_+', s):
			num	= ''
			alpha	= ''
			l	= []
			for c in e:
				if c in string.digits:
					num = num + c
					if alpha:
						l.append(alpha)
						alpha = ''
				else:
					alpha = alpha + c
					if num:
						l.append(string.atoi(num))
						num = ''
			if alpha:
				l.append(alpha)
			if num:
				l.append(string.atol(num))
			list.append(l)
		return list

	def getBaseName(self):
		return self.list[0]

	def getUniqueName(self):
		return '%s-%s' % (self.list[0], self.list[3])

	


class RPMFile(RPMBaseFile):

	def __init__(self, file, timestamp=None, size=None):
		RPMBaseFile.__init__(self, file, timestamp, size)
	
	def __cmp__(self, file):
		if self.getPackageArch() != file.getPackageArch():
			rc = 0
		else:
			# For RPM Files, if the timestamps are within 2 minutes
			# of each other check
			# the Buildtime of the RPM

		 	if abs(int(self.timestamp) - int(file.timestamp)) < 120 :
				# print "CMP %s:%s" % (self.getFullName(), file.getFullName())
				f1=os.popen("rpm -qp --qf '%%{BUILDTIME}' %s" % self.getFullName())
				self.timestamp=float(f1.readline())
				f1.close()
				f2=os.popen("rpm -qp --qf '%%{BUILDTIME}' %s" % file.getFullName())
				file.timestamp=float(f2.readline())
				f2.close()

			rc = File.__cmp__(self, file)

		return rc

	def getPackageName(self):
		return self.getBaseName()


	def getPackageVersion(self):
		return self.list[1]


	def getPackageRelease(self):
		return self.list[2]

	def getPackageVersionString(self):
		return self.version

	def getPackageReleaseString(self):
		return self.release

	def getPackageArch(self):
		return self.list[3]
		
	def installPackage(self, root, flags=""):
		"""Installs the RPM at the given root directory.  This is
		used for patching RPMs into the distribution and making
		bootable CDs"""
		pass
		
		dbdir = os.path.join(root, 'var', 'lib', 'rpm')
		if not os.path.isdir(dbdir):
			os.makedirs(dbdir)
	
		cmd = 'rpm -i --nomd5 --force --nodeps --ignorearch ' + \
			'--dbpath %s %s ' % (dbdir, flags)
		cmd += '--badreloc --relocate /=%s %s' \
			% (root, self.getFullName())

		print 'cmd', cmd
		retval = os.system(cmd)
		
		# Crawl up from the end of the dbdir path and prune off
		# all the empty directories.		
		while dbdir:
			if not os.listdir(dbdir):
				shutil.rmtree(dbdir)
			list = string.split(dbdir, os.sep)
			dbdir = string.join(list[:-1], os.sep)

		print 'retval', retval

		return retval

		
	


class RollFile(RPMBaseFile):

	def __init__(self, file, timestamp=None, size=None):
		RPMBaseFile.__init__(self, file, timestamp, size, 2)
		self.diskID = int(string.split(file, '.')[-2][4:])
	
	def __cmp__(self, file):
		if self.getRollArch() != file.getRollArch():
			rc = 0
		else:
			rc = File.__cmp__(self, file)
		return rc


	def getRollDiskID(self):
		return self.diskID
		
	def getRollName(self):
		return self.getBaseName()

	def getRollVersion(self):
		return self.list[1]

	def getRollRelease(self):
		return self.list[2]

	def getRollVersionString(self):
		return self.version

	def getRollReleaseString(self):
		return self.release

	def getRollArch(self):
		return self.list[3]


class RollInfoFile(File,
	xml.sax.handler.ContentHandler, xml.sax.handler.DTDHandler,
	xml.sax.handler.EntityResolver, xml.sax.handler.ErrorHandler):

	def __init__(self, file):
		File.__init__(self, file)
		
		self.attrs = {}
		parser = xml.sax.make_parser()
		parser.setContentHandler(self)
		fin = open(file, 'r')
		parser.parse(fin)
		fin.close()
		
	def startElement(self, name, attrs):
		self.attrs[str(name)] = {}
		for (attrName, attrVal) in attrs.items():
			self.attrs[str(name)][str(attrName)] = str(attrVal)
	
	def getXML(self):
		"""Regenerate the XML file based on what was read in and
		the current state."""
		
		xml = []
		
		xml.append('<roll name="%s" interface="%s">' %
			(self.getRollName(), self.getRollInterface()))
		for tag in self.attrs.keys():
			if tag == 'roll':
				continue
			attrs = ''
			for key,val in self.attrs[tag].items():
				attrs += ' %s="%s"' % (key, val)
			xml.append('\t<%s%s/>' % (tag, attrs))
		xml.append('</roll>')
		
		return string.join(xml, '\n')
		
	def getRollName(self):
		return self.attrs['roll']['name']
		
	def getRollInterface(self):
		return self.attrs['roll']['interface']
		
	def getRollVersion(self):
		return self.attrs['info']['version']
	
	def getRollRelease(self):
		return self.attrs['info']['release']
		
	def setRollOS(self, os):
		self.attrs['info']['os'] = os
		
	def getRollOS(self):
		try:
			return self.attrs['info']['os']
		except KeyError:
			return 'linux'

	def setRollArch(self, arch):
		self.attrs['info']['arch'] = arch

	def getRollArch(self):
		return self.attrs['info']['arch']
		
	def getISOMaxSize(self):
		return float(self.attrs['iso']['maxsize'])

	def setISOMaxSize(self, size):
		self.attrs['iso']['maxsize'] = size
		
	def getISOFlags(self):
		return self.attrs['iso']['mkisofs']
		
	def getRollRolls(self):
		return self.attrs['rpm']['rolls']
		
	def isBootable(self):
		return int(self.attrs['iso']['bootable'])
		
	def hasRolls(self):
		if self.attrs['rpm']['rolls'] != '0':
			return 1
		else:
			return 0
		
	def hasRPMS(self):
		return int(self.attrs['rpm']['bin'])
		
	def hasSRPMS(self):
		return int(self.attrs['rpm']['src'])
		

class Tree:

	def __init__(self, root):
		self.root = root
		self.tree = {}
		self.build('')

	def getRoot(self):
		return self.root

	def getDirs(self):
		return self.tree.keys()

	def clear(self, path=''):
		l1 = string.split(path, os.sep)
		for key in self.tree.keys():
			l2 = string.split(key, os.sep)
			if rocks.util.list_isprefix(l1, l2):
				del self.tree[key]
	
	def getFiles(self, path=''):
		try:
		    list = self.tree[path]
		except KeyError:
		    list = []
		return list

	def setFiles(self, path, files):
		self.tree[path] = files
	
	def build(self, dir):
		path = os.path.join(self.root, dir)
		if not os.path.isdir(path):
		    return

		# Handle the case where we don't have permission to traverse
		# into a tree by pruning off the protected sub-tree.
		try:
		    files = os.listdir(path)
		except:
		    files = []

		v = []
		for f in files:
			filepath = os.path.join(path, f)
			if os.path.isdir(filepath) and not \
			os.path.islink(filepath):
				self.build(os.path.join(dir, f))
			else:
				if re.match('.*\.rpm$', f) != None:
					v.append(RPMFile(filepath))
				elif re.match('roll-.*\.iso$', f) != None:
					v.append(RollFile(filepath))
				else:
					v.append(File(filepath))
		self.tree[dir] = v

	def dumpDirNames(self):
		for key in self.tree.keys():
		    print key
	    
	def dump(self):
		self.apply(self.__dumpIter__)

	def apply(self, func, root=None):
		for key in self.tree.keys():
			for e in self.tree[key]:
				func(key, e, root)

	def getSize(self):
		'Return the size the if Tree in Mbytes'

		len = 0
		for key in self.tree.keys():
			for file in self.tree[key]:
				len = len + file.getSize()
		return float(len)
    

	def __dumpIter__(self, path, file, root):
		print path,
		file.dump()
	
	
