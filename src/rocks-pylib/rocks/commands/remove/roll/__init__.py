# $Id: __init__.py,v 1.11 2012/11/27 00:48:22 phil Exp $
#
# This file was authored by Brandon Davidson from the University of Oregon.
# The Rocks Developers thank Brandon for his contribution.
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
# $Log: __init__.py,v $
# Revision 1.11  2012/11/27 00:48:22  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.10  2012/05/06 05:48:30  phil
# Copyright Storm for Mamba
#
# Revision 1.9  2011/07/23 02:30:34  phil
# Viper Copyright
#
# Revision 1.8  2010/09/07 23:52:58  bruno
# star power for gb
#
# Revision 1.7  2009/05/01 19:07:01  mjk
# chimi con queso
#
# Revision 1.6  2009/04/23 17:17:21  bruno
# remove the entry in the node_rolls table when a roll is removed
#
# Revision 1.5  2009/04/23 17:12:29  bruno
# cleanup 'rocks remove host' command
#
# Revision 1.4  2008/10/18 00:55:56  mjk
# copyright 5.1
#
# Revision 1.3  2008/09/25 19:27:46  bruno
# anoop's fix.
#
# Revision 1.2  2008/07/01 22:01:01  anoop
# self.os returns "sunos" and not "solaris". So
# function name needs to be clean_roll_sunos and not
# clean_roll_solaris
#
# Revision 1.1  2008/07/01 21:23:57  bruno
# added the command 'rocks remove roll' and tweaked the other roll commands
# to handle 'arch' flag.
#
# thank to Brandon Davidson from the University of Oregon for these changes.
#
#

import os
import stat
import time
import sys
import string
import rocks.commands


class Command(rocks.commands.RollArgumentProcessor,
	rocks.commands.remove.command):
	"""
	Remove a roll from both the database and filesystem.	

	<arg type='string' name='roll' repeat='1'>
	List of rolls. This should be the roll base name (e.g., base, hpc,
	kernel).
	</arg>
	
	<param type='string' name='version'>
	The version number of the roll to be removed. If no version number is
	supplied, then all versions of a roll will be removed.
	</param>
	
	<param type='string' name='arch'>
	The architecture of the roll to be removed. If no architecture is
	supplied, then all architectures will be removed.
	</param>

	<example cmd='remove roll kernel'>
	Remove all versions and architectures of the kernel roll
	</example>
	
	<example cmd='remove roll ganglia version=5.0 arch=i386'>
	Remove version 5.0 of the Ganglia roll for i386 nodes
	</example>
	
	<related>add roll</related>
	<related>enable roll</related>
	<related>disable roll</related>
	<related>list roll</related>
	<related>create roll</related>
	"""		

	def run(self, params, args):
		self.beginOutput()

                (arch, ) = self.fillParams([('arch', '%')])

                if len(args) < 1:
                        self.abort('must supply one or more rolls')

		for (roll, version) in self.getRollNames(args, params):
			rows = self.db.execute("""select arch from rolls
				where name like '%s' and 
				version like '%s' and
				arch like '%s'""" % (roll, version, arch))

			if rows == 0: # empty table is OK
				continue

			# Remove each arch's instance of this roll version
			for (thisarch,) in self.db.fetchall():
				self.clean_roll(roll, version, thisarch)

		self.endOutput(padChar='')

	def clean_roll(self, roll, version, arch):
		""" Remove roll files and database entry for this arch. Calls 
		the Host OS specific function for proper filesystem cleanup. """

		self.addOutput('', 'Removing "%s" (%s,%s) roll...' %
			(roll, version, arch))

		# Like add, call through to OS-specific function due to 
		# path differences. Proper DB use should fix this.
		clean_rolldir = getattr(self, 'clean_rolldir_%s' % self.os)
		clean_rolldir(roll, version, arch)

		#
		# remove the roll from 'node_rolls'
		#
		self.db.execute("""delete from node_rolls where
			rollid = (select id from rolls where name = '%s' and
			version = '%s' and arch = '%s') """ %
			(roll, version, arch))

		# Remove roll from database as well
		self.db.execute("""delete from rolls
			where name = '%s' and
			version = '%s' and
			arch = '%s'""" % (roll, version, arch))

	def clean_rolldir_linux(self, roll, version, arch):
		""" Clean out the roll's filesystem presence on Linux. """
		rolls_dir = '/export/rocks/install/rolls'
		self.clean_dir(os.path.join(rolls_dir, roll, version, arch))

	def clean_rolldir_sunos(self, roll, version, arch):
		""" Clean out the roll's filesystem presence on Solaris. """
		rolls_dir = '/export/rocks/install/jumpstart/rolls'
		self.clean_dir(os.path.join(rolls_dir, roll, version, arch))

	def clean_dir(self, dir):
		# This function cleans up a given directory and
		# removes it from the face of the harddisk
		if os.path.exists(dir):
			for root, dirs, files in os.walk(dir, topdown=False):
				for name in files:
					os.remove(os.path.join(root, name))
				for name in dirs:
					if os.path.islink(os.path.join(root,
						name)):
						os.remove(os.path.join(root,
							name))
					else:
						os.rmdir(os.path.join(root,
							name))

			os.removedirs(dir)

