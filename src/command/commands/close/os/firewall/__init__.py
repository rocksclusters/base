# $Id: __init__.py,v 1.4 2011/02/24 20:10:29 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4 (Maverick)
# 
# Copyright (c) 2000 - 2010 The Regents of the University of California.
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
# Revision 1.4  2011/02/24 20:10:29  bruno
# Added documentation and examples to the add/close/open firewall commands.
# Thanks to Larry Baker for the suggestion.
#
# Revision 1.3  2010/09/07 23:52:51  bruno
# star power for gb
#
# Revision 1.2  2010/05/07 23:13:32  bruno
# clean up the help info for the firewall commands
#
# Revision 1.1  2010/05/06 23:04:57  bruno
# round out the 'close' commands
#
#

import rocks.commands

class Command(rocks.commands.OSArgumentProcessor,
	rocks.commands.close.command):
	"""
	Close a service for an OS type in the cluster.

	<arg type='string' name='os'>
	Name of OS (e.g., "linux", "sunos").
	</arg>

	<param type='string' name='service'>
	The service identifier, port number or port range. For example
	"www", 8080 or 0:1024.
	To have this firewall rule apply to all services, specify the
	keyword 'all'.
	</param>

	<param type='string' name='protocol'>
	The protocol associated with the service. For example, "tcp" or "udp".
	To have this firewall rule apply to all protocols, specify the
	keyword 'all'.
	</param>
	
        <param type='string' name='network'>
        The network this rule should be applied to. This is a named network
        (e.g., 'private') and must be one listed by the command
        'rocks list network'.
	To have this firewall rule apply to all networks, specify the
	keyword 'all'.
	</param>

	<example cmd='close os firewall linux network=public protocol=tcp service=3306'>
	Close the firewall for service 3306 for the TCP protocol on the
	public network for all Linux hosts.
	If 'eth1' is associated with public network on a Linux host, then this
	will be translated as the following iptables rule:
	"-A INPUT -i eth1 -p tcp --dport 3306 -j REJECT"
	</example>

	<example cmd='close os firewall linux network=all protocol=all service=https'>
	Close the firewall for the https service for all protocols and on all
	networks for all Linux hosts.
	If 'eth1' is associated with public network on a Linux host, then this
	will be translated as the following iptables rule:
	"-A INPUT --dport https -j REJECT"
	</example>
	"""

	def run(self, params, args):
		(service, network, protocol) = self.fillParams([
			('service', ),
			('network', ),
			('protocol', )
			])

		if not service:
			self.abort('service required')
		if not network:
			self.abort('network required')
		if service not in [ 'all', 'nat' ] and not protocol:
			self.abort('protocol required')

		if len(args) == 0:
			self.abort('must supply at least one OS type')

		cmd = ()
		if service:
			cmd += ('service=%s' % service, )
		if network:
			cmd += ('network=%s' % network, )
		if protocol:
			cmd += ('protocol=%s' % protocol, )

		#
		# since this is an 'close' command, we assume the action is
		# "REJECT" and the chain is "INPUT"
		#
		cmd += ('action=REJECT', )
		cmd += ('chain=INPUT', )

		for os in self.getOSNames(args):
			self.command('add.os.firewall', (os, ) + cmd)

