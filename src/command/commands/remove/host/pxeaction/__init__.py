# $Id: __init__.py,v 1.11 2008/03/06 23:41:39 mjk Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		            version 5.0 (V)
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
# Revision 1.11  2008/03/06 23:41:39  mjk
# copyright storm on
#
# Revision 1.10  2008/02/01 20:51:23  bruno
# add the ability to remove all pxeactions for host with a wildcard
#
# Revision 1.9  2008/01/22 17:27:21  bruno
# after removing a pxeaction, need to rebuild the pxe configuration files
#
# Revision 1.8  2007/07/04 01:47:39  mjk
# embrace the anger
#
# Revision 1.7  2007/06/28 21:48:38  bruno
# made a sweep over all the remove commands
#
# Revision 1.6  2007/06/25 23:45:06  bruno
# associate with base roll
#
# Revision 1.5  2007/06/19 16:42:42  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.4  2007/06/05 22:28:11  mjk
# require root for all remove commands
#
# Revision 1.3  2007/05/31 19:35:43  bruno
# first pass at getting all the 'help' consistent on all the rocks commands
#
# Revision 1.2  2007/05/10 20:37:02  mjk
# - massive rocks-command changes
# -- list host is standardized
# -- usage simpler
# -- help is the docstring
# -- host groups and select statements
# - added viz commands
#
# Revision 1.1  2007/05/02 20:20:53  bruno
# added 'pxeaction' table -- allows for adding and removing pxeboot actions
#
#

import sys
import string
import rocks.commands
import os

class Command(rocks.commands.remove.host.command):
	"""
	Remove a pxeaction specification for a list of hosts.

	<arg type='string' name='host' repeat='1'>
	List of hosts to remove pxeaction definitions. If no hosts are listed,
	then the global definition that matches the 'action=name' is removed.
	</arg>

	<param type='string' name='action'>
	The label name for the pxeaction. You can see the pxeaction label
	names by executing: 'rocks list host pxeaction'.
	</param>

	<example cmd='remove host pxeaction compute-0-0 action=os'>
	Remove the 'os' pxeaction for compute-0-0.
	</example>
	"""

	def run(self, params, args):
		(action, ) = self.fillParams([('action', '%')])

		# If no host list is provided remove the default action.
		# Otherwise remove the action for each host.
		
		if not len(args):
			self.db.execute("""delete from pxeaction where
				node=0 and pxeaction.action='%s'""" % action)

			#	
			# regenerate all the pxe boot configuration files
			# including the default
			#
			self.command('set.host.pxeboot', self.getHostnames())
		else:
			for host in self.getHostnames(args):
				self.db.execute("""delete from pxeaction where
					node=
					(select id from nodes where name='%s')
					and pxeaction.action like '%s' """ % 
					(host, action))

				#
				# regenerate the pxe boot configuration
				# file for host
				#
				self.command('set.host.pxeboot', [ host ])

