# $Id: __init__.py,v 1.18 2012/11/27 00:48:12 phil Exp $
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
# Revision 1.18  2012/11/27 00:48:12  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.17  2012/05/06 05:48:22  phil
# Copyright Storm for Mamba
#
# Revision 1.16  2011/07/23 02:30:27  phil
# Viper Copyright
#
# Revision 1.15  2010/09/07 23:52:52  bruno
# star power for gb
#
# Revision 1.14  2009/05/01 19:06:56  mjk
# chimi con queso
#
# Revision 1.13  2008/10/18 00:55:49  mjk
# copyright 5.1
#
# Revision 1.12  2008/07/01 21:23:57  bruno
# added the command 'rocks remove roll' and tweaked the other roll commands
# to handle 'arch' flag.
#
# thank to Brandon Davidson from the University of Oregon for these changes.
#
# Revision 1.11  2008/03/06 23:41:36  mjk
# copyright storm on
#
# Revision 1.10  2007/07/04 01:47:37  mjk
# embrace the anger
#
# Revision 1.9  2007/07/02 17:51:31  bruno
# cleanup enable and disable commands
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
# Revision 1.6  2007/06/16 02:39:50  mjk
# - added list roll commands (used for docbook)
# - docstrings should now be XML
# - added parser for docstring to ASCII or DocBook
# - ditched Phil's Network regex stuff (will come back later)
# - updated several docstrings
#
# Revision 1.5  2007/06/07 21:23:04  mjk
# - command derive from verb.command class
# - default is MustBeRoot
# - list.command / dump.command set MustBeRoot = 0
# - removed plugin non-bugfix
#
# Revision 1.4  2007/06/07 17:21:50  mjk
# - added RollArgumentProcessor
# - added trimOwner option to the endOutput method
# - roll based commands are uniform
#
# Revision 1.3  2007/06/05 19:08:43  bruno
# handle ops on all rolls
#
# Revision 1.2  2007/06/04 20:40:31  bruno
# tweaks to rocks enable/disable roll
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
	rocks.commands.disable.command):
	"""
	Disable an available roll. The roll must already be copied on the
	system using the command "rocks add roll".
	
	<arg type='string' name='roll' repeat='1'>
	List of rolls to disable. This should be the roll base name (e.g.,
	base, hpc, kernel).
	</arg>
	
	<param type='string' name='version'>
	The version number of the roll to be disabled. If no version number is
	supplied, then all versions of a roll will be disabled.
	</param>
	
	<param type='string' name='arch'>
	The architecture to disable this roll for. If no architecture is
	supplied, then the roll will be disabled for all architectures.
	</param>	

	<example cmd='disable roll kernel'>
	Disable the kernel roll
	</example>
	
	<example cmd='disable roll ganglia version=5.0 arch=i386'>
	Disable version 5.0 the Ganglia roll for i386 nodes
	</example>
	
	<related>add roll</related>
	<related>remove roll</related>
	<related>enable roll</related>
	<related>list roll</related>
	<related>create roll</related>
	"""		

	def run(self, params, args):
                (arch, ) = self.fillParams([('arch', '%')])

                if len(args) < 1:
                        self.abort('must supply one or more rolls')

		for (roll, version) in self.getRollNames(args, params):
			self.db.execute("""update rolls set enabled='no' where
				name='%s' and version='%s' and arch like '%s'"""
				% (roll, version, arch))

