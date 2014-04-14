# $Id: __init__.py,v 1.16 2012/11/27 00:48:28 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 6.1.1 (Sand Boa)
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
# Revision 1.16  2012/11/27 00:48:28  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.15  2012/08/23 16:42:06  clem
# set host interface vlan and set host interface subnet did not accept properly
# MAC addresses for their iface input argument
#
# Revision 1.14  2012/05/06 05:48:35  phil
# Copyright Storm for Mamba
#
# Revision 1.13  2011/07/23 02:30:38  phil
# Viper Copyright
#
# Revision 1.12  2011/02/01 20:46:24  mjk
# Fixed naming to default to HOSTNAME, instead of HOSTNAME-SUBNET.  This
# was missed in the transition to the new networks based naming.
#
# Revision 1.11  2010/09/07 23:53:01  bruno
# star power for gb
#
# Revision 1.10  2010/04/20 16:38:27  bruno
# comment fix
#
# Revision 1.9  2010/01/20 21:49:13  mjk
# - generate a default name for the interface (enhancement)
#   - hostname if private
#   - hostname-subnet otherwise
#
# Revision 1.8  2009/05/01 19:07:03  mjk
# chimi con queso
#
# Revision 1.7  2009/04/14 16:12:17  bruno
# push towards chimmy beta
#
# Revision 1.6  2008/10/18 00:55:57  mjk
# copyright 5.1
#
# Revision 1.5  2008/03/06 23:41:40  mjk
# copyright storm on
#
# Revision 1.4  2007/07/04 01:47:40  mjk
# embrace the anger
#
# Revision 1.3  2007/06/19 16:42:43  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.2  2007/06/18 22:34:41  phil
# Rewrote add host interface to use set commands
# Fixed error in subnet
# Xrefs in ip
#
# Revision 1.1  2007/06/18 20:45:13  phil
# Fix documentation
#
#

import rocks.commands

class Command(rocks.commands.set.host.command):
	"""
	Sets the subnet for named interface on one of more hosts. 

	<arg type='string' name='host' repeat='1'>
	One or more named hosts.
	</arg>
	
	<arg type='string' name='iface'>
 	Interface that should be updated. This may be a logical interface or 
 	the MAC address of the interface.
 	</arg>
 	
 	<arg type='string' name='subnet'>
	The subnet address of the interface. This is a named subnet and must be
	listable by the command 'rocks list network'.
	</arg>

	<param type='string' name='iface'>
	Can be used in place of the iface argument.
	</param>

	<param type='string' name='subnet'>
	Can be used in place of the subnet argument.
	</param>
	

	<example cmd='set host interface subnet compute-0-0 eth1 public'>
	Sets eth1 to be on the public subnet.
	</example>

	<example cmd='set host interface mac compute-0-0 iface=eth1 subnet=public'>
	Same as above.
	</example>
	
	<!-- cross refs do not exist yet
	<related>set host interface iface</related>
	<related>set host interface ip</related>
	<related>set host interface module</related>
	-->
	<related>add host</related>
	"""
	
	def run(self, params, args):

		(args, iface, subnet) = self.fillPositionalArgs(
			('iface', 'subnet'))

		if not len(args):
			self.abort('must supply host')
		if not iface:
			self.abort('must supply iface')
		if not subnet:
			self.abort('must supply subnet')

		for host in self.getHostnames(args):
			
			# Check to see if this interface has a name yet.  If
			# not label the private interace according to the
			# hostname (in nodes table) and secondary networks
			# are labeled hostname.
			#
			# This protects from the user forgetting to assign
			# a name to each interface, since several commands
			# assuming everything is named.

			self.db.execute("""select net.name from
				networks net, nodes n where
				n.name='%s' and 
				net.node=n.id and 
				(net.device='%s' or net.mac='%s')""" % 
				(host, iface, iface))

			name, = self.db.fetchone()
			if not name:
				name = host

			# Updates the subnet id and the name.  The name
			# is updated even if it did not change (see above)

			self.db.execute("""update networks net, nodes n 
				set net.subnet=
				(select id from subnets s where s.name='%s'),
				net.name='%s'
				where
				n.name='%s' and net.node=n.id and
			 	(net.device='%s' or net.mac='%s')""" %
				(subnet, name, host, iface, iface))


