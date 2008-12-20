# $Id: __init__.py,v 1.1 2008/12/20 01:06:15 mjk Exp $
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
# Revision 1.1  2008/12/20 01:06:15  mjk
# - added appliance_attributes
# - attributes => node_attributes
# - rocks set,list,remove appliance attr
# - eval shell for conds has a special local dictionary that allows
#   unresolved variables (attributes) to evaluate to None
# - need to add this to solaris
# - need to move UserDict stuff into pylib and remove cut/paste code
# - need a drink
#

import sys
import socket
import rocks.commands
import string

class Command(rocks.commands.list.host.command):
	"""
	Lists the set of attributes for hosts.

	<arg optional='1' type='string' name='host'>
	Host name of machine
	</arg>
	
	<example cmd='list host attr compute-0-0'>
	List the attributes for compute-0-0.
	</example>
	"""

	def run(self, params, args):

		self.beginOutput()
		
		for host in self.getHostnames(args):
			attrs = {}
			self.db.execute("""
				select aa.attr, aa.value from
				appliance_attributes aa, nodes n, 
				memberships m, appliances a where
				n.membership=m.id and 
				m.appliance=a.id and 
				aa.appliance=a.id and 
				n.name='%s'
				""" % host)
			for (key, value) in self.db.fetchall():
				attrs[key] = (value, 'appliance')
		
			self.db.execute("""
				select a.attr, a.value from 
				node_attributes a, nodes n where
				a.node=n.id and n.name='%s'
				""" % host)
			for (key, value) in self.db.fetchall():
				attrs[key] = (value, 'node')
				
			for (key, value) in attrs.items():
				self.addOutput(host, (key, value[0], value[1]))

		self.endOutput(header=['host', 'attr', 'value', 'source' ],
			trimOwner=0)

