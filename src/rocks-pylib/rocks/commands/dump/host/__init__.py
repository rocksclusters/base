# $Id: __init__.py,v 1.17 2012/11/27 00:48:14 phil Exp $
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
# Revision 1.17  2012/11/27 00:48:14  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.16  2012/05/06 05:48:23  phil
# Copyright Storm for Mamba
#
# Revision 1.15  2011/07/23 02:30:28  phil
# Viper Copyright
#
# Revision 1.14  2011/05/26 23:20:54  phil
# Add unambiguous add host command
#
# Revision 1.13  2011/03/04 02:00:26  anoop
# fix rocks host dump command to capture os information
#
# Revision 1.12  2010/09/07 23:52:52  bruno
# star power for gb
#
# Revision 1.11  2009/10/28 21:00:56  bruno
# capture the runaction and installaction from a 'rocks dump'
#
# Revision 1.10  2009/06/19 21:07:30  mjk
# - added dumpHostname to dump commands (use localhost for frontend)
# - added add commands for attrs
# - dump uses add for attr (does not overwrite installer set attrs)A
# - do not dump public or private interfaces for the frontend
# - do not dump os/arch host attributes
# - fix various self.about() -> self.abort()
#
# Revision 1.9  2009/06/16 21:45:38  bruno
# no need to use double quotes
#
# Revision 1.8  2009/05/01 19:06:57  mjk
# chimi con queso
#
# Revision 1.7  2008/10/18 00:55:49  mjk
# copyright 5.1
#
# Revision 1.6  2008/03/06 23:41:36  mjk
# copyright storm on
#
# Revision 1.5  2007/07/04 01:47:37  mjk
# embrace the anger
#
# Revision 1.4  2007/06/23 03:54:52  mjk
# - first pass at consistency
# - still needs some docstrings
# - argument processors take SQL wildcards
# - add cannot run twice (must use set)
# - dump does sets not just adds
#
# Revision 1.3  2007/06/19 16:42:41  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.2  2007/06/07 21:23:04  mjk
# - command derive from verb.command class
# - default is MustBeRoot
# - list.command / dump.command set MustBeRoot = 0
# - removed plugin non-bugfix
#
# Revision 1.1  2007/06/07 16:19:10  mjk
# - add "rocks add host"
# - add "rocks dump host"
# - add "rocks dump host interface"
# - remove "rocks add host new"
# - add mysql db init script to foundation-mysql
# - more flexible hostname lookup for the command line
#

import os
import sys
import string
import rocks.commands

class command(rocks.commands.HostArgumentProcessor,
	rocks.commands.dump.command):

	def dumpHostname(self, hostname):
		if hostname == self.db.getHostname():
			return 'localhost'
		else:
			return hostname

	
class Command(command):
	"""
	Dump the host information as rocks commands.

	<arg optional='1' type='string' name='host' repeat='1'>
	Zero, one or more host names. If no host names are supplied, 
	information for all hosts will be listed.
	</arg>

	<example cmd='dump host compute-0-0'>
	Dump host compute-0-0 information.
	</example>
	
	<example cmd='dump host compute-0-0 compute-0-1'>
	Dump host compute-0-0 and compute-0-1 information.
	</example>
		
	<example cmd='dump host'>
	Dump all hosts.
	</example>
	"""

	def run(self, params, args):
		for host in self.getHostnames(args):
			self.db.execute("""select 
				n.cpus, n.rack, n.rank, m.name, 
				n.runaction, n.installaction, n.os
				from nodes n, memberships m where
				n.membership=m.id and n.name='%s'""" % host)
			(cpus, rack, rank, membership, runaction,
				installaction, os) = self.db.fetchone()

			# do not dump the localhost since the installer
			# will add the host for us

			if self.db.getHostname() == host:
				continue

			self.dump('"add host" %s cpus=%s rack=%s rank=%s '
				'membership=%s os=%s' %
				(host, cpus, rack, rank, 
				self.quote(membership), os))

			#
			# now set the runaction and installaction for each host
			#
			if runaction:
				self.dump('set host runaction %s action=%s'
					% (host, self.quote(runaction)))
			if installaction:
				self.dump('set host installaction %s action=%s'
					% (host, self.quote(installaction)))



RollName = "base"
