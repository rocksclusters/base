#!/opt/rocks/usr/bin/python
#
# $Id: build-updates-img.py,v 1.9 2009/03/04 01:32:13 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		           version 5.1  (VI)
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
# $Log: build-updates-img.py,v $
# Revision 1.9  2009/03/04 01:32:13  bruno
# attributes work for frontend installs
#
# Revision 1.8  2008/10/18 00:56:03  mjk
# copyright 5.1
#
# Revision 1.7  2008/05/30 22:15:16  bruno
# can now install a frontend off CD with the distro moved to
# /export/rocks/install
#
# Revision 1.6  2008/05/23 18:59:31  anoop
# Small changes to the base roll to make a cleaner build
#
# Revision 1.5  2008/05/22 21:02:07  bruno
# rocks-dist is dead!
#
# moved default location of distro from /export/home/install to
# /export/rocks/install
#
# Revision 1.4  2008/03/06 23:41:46  mjk
# copyright storm on
#
# Revision 1.3  2007/12/20 21:58:59  bruno
# fixes for RHEL 5 update 1
#
# Revision 1.2  2007/12/13 02:53:40  bruno
# can now build a bootable kernel CD and build a physical frontend with V
# on RHEL 5 update 1
#
# Revision 1.1  2007/12/10 21:28:35  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.12  2006/12/19 21:32:52  bruno
# remove print statement
#
# Revision 1.11  2006/12/19 20:35:03  bruno
# look in the local roll RPMS directory for the latest built RPMS
#
# Revision 1.10  2006/09/19 21:14:38  bruno
# thin is in
#
# Revision 1.9  2006/09/18 17:33:26  bruno
# weight-loss program
#
# Revision 1.8  2006/09/11 22:47:03  mjk
# monkey face copyright
#
# Revision 1.7  2006/09/08 18:28:57  bruno
# add sharutils -- this includes uudecode which is used in the restore roll
# to reconstruct saved files
#
# Revision 1.6  2006/08/10 00:09:26  mjk
# 4.2 copyright
#
# Revision 1.5  2006/06/19 20:41:04  bruno
# more build tweaks
#
# Revision 1.4  2006/06/15 23:07:35  bruno
# vnc for monitoring installations is ready for the beta
#
# Revision 1.3  2006/06/05 17:57:35  bruno
# first steps towards 4.2 beta
#
# Revision 1.2  2006/03/29 02:38:17  bruno
# move all package installation over to updates.img
#
# Revision 1.1  2006/03/23 01:05:28  bruno
# first draft at support for building an updates.img
#
#

import string
import popen2
import rocks.kickstart
import os
import os.path
import sys
import rocks.bootable
from rocks.dist import DistError


class Distribution:

	def __init__(self, arch, name='rocks-dist'):
		self.arch = arch
		self.tree = None
		self.name = name

		#
		# the 'native' cpu is always first
		#
		self.cpus = []
		i86cpus = [ 'i686', 'i586', 'i486', 'i386' ]

		native = os.uname()[4]
		self.cpus.append(native)

		if native in i86cpus:
			self.cpus += i86cpus

		self.cpus.append('noarch')

	
	def getPath(self):
		return os.path.join(self.name, self.arch)
		
	def generate(self, flags=""):
		rocks.util.system('/opt/rocks/bin/rocks create distro')
		self.tree = rocks.file.Tree(os.path.join(os.getcwd(), 
			self.getPath()))
		
	def getRPMS(self):
		return self.tree.getFiles(os.path.join('RedHat', 'RPMS'))

	def getSRPMS(self):
		return self.tree.getFiles('SRPMS')
		
	def getRPM(self, name):
		l = []
		for rpm in self.getRPMS():
			try:
				if rpm.getPackageName() == name:
					l.append(rpm)
			except:
				pass
		if len(l) > 0:
			return l
		return None

	

class App(rocks.app.Application):
	"""Preps the initrd for the rocks-boot package by
	using the native kernel pakcage to build a custom
	initrd image. Uses the kickstart Application to locate 
	packages in the local distribution."""
	
	def __init__(self, argv):
		rocks.app.Application.__init__(self, argv)
		self.usage_name = 'Build updates.img'
		self.usage_version = '@VERSION@'
		

	def thinkLocally(self, name):
		import rocks.file

		localtree = rocks.file.Tree(os.path.join(os.getcwd(),
			'..', '..', 'RPMS'))	

		locallist = {}
		for dir in localtree.getDirs():
			if 'CVS' in string.split(dir, os.sep):
				continue # skip CVS metadata

			for rpm in localtree.getFiles(dir):
				try:
					if name == rpm.getBaseName():
						return rpm
				except:
					pass
		

		return None


	def run(self):
		self.dist = Distribution(self.getArch())
		self.dist.generate()

		self.boot = rocks.bootable.Bootable(self.dist)

		rpms = [
			'createrepo',
			'firerox', 
			'foundation-libxml2',
			'foundation-python',
			'foundation-python-extras',
			'foundation-python-xml',
			'foundation-redhat',
			'keyutils-libs',
			'keyutils-libs-devel',
			'rocks-bittorrent',
			'rocks-command',
			'rocks-dbreport',
			'rocks-ekv',
			'rocks-kickstart', 
			'rocks-kpp',            
			'rocks-piece-pipe',
			'rocks-pylib',
			'rocks-screens',
			'sharutils',
			'squashfs-tools'
		]

		for rpmname in rpms:
			rpm = self.thinkLocally(rpmname)
			if not rpm:
				rpm = self.boot.getBestRPM(rpmname)

			try:
				print 'rpm: ', rpmname
				self.boot.applyRPM(rpm, 
					os.path.join(os.getcwd(), 'extra'),
					flags='--noscripts --excludedocs')
			except:
				print "couldn't apply RPM (%s)" % (rpmname)
				raise

		#
		# nuke un-needed files
		#
		cwd = os.getcwd()
		os.chdir('extra')

		cmd = 'find . -type f -name *.pyc -or -name *.pyo | xargs rm -f'
		os.system(cmd)
		
		cmd = 'rm -f opt/rocks/redhat/var/lib/rpm/__db*'
		os.system(cmd)

		cmd = 'rm -f opt/rocks/lib/python2.4/' + \
					'distutils/command/wininst-*exe'
		os.system(cmd)

		cmd = 'find . -type d -name Doc -or -name docs -or -name doc' +\
			' | xargs rm -rf'
		os.system(cmd)

		cmd = 'find opt/rocks/lib/python2.4 -type d ' + \
			'-name test -or -name tests | xargs rm -rf'
		os.system(cmd)

		for i in [ 'numarray', 'Numeric', 'numpy', 'POW', 'gtk-2.0' ]:
			cmd = 'rm -rf opt/rocks/lib/python2.4/site-packages/'
			cmd += '%s' % (i)
			os.system(cmd)


		os.chdir(cwd)

		return


# Main
app = App(sys.argv)
app.parseArgs()
app.run()

