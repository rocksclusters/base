#! /opt/rocks/bin/python
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
# $Log: media.py,v $
# Revision 1.18  2012/11/27 00:48:40  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.17  2012/05/06 05:48:47  phil
# Copyright Storm for Mamba
#
# Revision 1.16  2012/04/01 16:45:04  phil
# Eject CD now looks to be working on 6.
#
# Revision 1.15  2012/03/17 05:05:07  phil
# eject was not working in 6.
# Backed out the "hack" installed rocks-pylib in two places
#
# Revision 1.14  2011/07/23 02:30:49  phil
# Viper Copyright
#
# Revision 1.13  2010/09/07 23:53:08  bruno
# star power for gb
#
# Revision 1.12  2009/05/01 19:07:08  mjk
# chimi con queso
#
# Revision 1.11  2008/10/18 00:56:02  mjk
# copyright 5.1
#
# Revision 1.10  2008/03/26 18:24:55  bruno
# another whack at ejecting the CD early
#
# Revision 1.9  2008/03/24 18:55:56  bruno
# handle lighttpd and apache style directory listings
#
# Revision 1.8  2008/03/21 23:07:53  bruno
# tweak code to get rolls off a CD/DVD
#
# Revision 1.7  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.6  2007/12/10 21:28:35  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.5  2007/06/23 04:03:24  mjk
# mars hill copyright
#
# Revision 1.4  2006/09/15 00:02:33  bruno
# there are cases where the CD doesn't immediately un-mount
# (it could be a slow finishing operation).
#
# try 10 times to unmount the CD.
#
# Revision 1.3  2006/09/11 22:47:23  mjk
# monkey face copyright
#
# Revision 1.2  2006/08/10 00:09:41  mjk
# 4.2 copyright
#
# Revision 1.1  2006/06/08 20:04:20  bruno
# added class to interface with rocks media (CDs and network)
#
#
#

import os
import os.path
import string
import rocks

class Media:

	def mounted(self):
		"Returns true if /tmp/rocks-cdrom device or /mnt/cdrom is mounted"

		rv = 0
		f = open('/proc/mounts','r')
		for line in f.readlines():
			if line.find('/tmp/rocks-cdrom') >= 0:
				rv = 1
				break
			if line.find('/mnt/cdrom') >= 0:
				rv = 1
				break
		f.close()
		return rv


	def mountCD(self, prefix="/"):
		"""Try to mount the CD. Returns 256 if mount failed
		(no disk in drive), 0 on success."""

		if self.mounted():
			return 1
			
		mountpoint = os.path.join(prefix, 'mnt', 'cdrom')

		#
		# loader creates '/tmp/rocks-cdrom' -- the cdrom device
		#
		rc = os.system('mount -o ro /tmp/rocks-cdrom'
			+ ' %s > /dev/null 2>&1' % (mountpoint))

		return rc


	def umountCD(self, prefix="/"):
		if not self.mounted():
			return
              
		mountpoint = os.path.join(prefix, 'mnt', 'cdrom')
		os.system('umount %s > /dev/null 2>&1' % (mountpoint))
                return


	def ejectCD(self):
		self.umountCD()

		#
		# there are cases where the CD doesn't immediately un-mount
		# (it could be a slow finishing operation).
		#
		# try 10 times to unmount the CD.
		#
		i = 0
		while self.mounted() and i < 10:
			self.umountCD()
			i += 1

		#
		# the 'eject' utility requires '/etc/fstab' to exist
		#
		os.system('touch /etc/fstab')

		#
		# loader creates the cdrom device '/tmp/rocks-cdrom'
		#
		if rocks.version_major == '6':
			ejectcmd = '/tmp/updates/usr/sbin/eject'
		else:
			ejectcmd = '/usr/bin/eject'

		cmd = '%s /tmp/rocks-cdrom > /dev/null 2>&1' % ejectcmd
		os.system(cmd)

		return


	def getCDInfo(self):
		self.mountCD()

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


	def getCDInfoFromXML(self):
		retval = (None, None, None)

		self.mountCD()
		cdtree = rocks.file.Tree('/mnt/cdrom')
		for dir in cdtree.getDirs():
			for file in cdtree.getFiles(dir):
				try:
					xmlfile = rocks.file.RollInfoFile(
							file.getFullName())

					rollname = xmlfile.getRollName()
					rollversion = xmlfile.getRollVersion()
					rollarch = xmlfile.getRollArch()

					if rollname != None and \
						rollversion != None and \
							rollarch != None:

						retval = (rollname, \
							rollversion, rollarch)
						break

				except:
					continue

			if retval != (None, None, None):
				break

		return retval


	def getId(self):
		"""Get the Id of the physical roll CD."""

		(timestamp, name, archinfo, diskid) = self.getCDInfo()

		if name != None and diskid != None:
			str = '%s - Disk %s' % (name, diskid)
		else:
			str = 'Not Identified'

		return str
		

	def listRolls(self, url, diskid, rollList):
		if os.path.exists('/tmp/updates/rocks/bin/wget'):
			wget = '/tmp/updates/rocks/bin/wget'
		else:
			wget = '/usr/bin/wget'

		cmd = "%s --timeout=15 --tries=2 -O - -nv %s 2>&1 " % \
			(wget, url)

		for line in os.popen(cmd).readlines():
			l = string.split(line, '"')

			if l[0] == '<a href=':
				#
				# apache style listing
				#
				filename = l[1]
			elif len(l) > 2 and l[2] == '><a href=':
				#
				# lighttpd style listing
				#
				filename = l[3]
			else:
				continue
				
			if len(filename) > 0 and filename[-1] == '/':
				#
				# this is a directory
				#
				dir = filename[:-1]
				
				if dir in [ '.', '..']:
					continue

				if dir == 'RedHat':
					urlList = url.split('/')

					rollname = urlList[-3]
					rollversion = urlList[-2]
					rollarch = urlList[-1]

					rollList.append((rollname,
						rollversion, rollarch, diskid))
				else:
					self.listRolls(os.path.join(url, dir),
						diskid, rollList)

		return

