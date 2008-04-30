# $Id: __init__.py,v 1.30 2008/03/06 23:41:35 mjk Exp $
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
# $Log: __init__.py,v $
# Revision 1.30  2008/03/06 23:41:35  mjk
# copyright storm on
#
# Revision 1.29  2008/02/13 01:06:03  anoop
# Now makes use of the OS column in the rolls table when adding
# roll information to the database. This way we can keep solaris
# and linux rolls separate even with the same roll name
#
# Revision 1.28  2008/01/29 01:18:13  bruno
# fix kreative grmmr
#
# Revision 1.27  2008/01/16 18:10:36  bruno
# make sure apache can traverse the roll's directory after one executes:
#
#     rocks add roll
#
# Revision 1.26  2007/11/09 23:28:25  anoop
# Bug Fix
#
# Revision 1.25  2007/11/09 22:09:41  anoop
# Changed architecture to i386 from i86pc
#
# Now uses the "os" column when adding rolls on Solaris
#
# Revision 1.24  2007/10/31 23:25:15  anoop
# Minor Bug fixes
#
# Revision 1.23  2007/10/31 23:12:44  anoop
# Actually change what you want to change
#
# Revision 1.22  2007/10/31 23:04:16  anoop
# Adding more rolls capability, so that Solaris Rolls start to look more
# like Linux rolls with version numbers and architecture separated directories.
#
# Revision 1.21  2007/10/29 01:07:34  anoop
# Empty the roll_info dictionary for every iso file.
# Quietly copy the CD on to disc
# Don't be inside the cdrom directory and then try to unmount it
#
# Revision 1.20  2007/10/28 23:24:12  anoop
# *** empty log message ***
#
# Revision 1.19  2007/10/28 23:21:21  anoop
# mkdirhier is a bash command, not a python function. Also make sure
# a directory exists before trying to delete it. Catching an OSError exception
# is not the best way to go about this.
#
# Revision 1.18  2007/10/28 01:06:59  anoop
# Forgot a *
#
# Revision 1.17  2007/10/28 00:38:50  anoop
# Major changes to rocks add roll.
# Now calls native code for copying Linux and Solaris Rolls
# to disk. rocks-dist copyroll called for non-native Linux Rolls.
# Also, rocks add roll is now cross OS compatible. It can copy
# any Solaris Roll to a Linux host.
#
# Revision 1.16  2007/10/11 00:26:35  anoop
# Minor Bug fix.
#
# On Linux, rocks add roll does not run "rocks-dist copyroll" anymore
# It runs native code. This is still primitive code that needs to accomadate
# reading non-Rocks OS CDs and also being slightly more verbose. There's
# always tomorrow for that.
#
# Revision 1.15  2007/10/10 23:07:58  anoop
# Thinning down Pylib a little more. Moving classes that are used
# by single commands into the command structure away from pylib.
# The roll-<rollname>.xml file now supports "os" parameter
#
# Revision 1.14  2007/10/03 22:14:06  anoop
# Changes to internal functioning of the "rocks create roll" command. All
# classes except Command class moved to rollbuilder.py under pylib
# Any changes that need to be made to roll building need to go to rollbuilder.py
# in pylib.
#
# Minor changes to "rocks add roll" command as well. Functionality for this
# will be moved up to pylib as well.
#
# Revision 1.13  2007/07/04 01:47:37  mjk
# embrace the anger
#
# Revision 1.12  2007/07/02 19:43:58  bruno
# more params/flags cleanup
#
# Revision 1.11  2007/06/23 03:54:51  mjk
# - first pass at consistency
# - still needs some docstrings
# - argument processors take SQL wildcards
# - add cannot run twice (must use set)
# - dump does sets not just adds
#
# Revision 1.10  2007/06/19 16:42:40  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.9  2007/06/16 02:39:50  mjk
# - added list roll commands (used for docbook)
# - docstrings should now be XML
# - added parser for docstring to ASCII or DocBook
# - ditched Phil's Network regex stuff (will come back later)
# - updated several docstrings
#
# Revision 1.8  2007/06/07 21:23:03  mjk
# - command derive from verb.command class
# - default is MustBeRoot
# - list.command / dump.command set MustBeRoot = 0
# - removed plugin non-bugfix
#
# Revision 1.7  2007/06/05 17:02:59  bruno
# added 'clean' flag to 'rocks add roll'
#
# Revision 1.6  2007/05/31 19:35:41  bruno
# first pass at getting all the 'help' consistent on all the rocks commands
#
# Revision 1.5  2007/05/30 22:08:32  bruno
# added help
#
# Revision 1.4  2007/05/10 20:37:00  mjk
# - massive rocks-command changes
# -- list host is standardized
# -- usage simpler
# -- help is the docstring
# -- host groups and select statements
# - added viz commands
#
# Revision 1.3  2007/02/27 01:53:57  mjk
# - run(self, args) => run(self, flags, args)
# - replaced rocks list host xml with more complete code
# - replaced rocks lust node xml with kpp shell (not a command now)
#
# Revision 1.2  2007/02/08 17:31:25  mjk
# Added root check for root-only commands
# Added syslog tracking to record changes to the cluster
#
# Revision 1.1  2007/02/05 23:29:19  mjk
# added 'rocks add roll'
# added plugin_* facility
# added 'rocks sync user' (plugin-able)
#


import os
import stat
import time
import sys
import string
import rocks.commands
import rocks.file
import popen2

class RollHandler:
	def __init__(self, arch, os, db):
		# Setup the initial variables
		self.host_os = os				# Host Operating System
		self.host_arch = arch			# Host Architecture
		self.db = db 					# Database Connection

		self.cdrom_mount = '/mnt/cdrom'	# Default(Linux) mount point
		if self.host_os == 'sunos':		# Solaris CDROM mount point
			self.cdrom_mount = '/cdrom'

		self.roll_info = {}
		
	def mount_iso(self, iso):
		"""Mount the ISO image given. Calls the Host OS specific
		mount function"""
		f = getattr(self, 'mount_iso_%s' % (self.host_os))
		f(iso)

	def mount_iso_linux(self, iso):
		"""Mount the ISO Image on Linux"""
		os.system('mount -o loop %s %s' % (iso, self.cdrom_mount))

	def mount_iso_solaris(self, iso):
		"""Mount the ISO Image on Solaris"""
		r, w = popen2.popen2('lofiadm -a %s' % os.path.abspath(iso))
		self.lofidev = r.read().strip()
		os.system('mount -F hsfs %s %s' % (self.lofidev, self.cdrom_mount))
	
	def umount_iso(self):
		"""Unmount the ISO Image. Calls the host OS specific umount
		command"""
		f = getattr(self, 'umount_iso_%s' % (self.host_os))
		f()

	def umount_iso_linux(self):
		"""Unmount the ISO image on linux"""
		os.system('umount %s' % self.cdrom_mount)

	def umount_iso_sunos(self):
		"""Unmount the ISO image on Solaris"""
		os.system('umount %s' % self.cdrom_mount)
		os.system('lofiadm -d %s' % self.lofidev)

	def is_cd_mounted(self):
		f = getattr(self, 'is_cd_mounted_%s' % self.host_os)
		return f()

	def is_cd_mounted_linux(self):
		cmd = 'mount | grep %s' % self.cdrom_mount
		if os.system(cmd):
			return False
		return True

	def is_cd_mounted_sunos(self):
		""" Check if the CD is mounted at the given 
		mount point. If not, return 0"""
		# Run the mount command, and check if the mount
		# point is specified in the list of mounted filesystems
		cmd = 'mount | grep \\^%s' % self.cdrom_mount
		if os.system(cmd):
			return False
		return True

	def copy_cd(self, clean):
		"""Copy all the Rolls from the CD to Disk"""

		# Read the CD. The read_cd function populates
		# the self.roll_info hash. This hash contains roll
		# information about all the rolls present on disc.
		# Always empty the roll_info dictionary for every
		# CD.
		self.roll_info = {}
		self.read_cd()

		# If the roll_info hash is empty, that means there are
		# no Rocks recognizable rolls on the Disc. This mean
		# it may just be a normal OS CD like CentOS, RHEL, Scientific
		# Linux or Solaris. In any case it's a foreign CD, and should
		# be treated as such.
		if len(self.roll_info) == 0:
			self.copy_foreign_cd(clean)
			return
		
		# If we've come this far that means the disc has rolls on it.
		# So for all rolls present, copy into the rolls directory.
		for i in self.roll_info:
			self.copy_roll(clean, self.roll_info[i])
			
	def copy_roll(self, clean, roll_info):
		"""Copy the roll on to disk"""
		# See what the OS of the roll is and call the appropriate
		# copy_roll command
		f = getattr(self,'copy_%s_roll' % roll_info.getRollOS())
		f(clean, roll_info)

	def copy_linux_roll(self, clean, roll_info):
		"""The Roll is a Linux Roll, so copy it the Linux way"""

		# Get name, version, architecture of Roll
		roll_name = roll_info.getRollName()
		roll_vers = roll_info.getRollVersion()
		roll_arch = roll_info.getRollArch()
		roll_os   = roll_info.getRollOS()
		self.rolls_dir = '/export/home/install/rolls'
		# Get the destination, ie. where should the roll be put.
		# This is always rolls_directory/roll_name/
		roll_dir = os.path.join(self.rolls_dir, roll_name)
		# Clean out the existing roll directory if asked
		
		if clean:
			if os.path.exists(roll_dir):
				print 'Cleaning %s from the Rolls Directory' % roll_name
				self.clean_dir(roll_dir)
			os.makedirs(roll_dir)
		# Finally copy the roll to the HD
		sys.stdout.write('Copying %s to Rolls.....' % roll_name)
		sys.stdout.flush()
		cwd = os.getcwd()
		os.chdir(os.path.join(self.cdrom_mount,roll_name))
		os.system('find . ! -name TRANS.TBL -print'
						' | cpio -mpud %s'
						% roll_dir)

		# after copying the roll, make sure everyone (apache included)
		# can traverse the directories
		os.system('find %s -type d -exec chmod a+rx {} \;' % roll_dir)

		# Insert the roll information into the database. Insert
		# into the database only in case it already doesn't exist
		rows = self.db.execute('select * from rolls where'	\
				' name="%s" and version="%s" and arch="%s"' \
				' and os="%s"'
				% (roll_name, roll_vers, roll_arch, roll_os))
		if not rows:
			db_cmd = 'insert into rolls (name, version, arch, enabled)'\
				' values("%s", "%s", "%s", "no")'	\
				% (roll_name, roll_vers, roll_arch)
			self.db.execute(db_cmd)
		
		os.chdir(cwd)
	
	def copy_sunos_roll(self, clean, roll_info):
		"""This function copies a Solaris Roll on to disk"""

		# Get info on the Roll
		roll_name = roll_info.getRollName()
		roll_vers = roll_info.getRollVersion()
		roll_arch = roll_info.getRollArch()
		roll_os = roll_info.getRollOS()

		roll_dir = os.path.join('/export/home/install',
					'jumpstart/rolls/',
					roll_name)
		
		if clean:
			if os.path.exists(roll_dir):
				print 'Cleaning %s from the Rolls Directory' % roll_name
				self.clean_dir(roll_dir)
			os.makedirs(roll_dir)

		# Navigate to the Roll directory <cdrom>/<roll_name>
		# and just copy everything into the media directory
		cwd = os.getcwd()
		os.chdir(os.path.join(self.cdrom_mount, roll_name))
		print 'Copying SunOS: %s to %s' % (roll_name, roll_dir) 
		os.system('find . ! -name TRANS.TBL'
				' | cpio -mpud %s' % roll_dir)

		# after copying the roll, make sure everyone (apache included)
		# can traverse the directories
		os.system('find %s -type d -exec chmod a+rx {} \;' % roll_dir)

		rows = self.db.execute(
				"select * from rolls where"
				" name='%s' and Arch='%s' and OS='%s' and version='%s'"
				% (roll_name, roll_arch, roll_os, roll_vers))
		if rows:
			pass
		else:
			self.db.execute("insert into rolls (name, arch, os, version)"
					" values ('%s','%s','%s', '%s')" %
					(roll_name, roll_arch, roll_os, roll_vers))
		os.chdir(cwd)

	def read_cd(self):
		"""This function reads the CD and populates
		information about the rolls that are on the CD"""

		# Check to see if roll-<name>.xml files are present
		r, w = popen2.popen2('find %s -type f -name roll-\*.xml' % self.cdrom_mount)
		f_list = r.readlines()
		
		# Get roll information from all the Rolls present on the CD
		for i in f_list:
			roll = rocks.file.RollInfoFile(i.strip())
			self.roll_info[roll.getRollName()] = roll

	def copy_foreign_cd(self, clean):
		"""Copy a CD which is not the Standard Rocks Roll CD"""

		# Check the OS of the CD. This is pretty easily discernable.
		# .discinfo file in the root of the CD implies an RHEL based disc
		# .cdtoc file in the root of the CD implies a Solaris 10 disc
		# Pass off to appropriate handling functions
		if os.path.exists(os.path.join(self.cdrom_mount, '.discinfo')):
			self.copy_foreign_cd_linux(clean)
		if os.path.exists(os.path.join(self.cdrom_mount, '.cdtoc')):
			self.copy_foreign_cd_sunos(clean)

	def copy_foreign_cd_linux(self, clean):
		"""Copy a Linux OS CD. This is when the CD is a standard CentOS
		RHEL or Scientific Linux CD"""

		# For now just call the rocks-dist command. This needs to
		# change in the future.
		args = ''
		if clean:
			args = '--clean'
		os.system('rocks-dist %s copyroll' % args)

	def copy_foreign_cd_sunos(self, clean):
		"""Copy a standard Solaris CD"""
		
		js_dir = '/export/home/install/jumpstart/'
		# For now, hardcode the architecture, because we only support
		# one architecture. No others. This should really be obtained
		# from the database.
		arch = 'i386'
		roll_os = 'sunos'

		# Make sure it's a Solaris CD/DVD
		file = open(os.path.join(self.cdrom_mount, '.cdtoc'), 'r')
		for i in file.readlines():
			if i.startswith('#'):
				continue
			if i.startswith('PRODNAME'):
				prod_name = i.split('=')[1].strip()
			if i.startswith('PRODVERS'):
				prod_vers = i.split('=')[1].strip()
		if not prod_name.startswith('Solaris'):
			print "Not Valid Solaris CD"
			return

		# If we've got this far, that means that we can continue
		# and copy the Solaris DVD.
		print prod_name, prod_vers
		roll_dir = os.path.join(js_dir, 'rolls', prod_name, prod_vers, arch)
		
		# Set the source and destination directories for cpio
		# These default to the CDROM for source and the roll directory
		# for destination
		cpio_src_dir = self.cdrom_mount
		cpio_dest_dir = roll_dir

		# If clean flag is specified, remove the roll directory
		if clean:
			if os.path.exists(roll_dir):
				print "Cleaning %s from Rolls directory"
				self.clean_dir(roll_dir)
			os.makedirs(roll_dir)

		# If it's the companion DVD, the filesystem layout is a 
		# tad bit different. Treat it as such, and set cpio source
		# and destination directories appropriately.
		if prod_name == 'Solaris_Software_Companion':
			cpio_src_dir = os.path.join(self.cdrom_mount, 
					'Solaris_Software_Companion',
					'Solaris_%s' % arch, 'Packages')
			cpio_dest_dir = os.path.join(roll_dir, 'Solaris_10','Product')
			
		if not os.path.exists(cpio_dest_dir):
			os.makedirs(cpio_dest_dir)

		# Now that we know it's some sort of Solaris CD,
		# add an entry to the database
		rows = self.db.execute(
				"select * from rolls where"
				" name='%s' and Arch='%s' and OS='%s' and version='%s'"
				% (prod_name, arch, roll_os, prod_vers))
		if rows:
			pass
		else:
			self.db.execute("insert into rolls (name, arch, os, version)"
					" values ('%s','%s','%s', '%s')" %
					(prod_name, arch, roll_os, prod_vers))

		# ... and now copy the CD over to the HDD.
		cwd = os.getcwd()
		os.chdir(cpio_src_dir)
		os.system('find . -print | cpio -mpud %s' % cpio_dest_dir)
		os.chdir(cwd)
		return

	def clean_dir(self, dir):
		# This function cleans up a given directory and
		# removes it from the face of the harddisk
		for root, dirs, files in os.walk(dir, topdown=False):
			for name in files:
				os.remove(os.path.join(root, name))
			for name in dirs:
				os.rmdir(os.path.join(root, name))
		os.removedirs(dir)
	
class Command(rocks.commands.add.command):
	"""
	Add Roll ISO images to this machine's roll directory. This command
	copies all files in the ISOs to a directory under /home/install/rolls.

	<arg optional='1' type='string' name='roll' repeat='1'>
	A list of Roll ISO images to add to /home/install/rolls. If no list is
	supplied, then if a roll is mounted on /mnt/cdrom, it will be copied
	into /home/install/rolls.
	</arg>
		
	<param type='bool' name='clean'>
	If set, then remove all files from any existing rolls of the same
	name, version, and architecture before copying the contents of the
	Rolls onto the local disk.  This parameter should not be set
	when adding multi-CD Rolls such as the OS Roll, but should be set
	when adding single Roll CDs such as the Grid Roll.
	</param>
	
	<example cmd='add roll clean=1 kernel*iso'>
	Adds the Kernel Roll to local Roll directory.  Before the Roll is
	added the old Kernel Roll packages are removed from the Roll directory.
	</example>
	
	<example cmd='add roll kernel*iso pvfs2*iso ganglia*iso'>
	Added the Kernel, PVFS, and Ganglia Rolls to the local Roll
	directory.
	</example>
	"""

	def run(self, params, args):
		# Check if we're doing a clean copy or an overwrite
		(self.clean, ) = self.fillParams([('clean', 'n')])
		self.clean = self.str2bool(self.clean)
		
		# Get a list of all the iso files mentioned in
		# the command line. Make sure we get the complete 
		# path for each file.
		iso_list = []
		for i in args:
			i = os.path.join(os.getcwd(),i)
			if os.path.exists(i) and i.endswith('.iso'):
				iso_list.append(i)
			else:
				print "Cannot find %s or %s "\
					"is not and ISO image" % (i,i)
		
		# Create a Rollhandler Instance. This handles rolls
		# for both Solaris and Linux.
		roll_handler = RollHandler(self.arch, self.os, self.db)

		# If no isos are mentioned then check if cdrom is mounted
		# and perform a copyroll. Otherwise perform a copyroll
		# on all CDs
		if (len(iso_list) == 0):
			if roll_handler.is_cd_mounted():
				roll_handler.copy_cd(self.clean)
			else:
				self.abort('CDROM not mounted')
		else:
			for i in iso_list:
				roll_handler.mount_iso(i)
				roll_handler.copy_cd(self.clean)
				roll_handler.umount_iso()
