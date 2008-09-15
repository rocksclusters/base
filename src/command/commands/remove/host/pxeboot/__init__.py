# $Id: __init__.py,v 1.8 2008/09/15 19:52:57 bruno Exp $
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
# Revision 1.8  2008/09/15 19:52:57  bruno
# fix for removing a node that has vlans defined
#
# Revision 1.7  2008/03/06 23:41:39  mjk
# copyright storm on
#
# Revision 1.6  2007/07/04 01:47:39  mjk
# embrace the anger
#
# Revision 1.5  2007/06/28 21:48:38  bruno
# made a sweep over all the remove commands
#
# Revision 1.4  2007/06/27 16:58:54  bruno
# needs an 's'
#
# Revision 1.3  2007/06/27 04:57:14  bruno
# check for file existence before unlinking it
#
# Revision 1.2  2007/06/25 23:45:06  bruno
# associate with base roll
#
# Revision 1.1  2007/06/25 23:24:36  bruno
# added a command to remove the PXE boot configuration for a node that
# is removed with insert-ethers
#
# Revision 1.3  2007/06/19 16:42:43  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.2  2007/06/18 20:58:02  phil
# Fix doc in gateway. Added set module command
#
# Revision 1.1  2007/06/18 20:44:58  phil
# Allow setting of gateway
#

import os
import os.path
import string
import rocks.commands

class Command(rocks.commands.remove.host.command):
	"""
	Removes the PXE boot configuration for a host

	<arg type='string' name='host' repeat='1'>
	One or more named hosts.
	</arg>
	
	<example cmd='remove host pxeboot compute-0-0'>
	Removes the PXE boot configuration for host compute-0-0.
	</example>

	<example cmd='remove host pxeboot compute-0-0 compute-0-1'>
	Removes the PXE boot configuration for hosts compute-0-0 and
	compute-0-1.
	</example>
	"""
	
	def run(self, params, args):
		if not len(args):
			self.abort("must supply host")

		for host in self.getHostnames(args):

			self.db.execute("""delete from pxeboot where
				pxeboot.node=
				(select id from nodes where name='%s')""" % 
				host)
				
			#
			# remove the pxe configuration file
			#
			rows = self.db.execute("""select networks.ip from
				networks, nodes, subnets where
				networks.node=nodes.id and
				subnets.name='private' and
				networks.subnet=subnets.id and
				nodes.name='%s'""" % host)

			for ipaddr, in self.db.fetchall():
				if not ipaddr:
					return

				filename = '/tftpboot/pxelinux/pxelinux.cfg/'
				for i in string.split(ipaddr, '.'):
					hexstr = '%02x' % (int(i))
					filename += '%s' % hexstr.upper()

				if os.path.exists(filename):
					os.unlink(filename)

