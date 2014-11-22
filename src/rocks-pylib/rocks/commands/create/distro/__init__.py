# $Id: __init__.py,v 1.17 2012/11/27 00:48:11 phil Exp $
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
# Revision 1.17  2012/11/27 00:48:11  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.16  2012/11/16 03:52:56  clem
# before running rocks create distro check if lock file is already in place
#
# Revision 1.15  2012/05/06 05:48:21  phil
# Copyright Storm for Mamba
#
# Revision 1.14  2012/04/05 22:00:36  phil
# Now have flag to not create packages.md5. Temporary distributions don't need
# them.
#
# Revision 1.13  2011/07/23 02:30:26  phil
# Viper Copyright
#
# Revision 1.12  2011/04/28 22:52:21  bruno
# Put the rocks-dist lock file back in place.
#
# This is important to have as one could build a new frontend and then
# immediately run 'insert-ethers', discover some nodes, then the repo will be
# swapped out from under them which will cause those installations to fail.
#
# Revision 1.11  2010/10/01 14:21:44  bruno
# we no longer build torrent files
#
# Revision 1.10  2010/09/07 23:52:51  bruno
# star power for gb
#
# Revision 1.9  2009/07/16 23:07:46  bruno
# cross-kickstarting fixes
#
# Revision 1.8  2009/06/15 23:47:47  bruno
# atomically create distros
#
# Revision 1.7  2009/05/01 19:06:56  mjk
# chimi con queso
#
# Revision 1.6  2009/03/21 22:22:55  bruno
#  - lights-out install of VM frontends with new node_rolls table
#  - nuked 'site' columns and tables from database
#  - worked through some bugs regarding entities
#
# Revision 1.5  2008/12/18 21:41:17  bruno
# add the 'enabled' field to the rolls selection code while building a distro.
#
# Revision 1.4  2008/10/18 00:55:48  mjk
# copyright 5.1
#
# Revision 1.3  2008/05/30 22:15:16  bruno
# can now install a frontend off CD with the distro moved to
# /export/rocks/install
#
# Revision 1.2  2008/05/22 21:02:06  bruno
# rocks-dist is dead!
#
# moved default location of distro from /export/home/install to
# /export/rocks/install
#
# Revision 1.1  2008/05/10 01:49:28  bruno
# first draft of rocks-dist replacement
#
#

import os
import os.path
import tempfile
import shutil
import rocks
import rocks.commands
import rocks.dist
import rocks.build

class Command(rocks.commands.create.command):
	"""
	Create a Rocks distribution. This distribution is used to install
	Rocks nodes.

	<param type='string' name='arch'>
	The architecture of the distribution. The default is the native
	architecture of the machine.
	</param>

	<param type='string' name='version'>
	The version of the distribution. The default is the native
	version of the machine.
	</param>

	<param type='string' name='rolls'>
	A list of rolls that should be included in the distribution. This
	must be a list separated by spaces of the form: rollname,version.
	For example: rolls="CentOS,5.0 kernel,5.0". The default is to
	include all the enabled rolls for the native architecture. To
	get a list of enabled rolls, execute: "rocks list roll".
	</param>

	<param type='string' name='root'>
	The path prefix location of the rolls. The default is:
	/export/rocks/install.
	</param>

	<param type='string' name='dist'>
	The directory name of the distribution. The default is: "rocks-dist".
	</param>

	<param type='bool' name='md5'>
	Calculate MD5SUM of all packages. Default is 'yes'.
	</param>
	<example cmd='create distro'>

	Create a distribution in the current directory.
	</example>
	"""

	def getRolls(self, arch):
		rolls = []

		self.db.execute("""select name,version,arch,enabled from
			rolls where OS="linux" """)

		for name,version,arch,enabled in self.db.fetchall():
			if enabled == 'yes' and arch == arch:
				rolls.append([name, version, enabled])

		return rolls


	def commandDist(self, dist, rolls):    	
		builder = rocks.build.DistributionBuilder(dist)

		builder.setRolls(rolls)
		builder.setSiteProfiles(1)
		builder.setCalcMD5(self.md5)
		builder.build()

		return builder


	def run(self, params, args):
		#
		# args = arch
		#
		lockfile = '/var/lock/rocks-dist'
		if os.path.exists(lockfile):
			
			self.abort("Lockfile exists already. Is another rocks create " +\
				"distro running?\nRemove %s if you are sure it doesn't." 
				% lockfile)
		os.system('touch %s' % lockfile)

		(arch, version, withrolls, root, calcmd5, dist) = self.fillParams(
			[ ('arch', self.arch),
			('version', rocks.version),
			('rolls', None),
			('root', '/export/rocks/install'),
			('md5', 'yes'),
			('dist', 'rocks-dist') ])

		rolls = []
		if withrolls == None:
			if self.db:
				rolls = self.getRolls(arch)
		else:
			for i in withrolls.split(' '):
				rolls.append(i.split(',') + [ 'yes' ] )

		self.md5 = self.str2bool(calcmd5)

		mirror = rocks.dist.Mirror()
		mirror.setHost('rolls')
		mirror.setPath(root)
		mirror.setRoot(root)
		mirror.setArch(arch)

		mirrors = []
		mirrors.append(mirror)

		distro = rocks.dist.Distribution(mirrors, version)
		distro.setRoot(os.getcwd())

		#
		# set the proper umask so we don't end up with a 
		# distro which is unaccessible from apache
		#
		old_umask = os.umask(0o022)
		try:
			#
			# build the new distro in a temporary directory
			#
			tempdist = tempfile.mkdtemp(dir="")
			distro.setDist(tempdist)

			distro.setLocal('/usr/src/redhat')
			distro.setContrib(os.path.join(mirror.getRootPath(), 'contrib',
				version))

			builder = self.commandDist(distro, rolls)

			#
			# make sure everyone can traverse the the rolls directories
			#
			mirrors = distro.getMirrors()
			fullmirror = mirrors[0].getRollsPath()
			os.system('find %s -type d ' % (fullmirror) + \
				'-exec chmod -R 0755 {} \;')

			#
			# if we are cross-kickstarting, and if there already is
			# a distro directory, then just move the architecture
			# directory into the existing distro
			#
			if self.arch != arch and os.path.exists(dist):
				shutil.move(os.path.join(tempdist, arch),
					os.path.join(dist, arch))
				shutil.rmtree(tempdist)
			else:
				#
				# now move the previous distro into a temporary
				# directory
				#
				prevdist = tempfile.mkdtemp(dir="")
				try:
					shutil.move(dist, prevdist)
				except:
					pass

				#
				# rename the temporary distro (the one we just built)
				# to the 'official' name and make sure the permissions
				# are correct
				#
				shutil.move(tempdist, dist)
				os.system('chmod 755 %s' % dist)

				#
				# nuke the previous distro
				#
				try:
					shutil.rmtree(prevdist)
				except:
					pass

			os.unlink(lockfile)

		finally:
			os.umask(old_umask)



RollName = "base"
