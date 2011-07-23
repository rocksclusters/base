# $Id: __init__.py,v 1.4 2011/07/23 02:30:39 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4.3 (Viper)
# 
# Copyright (c) 2000 - 2011 The Regents of the University of California.
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
# 	Development Team at the San Diego Supercomputer Center at the
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
# Revision 1.4  2011/07/23 02:30:39  phil
# Viper Copyright
#
# Revision 1.3  2010/09/07 23:53:02  bruno
# star power for gb
#
# Revision 1.2  2009/05/01 19:07:03  mjk
# chimi con queso
#
# Revision 1.1  2009/03/24 15:56:09  bruno
# add rolls to the node_rolls table
#
#

import rocks.commands

class Command(rocks.commands.set.host.command):
	"""
	Associates a roll with a frontend appliance.

	<arg type='string' name='host'>
	Host name of a frontend machine.
	</arg>
	
	<arg type='string' name='name'>
	Name of the roll (e.g., 'base').
	</arg>

	<arg type='string' name='version'>
	Version of the roll (e.g., '5.2').
	</arg>

	<arg type='string' name='arch'>
	Architecture of the roll (e.g., 'x86_64').
	</arg>
	
	<param type='string' name='name'>
	Same as 'name' argument.
	</param>

	<param type='string' name='version'>
	Same as 'version' argument.
	</param>

	<param type='string' name='arch'>
	Same as 'arch' argument.
	</param>

	<param type='string' name='os'>
	The OS version. The default is 'linux'.
	</param>

	<example cmd='set host roll frontend-0-0-0 base 5.2 x86_64'>
	Associates the roll with name/version/arch of 'base/5.2/x86_64' to
	frontend-0-0-0.
	</example>

	<related>list host roll</related>
	"""

	def run(self, params, args):
		(args, name, version, arch) = self.fillPositionalArgs(
			('name', 'version', 'arch'))

		os, = self.fillParams( [ ('os', 'linux') ] )

		hosts = self.getHostnames(args)
		
		if not name:
			self.abort('missing roll name')
		if not version:
			self.about('missing roll version')
		if not arch:
			self.about('missing roll architecture')

		fe_hosts = self.getHostnames( [ 'frontend' ] )

		for host in hosts:
			#
			# make sure each host is a frontend appliance
			#
			if host not in fe_hosts:
				msg = 'host "%s" ' % host
				msg += 'is not a frontend appliance'
				self.abort(msg)

		for host in hosts:
			self.setHostRoll(host, name, version, arch, os)

			
	def setHostRoll(self, host, name, version, arch, os):
		#
		# determine if the roll is already assigned to the frontend
		#
		rows = self.db.execute("""
			select * from node_rolls nr, rolls r where
			nr.node=(select id from nodes where name='%s') and
			nr.rollid = r.id and r.name = '%s' and r.version = '%s'
			and r.arch = '%s' and r.os = '%s' """ %
			(host, name, version, arch, os))

		if not rows:
			#
			# get the roll id
			#
			rows = self.db.execute("""select id from rolls where 
				name = '%s' and version = '%s' and
				arch = '%s' and os = '%s' """ % (name, version,
				arch, os))

			if rows == 0:
				msg = 'roll name/version/arch/os '
				msg += '%s/%s/%s/%s' % (name, version, arch, os)
				msg += ' is not in the database'
				self.abort(msg)
			else:
				rollid, = self.db.fetchone()

			self.db.execute("""
				insert into node_rolls values 
				((select id from nodes where name='%s'), %s)"""
				% (host, rollid))

