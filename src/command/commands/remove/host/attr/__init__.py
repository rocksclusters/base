# $Id: __init__.py,v 1.8 2012/11/27 00:48:21 phil Exp $
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
# Revision 1.8  2012/11/27 00:48:21  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.7  2012/05/06 05:48:29  phil
# Copyright Storm for Mamba
#
# Revision 1.6  2011/07/23 02:30:33  phil
# Viper Copyright
#
# Revision 1.5  2010/09/07 23:52:58  bruno
# star power for gb
#
# Revision 1.4  2009/11/18 23:34:49  bruno
# cleanup help section
#
# Revision 1.3  2009/05/01 19:07:00  mjk
# chimi con queso
#
# Revision 1.2  2008/12/20 01:06:15  mjk
# - added appliance_attributes
# - attributes => node_attributes
# - rocks set,list,remove appliance attr
# - eval shell for conds has a special local dictionary that allows
#   unresolved variables (attributes) to evaluate to None
# - need to add this to solaris
# - need to move UserDict stuff into pylib and remove cut/paste code
# - need a drink
#
# Revision 1.1  2008/12/18 20:01:33  mjk
# attribute commands
#

import rocks.commands
import rocks.commands.set.attr

class Command(rocks.commands.remove.host.command):
	"""
	Remove an attribute for a host.

	<arg type='string' name='host'>
	One or more hosts
	</arg>
	
	<arg type='string' name='attr'>
	The attribute name that should be removed.
 	</arg>
 	
	<param type='string' name='attr'>
	Can be used in place of the attr argument.
	</param>

	<example cmd='remove host attr compute-0-0 cpus'>
	Removes the attribute cpus for host compute-0-0.
	</example>

	<example cmd='remove host attr compute-0-0 attr=cpus'>
	Same as above.
	</example>
	"""

	def run(self, params, args):
		(args, attr) = self.fillPositionalArgs(('attr', ))

		if not attr:
			self.abort('missing attribute name')

		for host in self.getHostnames(args):
			self.db.execute("""
			delete from node_attributes where 
			node = (select id from nodes where name='%s')
			and attr = '%s'
			""" % (host, attr))

			self.db.execute("""
			delete from node_attributes where
			node = (select id from nodes where name='%s')
			and attr = '%s'
			""" % (host, attr + rocks.commands.set.attr.postfix))

