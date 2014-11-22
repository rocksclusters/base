# $Id: __init__.py,v 1.38 2012/11/27 00:48:11 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
# 
# Copyright (c) 2000 - 2014 The Regents of the University of California.
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
# $Log: __init__.py,v $
# Revision 1.38  2012/11/27 00:48:11  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.37  2012/05/06 05:48:22  phil
# Copyright Storm for Mamba
#
# Revision 1.36  2012/03/30 06:04:03  phil
# update python path to properly import yum
#
# Revision 1.35  2012/02/01 20:01:26  phil
# use subprocess instead of popen2
#
# Revision 1.34  2011/08/25 21:13:31  anoop
# Since sunos rolls are present in separate jumpstart location,
# we dont need osname in the directory hierarchy
#
# Revision 1.33  2011/07/23 02:30:27  phil
# Viper Copyright
#
# Revision 1.32  2010/09/14 16:55:41  bruno
# give meta rolls the same version number as the hosting/building system
#
# Revision 1.31  2010/09/07 23:52:52  bruno
# star power for gb
#
# Revision 1.30  2009/08/25 21:45:51  anoop
# More patching support for Solaris.
#   - support for including patches during creation of Rolls
#   - support for parsing <patch> tags
#   - support for contrib patches
#
# Revision 1.29  2009/05/01 19:06:56  mjk
# chimi con queso
#
# Revision 1.28  2009/04/09 20:29:16  bruno
# much simplier way in which to write out a minimal kickstart file for
# bootable rolls
#
# Revision 1.27  2008/10/18 00:55:48  mjk
# copyright 5.1
#
# Revision 1.26  2008/08/07 21:19:23  bruno
# OS roll building fix
#
# Revision 1.25  2008/08/06 21:06:57  bruno
# fixes to build OS roll
#
# Revision 1.24  2008/07/01 21:23:57  bruno
# added the command 'rocks remove roll' and tweaked the other roll commands
# to handle 'arch' flag.
#
# thank to Brandon Davidson from the University of Oregon for these changes.
#
# Revision 1.23  2008/04/02 22:10:02  bruno
# also include the '@core' group when building the OS rolls
#
# Revision 1.22  2008/04/01 15:43:06  bruno
# when constructing the list of required OS packages, make sure to get the
# dependencies of the dependencies.
#
# Revision 1.21  2008/03/17 23:14:25  bruno
# fix to build OS roll on x86_64
#
# Revision 1.20  2008/03/06 23:41:36  mjk
# copyright storm on
#
# Revision 1.19  2008/03/03 18:57:48  bruno
# fix for building ks.cfg on the kernel roll CD and make sure the root
# password is not on the kernel roll CD.
#
# Revision 1.18  2008/02/26 21:36:56  bruno
# use a local yum.conf file
#
# Revision 1.17  2008/02/26 19:53:39  bruno
# lots of changes in order to make the OS roll under RHEL 5
#
# Revision 1.16  2008/02/13 01:04:47  anoop
# Add extra dir for OS, for solaris rolls only
#
# Revision 1.15  2007/12/13 02:53:40  bruno
# can now build a bootable kernel CD and build a physical frontend with V
# on RHEL 5 update 1
#
# Revision 1.14  2007/12/10 21:28:34  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.13  2007/10/31 23:04:16  anoop
# Adding more rolls capability, so that Solaris Rolls start to look more
# like Linux rolls with version numbers and architecture separated directories.
#
# Revision 1.12  2007/10/10 23:07:58  anoop
# Thinning down Pylib a little more. Moving classes that are used
# by single commands into the command structure away from pylib.
# The roll-<rollname>.xml file now supports "os" parameter
#
# Revision 1.11  2007/10/03 22:14:06  anoop
# Changes to internal functioning of the "rocks create roll" command. All
# classes except Command class moved to rollbuilder.py under pylib
# Any changes that need to be made to roll building need to go to rollbuilder.py
# in pylib.
#
# Minor changes to "rocks add roll" command as well. Functionality for this
# will be moved up to pylib as well.
#
# Revision 1.10  2007/07/04 01:47:37  mjk
# embrace the anger
#
# Revision 1.9  2007/07/02 18:35:24  bruno
# create cleanup
#
# Revision 1.8  2007/06/23 03:54:52  mjk
# - first pass at consistency
# - still needs some docstrings
# - argument processors take SQL wildcards
# - add cannot run twice (must use set)
# - dump does sets not just adds
#
# Revision 1.7  2007/06/19 16:42:40  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.6  2007/06/07 21:23:04  mjk
# - command derive from verb.command class
# - default is MustBeRoot
# - list.command / dump.command set MustBeRoot = 0
# - removed plugin non-bugfix
#
# Revision 1.5  2007/06/06 18:31:22  bruno
# allow only one argument
#
# Revision 1.4  2007/05/31 22:57:06  bruno
# more tweaks
#
# Revision 1.3  2007/05/31 19:35:42  bruno
# first pass at getting all the 'help' consistent on all the rocks commands
#
# Revision 1.2  2007/05/10 20:37:01  mjk
# - massive rocks-command changes
# -- list host is standardized
# -- usage simpler
# -- help is the docstring
# -- host groups and select statements
# - added viz commands
#
# Revision 1.1  2007/04/06 21:37:22  bruno
# add the rocks-roll replacement and changed 'rocks create mirror' to call
# 'rocks create roll' to build the ISO image
#
# Revision 1.1  2007/04/06 18:24:26  bruno
# converted rocks-mirror
#
#

import os
import sys
import re
import string
import time
import tempfile
import shutil
import subprocess
import pexpect
import socket
import rocks
import rocks.commands
import rocks.dist
import rocks.file
import rocks.roll
import rocks.util


class Builder:

	def __init__(self):
		self.config = None
		self.tempdir = os.getcwd()

	def mktemp(self):
		return tempfile.mktemp(dir=self.tempdir)
		
	def makeBootable(self, name):
		pass
				
	def mkisofs(self, isoName, rollName, diskName, rollDir):
		print 'Building ISO image for %s ...' % diskName

		if self.config.isBootable():
			extraflags = self.config.getISOFlags()
		else:
			extraflags = ''

		volname = '%s %s' % (rollName, diskName)
		if len(volname) > 32:
			volname = volname[0:32]
			
		cwd = os.getcwd()
		cmd = 'mkisofs -V "%s" %s -r -T -f -o %s .' % \
			(volname, extraflags, os.path.join(cwd, isoName))

		os.chdir(rollDir)
		rocks.util.system(cmd, 'spinner')
		os.chdir(cwd)

		
	def copyFile(self, path, file, root):
		if file.getName() in [ 'TRANS.TBL' ]:
			return

		dir	 = os.path.join(root, path)
		fullname = os.path.join(dir, file.getName())
		if not os.path.isdir(dir):
			os.makedirs(dir)

		shutil.copy(file.getFullName(), fullname)
		os.utime(fullname, (file.getTimestamp(), file.getTimestamp()))


	def copyRoll(self, roll, dir):
		tmp = self.mktemp()
		os.makedirs(tmp)
		subprocess.call('mount -o loop -t iso9660 %s %s' %
			  (roll.getFullName(), tmp), shell=True)
		tree = rocks.file.Tree(tmp)
		tree.apply(self.copyFile, dir)
		subprocess.call('umount %s' % tmp, shell=True)
		shutil.rmtree(tmp)


	def stampDisk(self, dir, name, arch, id=1):
		file = os.path.join(dir, '.discinfo')
		if os.path.isfile(file):
			os.unlink(file)
		fout = open(file, 'w')
		fout.write('%f\n' % time.time())
		fout.write('%s\n' % name)
		fout.write('%s\n' % arch)
		fout.write('%d\n' % id)
		fout.close()
			


class RollBuilder_linux(Builder, rocks.dist.Arch):

	def __init__(self, file, command):
		Builder.__init__(self)
		rocks.dist.Arch.__init__(self)
		self.config = rocks.file.RollInfoFile(file)
		self.setArch(self.config.getRollArch())
		self.command = command

	def mkisofs(self, isoName, rollName, diskName):
		Builder.mkisofs(self, isoName, rollName, diskName, diskName)
		
	def signRPM(self, rpm):
	
		# Only sign RPMs that were build on this host.  This
		# allows Rolls to include 3rd party RPMs that will
		# not be signed by the Roll builder.
		
		cmd = "rpm -q --qf '%%{BUILDHOST}' -p %s" % rpm.getFullName()
		buildhost = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.readline()
		hostname  = socket.gethostname()
		
		if buildhost == hostname:
			cmd = 'rpm --resign %s' % rpm.getFullName()
			try:		
				child = pexpect.spawn(cmd)
				child.expect('phrase: ')
				child.sendline()
				child.expect(pexpect.EOF)
				child.close()
			except:
				pass
			subprocess.call("rpm -qp %s --qf " 
				"'%%{name}-%%{version}-%%{release}: "
				"%%{sigmd5}\n'"
				% rpm.getFullName(), shell=True)
		

	def getRPMS(self, path):
		"""Return a list of all the RPMs in the given path, if multiple
		versions of a package are found only the most recent one will
		be included (just like rocks-dist)"""
		
		dict = {}
		tree = rocks.file.Tree(os.path.join(os.getcwd(), path))
		for dir in tree.getDirs():
			for file in tree.getFiles(dir):
				try:
					file.getPackageName()
				except AttributeError:
					continue # skip all non-rpm files
					
				# Skip RPMS for other architecures
				
				if file.getPackageArch() not in self.getCPUs():
					continue
					
				# Resolve package versions
				
				name = file.getUniqueName()
				if not dict.has_key(name) or file >= dict[name]:
					dict[name] = file
					
		# convert the dictionary to a list and return all the RPMFiles
		
		list = []
		for e in dict.keys():
			list.append(dict[e])
		return list


	def spanDisks(self, files, disks=[]):
		"""Given the Roll RPMS and SRPMS compute the size
		of all the files and return a list of files for each disk of 
		the roll.  The intention is for almost all rolls to be one
		CD but for our OS Roll this is not the case."""
		
		
		# Set the roll size to 0 to bypass the disk spanning
		# logic.  The updates Roll does this.
		
		avail = self.config.getISOMaxSize()
		if avail <= 0:
			infinite = 1
		else:
			infinite = 0
		consumed = []
		remaining = []
		
		# Fill the CDs, note that we start with an order of RPMS before
		# SRPMS but this will not be preserved.  A large RPM could
		# be bumped from the CD and SRMPS backfilled in its place.
		
		for file in files:
			if file and infinite:
				consumed.append(file)
			elif file and (avail - file.getSize()) > 0:
				consumed.append(file)
				avail -= file.getSize()
			else:
				remaining.append(file)
		
		id	= len(disks) + 1
		name	= 'disk%d' % id
		size	= self.config.getISOMaxSize() - avail
		disks.append((name, id, size, consumed))
		if len(remaining):
			self.spanDisks(remaining, disks)
		return disks
		

	def getExternalRPMS(self):
		import rocks.roll
		import rocks.gen

		# The distAll distribution includes all of the installed rolls
		# on the system and is used to generate a kickstart files for
		# the everything appliance.  This gives us a list of RPMs that
		# we know we need from the source os/updates CDs.

		print 'making rocks-dist-all'

		cwd = os.getcwd()

		os.environ['RPMHOME'] = os.getcwd()
		distAll = rocks.roll.Distribution(self.getDistArch(), 
			'rocks-dist-all')
		distAll.generate()

		#
		# copy the 'everything' node and graph file into the distro
		#
		shutil.copy(os.path.join('nodes', 'everything.xml'),
			os.path.join(distAll.getPath(), 'build', 'nodes'))
		shutil.copy(os.path.join('graphs', 'default', 'os.xml'),
			os.path.join(distAll.getPath(),
				'build', 'graphs', 'default'))

		basedir = os.path.join(distAll.getPath(), 'build')
		xml = self.command('list.node.xml', [ 'everything',
			'basedir=%s' % basedir, 'eval=n' ] )

		os.chdir(cwd)

		#
		# make sure the XML string is ASCII and not unicode, 
		# otherwise, the parser will fail
		#
		xmlinput = xml.encode('ascii', 'ignore')

		generator = rocks.gen.Generator_linux()
		generator.setArch(self.arch)
		generator.setOS('linux')
		generator.parse(xmlinput)

		rpms = []
		for line in generator.generate('packages'):
			if len(line) and line[0] not in [ '#', '%' ]:
				rpms.append(line)

		# The distOS distribution includes just the source os/update 
		# CDs (already in Roll form).  The distAll distribution is
		# still used for the comps file and the anaconda source 
		# code.  We need this since anaconda and comps are missing
		# from the foreign rolls (os/update CDs).

		print 'making rocks-dist-os'
		del os.environ['RPMHOME']

		distOS = rocks.roll.Distribution(self.getDistArch(), 
			'rocks-dist-os')
		distOS.generate('rolls="%s"' % self.config.getRollRolls())

		#
		# make sure a comps.xml file is present
		#
		comps = os.path.join(distOS.getPath(), 'RedHat', 'base',
			'comps.xml')
		if not os.path.exists(comps):
			print '\n\tCould not find a comps.xml file.'
			print '\tCopy a comps.xml file into the CentOS roll\n'
			sys.exit(-1)

		#
		# use yum to resolve dependencies
		#
		if rocks.version.split('.')[0] == '5':
			pyver='2.4'
		else:
			pyver='2.6'
		sys.path.append('/usr/lib/python%s/site-packages' % pyver)
		sys.path.append('/usr/lib64/python%s/site-packages' % pyver)
		sys.path.append('/usr/lib/python%s/lib-dynload' % pyver)
		sys.path.append('/usr/lib64/python%s/lib-dynload' % pyver)
		import yum

		a = yum.YumBase()
		a.doConfigSetup(fn='%s' % os.path.join(cwd, 'yum.conf'),
			init_plugins=False)
		a.conf.cache = 0
		a.doTsSetup()
		a.doRepoSetup()
		a.doRpmDBSetup()
		a.doSackSetup()
		a.doGroupSetup()

		selected = []
		for rpm in rpms + [ '@base', '@core' ]:
			if rpm[0] == '@':
				group = a.comps.return_group(
					rpm[1:].encode('utf-8'))

				for r in group.mandatory_packages.keys() + \
						group.default_packages.keys():
					if r not in selected:
						selected.append(r)
			elif rpm not in selected:
				selected.append(rpm)

		pkgs = []
		avail = a.pkgSack.returnNewestByNameArch()
		for p in avail:
			if p.name in selected:
				pkgs.append(p)

		done = 0
		while not done:
			done = 1
			results = a.findDeps(pkgs)
			for pkg in results.keys():
				for req in results[pkg].keys():
					reqlist = results[pkg][req]
					for r in reqlist:
						if r.name not in selected:
							selected.append(r.name)
							pkgs.append(r)
							done = 0

		# Now build a list of rocks (required) and non-rocks (optional)
		# rpms and return both of these list.  When the ISOs are created
		# all the required packages are first.
		
		rocks = []
		nonrocks = []
		for rpm in distOS.getRPMS():
			if rpm.getBaseName() in selected:
				rocks.append(rpm)
			else:
				nonrocks.append(rpm)

		return (rocks, nonrocks)


	def makeBootable(self, name):
		import rocks.roll

		print 'Configuring Roll to be bootable ...', name
		os.environ['RPMHOME'] = os.getcwd()
		dist = rocks.roll.Distribution(self.getArch(), 
			'rocks-dist-bootable')
		dist.generate('--notorrent')
		
		# 
		# create a minimal kickstart file. this will get us to the
		# rocks screens.
		# 
		distdir = os.path.join('mnt/cdrom', self.config.getRollName(),
			self.config.getRollVersion(),
			self.config.getRollArch())

		fout = open(os.path.join('disk1', 'ks.cfg'), 'w')
		fout.write('url --url http://127.0.0.1/%s\n' % distdir)
		fout.write('lang en_US\n')
		fout.write('keyboard us\n')
		fout.write('interactive\n')
		fout.write('install\n')
		fout.close()

		import rocks.bootable

		localrolldir = os.path.join(self.config.getRollName(), 
			self.config.getRollVersion(), self.config.getRollArch())

		rolldir = os.path.join(os.getcwd(), 'disk1', localrolldir)

		self.boot = rocks.bootable.Bootable(dist)

		#
		# add isolinux files
		# 
		self.boot.installBootfiles(os.path.join(os.getcwd(), 'disk1'))

		#
		# add the rocks netstage
		# 
		self.boot.installNetstage(rolldir)
	
		return


	def run(self):

		# Make a list of all the files that we need to copy onto the
		# rolls cds.  Don't worry about what the file types are right
		# now, we can figure that out later.
			
		list = []
		if self.config.hasRPMS():
			list.extend(self.getRPMS('RPMS'))
		if self.config.hasSRPMS():
			list.extend(self.getRPMS('SRPMS'))
		for rpm in list:
			self.signRPM(rpm)

		# Make a list of both required and optional packages.  The copy
		# code is here since python is by-reference for everything.
		# After we segregate the packages (old rocks-dist style) add
		# any local rpms to the required list.  This makes sure we
		# pick up the roll-os-kickstart package.
		
		required = []
		if self.config.hasRolls():
			(required, optional) = self.getExternalRPMS()
			for file in list:
				required.append(file)
			print 'Required Packages', len(required)
			print 'Optional Packages', len(optional)
			for file in required: # make a copy of the list
				list.append(file)
			list.extend(optional)


		optional = 0
		for (name, id, size, files) in self.spanDisks(list):
			print 'Creating %s (%.2fMB)...' % (name, size),
			if optional:
				print ' This disk is optional (extra rpms)'
			else:
				print 
				
			root = os.path.join(name,
				self.config.getRollName(),
				self.config.getRollVersion(),
				self.config.getRollArch())
			os.makedirs(root)
			os.makedirs(os.path.join(root, 'RedHat', 'RPMS'))
			os.makedirs(os.path.join(root, 'SRPMS'))
			
			# Symlink in all the RPMS and SRPMS
			
			for file in files:
				try:
					#
					# not RPM files will throw an exception
					# in getPackageArch()
					#
					arch = file.getPackageArch()
				except:
					continue

				if arch == 'src':
					file.symlink(os.path.join(root,
						'SRPMS', file.getName()))
				else:
					file.symlink(os.path.join(root,
						'RedHat', 'RPMS',
						file.getName()))
				if file in required:
					del required[required.index(file)]
					
			if len(required) == 0:
				optional = 1
				
			# Copy the Roll XML file onto all the disks
			shutil.copy(self.config.getFullName(), root)
			
			# Create the .discinfo file
					
			self.stampDisk(name, self.config.getRollName(), 
				self.config.getRollArch(), id)
				
			# make the ISO.  This code will change and move into
			# the base class, and supported bootable rolls.  Get
			# this working here and then test on the bootable
			# kernel roll.
			
			isoname = '%s-%s-%s.%s.%s.iso' % (
				self.config.getRollName(),
				self.config.getRollVersion(),
				self.config.getRollRelease(),
				self.config.getRollArch(),
				name)
				
			if id == 1 and self.config.isBootable() == 1:
				self.makeBootable(name)
			
			self.mkisofs(isoname, self.config.getRollName(), name)


		
class MetaRollBuilder(Builder):

	def __init__(self, files, version):
		self.version = version.strip()
		Builder.__init__(self)
		self.rolls = []
		for file in files:
			try:
				self.rolls.append(rocks.file.RollFile(file))
			except OSError:
				print 'error - %s, no such roll' % file
				sys.exit(-1)

	def run(self):
	
		name = []
		arch = []
		for roll in self.rolls:
			if roll.getRollName() not in name:
				name.append(roll.getRollName())
			if roll.getRollArch() not in arch:
				arch.append(roll.getRollArch())

		name.sort()
		rollName = string.join(name, '+')
		if len(arch) == 1:
			arch = arch[0]
		else:
			arch = 'any'
		name = "%s-%s.%s" % (rollName, self.version, arch)

    		# Create the meta roll
					
		print 'Building %s ...' % name
		tmp = self.mktemp()
		os.makedirs(tmp)
		for roll in self.rolls:
			print '\tcopying %s' % roll.getRollName()
			self.copyRoll(roll, tmp)
		isoname = '%s.disk1.iso' % (name)


		# Find a roll config file for the meta roll.  If any of
		# the rolls are bootable grab the config file for the
		# bootable roll.  Otherwise just use the file from
		# the first roll specified on the command line.

		for roll in self.rolls:
			xml = os.path.join(tmp, roll.getRollName(), 
				roll.getRollVersionString(), 
				roll.getRollArch(),
				'roll-%s.xml' % roll.getRollName())
			config = rocks.file.RollInfoFile(xml)
			if not self.config:
				self.config = config
			elif config.isBootable():
				self.config = config

		#
		# meta rolls can be arbitrarily large, but complain if it
		# is larger than the config found in the code block above
		#
		isosize = self.config.getISOMaxSize()
		self.config.setISOMaxSize(0)

		
		# Build the ISO. complain if we detect that it's too big.
		
		tree = rocks.file.Tree(tmp)
		size = tree.getSize()
		print 'Roll is %.1fMB' % size

		if isosize < size:
			print 'WARNING: Roll %.1fMB is ' % (tree.getSize()) + \
				'larger than computed max ' + \
				'size %.1fMB' % (isosize)
			
		self.stampDisk(tmp, rollName, arch)
		self.mkisofs(isoname, rollName, 'disk1', tmp)

		shutil.rmtree(tmp)

		

class ReArchBuilder(Builder, rocks.dist.Arch):

	def __init__(self, roll, arch):
		Builder.__init__(self)
		rocks.dist.Arch.__init__(self)
		self.setArch(arch)
		self.roll = rocks.file.RollFile(roll)
		
	def run(self):
		roll = self.roll
		isoname = '%s-%s-%s.%s.disk%d.iso'  % \
			(roll.getRollName(),
			roll.getRollVersionString(),
			roll.getRollReleaseString(),
			self.getArch(),
			roll.getRollDiskID())

		print 'Re-Arching %s ...' % roll.getRollName()
		tmp = self.mktemp()
		os.makedirs(tmp)
		print '\tcopying %s' % roll.getRollName()
		self.copyRoll(roll, tmp)
		
		# Fix the directory structure for the new Roll architecture
		
		src = os.path.join(tmp, roll.getRollName(), 
			roll.getRollVersionString(), roll.getRollArch())
		dst = os.path.join(tmp, roll.getRollName(),
			roll.getRollVersionString(), self.getArch())
		shutil.move(src, dst)
		
		# Fix the arch attribute in the roll XML file, and 
		# initialize the self.config to the new XML file.  We
		# unlink the file before writing to avoid any read-only
		# permission error (non-root can run this code)
		
		xml = rocks.file.RollInfoFile(os.path.join(dst, 
			'roll-%s.xml' % roll.getRollName()))
		xml.setRollArch(self.getArch())
		
		os.unlink(xml.getFullName())
		file = open(xml.getFullName(), 'w')
		file.write(xml.getXML())
		file.close()
		
		self.config = rocks.file.RollInfoFile(xml.getFullName())
		
		
		# Create a new .discinfo file and create the ISO 

		self.stampDisk(tmp, roll.getRollName(), self.getArch(), 
			roll.getRollDiskID())
		self.mkisofs(isoname, roll.getRollName(), 
			'disk%d' % roll.getRollDiskID(), tmp)

		shutil.rmtree(tmp)
		     

class RollBuilder_sunos(Builder, rocks.dist.Arch):
	
	def __init__(self, xml_file, command):
		Builder.__init__(self)
		
		self.config = rocks.file.RollInfoFile(xml_file)
	
		self.tmp_dir = os.getcwd()
		self.disc_dir = os.path.join(self.tmp_dir, 'cdrom')
		self.roll_dir = os.path.join(self.disc_dir,
			self.config.getRollName())
		self.vers_dir = os.path.join(self.roll_dir,
			self.config.getRollVersion())
		self.arch_dir = os.path.join(self.vers_dir,
			self.config.getRollArch())
		self.prod_dir = os.path.join(self.arch_dir,
			'Solaris_10', 'Product')
		os.makedirs(self.disc_dir)
		os.makedirs(self.roll_dir)
		os.makedirs(self.prod_dir)

		self.xml_file = xml_file
		self.command = command

	def run(self):
		
		# Transfer all packages from PKGS to Products
		# directory. All packages are in file-system format.
		subprocess.call('pkgtrans %s %s all' %
			(os.path.join(self.tmp_dir,'PKGS'),
			 self.prod_dir), shell=True)

		# Look for the patches directory. Some Solaris packages,
		# such as Sun Studio 12u1 will need to patch Solaris 10.
		# Such patches can come from within Rolls
		src_patch_dir = os.path.join(self.tmp_dir, 'PATCHES')
		if os.path.exists(src_patch_dir) and len(os.listdir(src_patch_dir)) > 0:
			self.patch_dir = os.path.join(self.arch_dir,
				'Solaris_10', 'Patches')
			os.makedirs(self.patch_dir)
			cwd = os.getcwd()
			os.chdir('PATCHES')
			subprocess.call('find . | cpio -mpud %s' % self.patch_dir, shell=True)
			os.chdir(cwd)
		# Copy the roll-rollname.xml  file
		shutil.copy(os.path.join(self.tmp_dir, self.xml_file),
			os.path.join(self.arch_dir,self.xml_file))

		# Create a .cdtoc file
		self.stampDisk()
		
		# Write the CD
		isoname = '%s-%s-%s.%s.iso' % (self.config.getRollName(), 
			self.config.getRollVersion(),
			self.config.getRollRelease(),
			self.config.getRollOS())
			
		self.mkisofs(isoname, self.config.getRollName(), self.config.getRollName(), self.disc_dir)

	def stampDisk(self):
		#Builder.stampDisk(self, self.disc_dir, 
		#	self.config.getRollName(), self.config.getRollArch())
		
		file = os.path.join(self.disc_dir,'.cdtoc')
		if os.path.isfile(file):
			os.unlink(file)
		fout = open(file,'w')
		fout.write('PRODNAME=%s\n' % self.config.getRollName())
		fout.write('PRODVERS=%s\n' % self.config.getRollVersion())
		fout.write('PRODARCH=%s\n' % self.config.getRollArch())
		fout.close()
		        
class Command(rocks.commands.create.command):
	"""
	Create a roll.  You may specify either a single XML file to build
	one Roll or a list of ISO files to build a Meta Roll.

	<arg type='string' name="roll" repeat='1'>
	Either a list of Roll ISO files or the name of a single Roll XML
	description file.  If a list of Roll ISO files to be merge together 
	into a single Roll.  Otherwise the single argument is assumed to
	be the name of the XML file generated by the top level Makefile in
	the Roll's source.
	</arg>

	<example cmd='create roll roll-base.xml'>
	Creates the Rocks Base Roll from the roll-base.xml description file.
	</example>
	
	<example cmd='create roll base*iso kernel*iso'>
	Create a composite Roll from a list of Roll ISOs.
	</example>

	<related>add roll</related>
	<related>remove roll</related>
	<related>enable roll</related>
	<related>disable roll</related>
	<related>list roll</related>
	"""

	def run(self, params, args):
		
		# Set Roll Builder to correct OS
		roller = getattr(rocks.commands.create.roll,
			'RollBuilder_%s' % (self.os))
		if len(args) == 1:
			base, ext = os.path.splitext(args[0])
			if ext == '.xml':
				builder = roller(args[0], self.command)
			else:
				self.abort('missing xml file')
		elif len(args) > 1:
			for arg in args:
				base, ext = os.path.splitext(arg)
				if not ext == '.iso':
					self.abort('bad iso file')
			builder = MetaRollBuilder(args,
				self.command('report.version'))
		else:
			self.abort('no arguments')
			
		builder.run()


RollName = "base"
