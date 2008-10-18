# $Id: __init__.py,v 1.9 2008/10/18 00:55:55 mjk Exp $
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
# $Log: __init__.py,v $
# Revision 1.9  2008/10/18 00:55:55  mjk
# copyright 5.1
#
# Revision 1.8  2008/07/01 21:23:57  bruno
# added the command 'rocks remove roll' and tweaked the other roll commands
# to handle 'arch' flag.
#
# thank to Brandon Davidson from the University of Oregon for these changes.
#
# Revision 1.7  2008/03/06 23:41:38  mjk
# copyright storm on
#
# Revision 1.6  2007/06/23 03:54:52  mjk
# - first pass at consistency
# - still needs some docstrings
# - argument processors take SQL wildcards
# - add cannot run twice (must use set)
# - dump does sets not just adds
#
# Revision 1.5  2007/06/19 16:42:42  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.4  2007/06/07 21:23:05  mjk
# - command derive from verb.command class
# - default is MustBeRoot
# - list.command / dump.command set MustBeRoot = 0
# - removed plugin non-bugfix
#
# Revision 1.3  2007/06/07 17:21:51  mjk
# - added RollArgumentProcessor
# - added trimOwner option to the endOutput method
# - roll based commands are uniform
#
# Revision 1.2  2007/06/01 17:44:10  bruno
# more than one version of a roll in the rolls database caused redundant
# info to be listed -- the 'distinct' keyword only prints unique values
#
# Revision 1.1  2007/05/31 21:25:55  bruno
# rocks enable/disable/list roll
#
#


import os
import stat
import time
import sys
import string
import rocks.commands


class Command(rocks.commands.RollArgumentProcessor,
	rocks.commands.list.command):
	"""
	List the status of available rolls.
	
	<arg optional='1' type='string' name='roll' repeat='1'>
	List of rolls. This should be the roll base name (e.g., base, hpc,
	kernel). If no rolls are listed, then status for all the rolls are
	listed.
	</arg>

	<example cmd='list roll kernel'>		
	List the status of the kernel roll
	</example>
	
	<example cmd='list roll'>
	List the status of all the available rolls
	</example>

	<related>add roll</related>
	<related>remove roll</related>
	<related>enable roll</related>
	<related>disable roll</related>
	<related>create roll</related>
	"""		

	def run(self, params, args):

		self.beginOutput()
		for (roll, version) in self.getRollNames(args, params):
			self.db.execute("""select version, arch, enabled from
				rolls where name='%s' and version='%s'""" %
				(roll, version))
			for row in self.db.fetchall():
				self.addOutput(roll, row)

		self.endOutput(header=['name', 'version', 'arch', 'enabled'],
			trimOwner=0)
		
