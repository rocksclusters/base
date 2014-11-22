# $Id: __init__.py,v 1.6 2013/02/19 18:48:43 clem Exp $
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
# Revision 1.6  2013/02/19 18:48:43  clem
# when changing the name of a host check that the new name is not already used
#
# Revision 1.5  2012/11/27 00:48:28  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.4  2012/05/06 05:48:35  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2012/04/05 20:57:41  phil
# Fix bug where catindex was not updated when the host name was changed
#
# Revision 1.2  2011/07/23 02:30:38  phil
# Viper Copyright
#
# Revision 1.1  2010/10/04 18:30:38  bruno
# add the ability to change the name in the nodes table
#
#

import rocks.commands

class Command(rocks.commands.set.host.command):
	"""
	Rename a host.
	
	<arg type='string' name='host' repeat='0'>
	The current name of the host.
	</arg>

	<arg type='string' name='name'>
	The new name for the host.
	</arg>

	<param optional='1' type='string' name='name'>
	Can be used in place of the 'name' argument.
	</param>

	<example cmd='set host name compute-0-0 new-compute-0-0'>
	Changes the name of compute-0-0 to new-compute-0-0.
	</example>

	<example cmd='set host cpus compute-0-0 name=new-compute-0-1'>
	Same as above.
	</example>
	"""

	def run(self, params, args):
		(args, name) = self.fillPositionalArgs(('name',))
		
		if not len(args):
			self.abort('must supply a host')
		if not name:
			self.abort('must supply new name')

		self.newdb.checkHostnameValidity(name)
		
		hosts = self.getHostnames(args)
		if len(hosts) > 1:
			self.abort('must supply only one host')
		host = hosts[0]

		self.db.execute("""UPDATE catindex SET name='%s'  
			WHERE name='%s' AND 
			category=(SELECT id FROM categories WHERE name='host')
			""" % (name,host))

		self.db.execute("""UPDATE nodes SET name='%s' 
			WHERE name='%s'""" % (name, host))
		

RollName = "base"
