# $Id: __init__.py,v 1.1 2010/04/30 22:07:16 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
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
# Revision 1.1  2010/04/30 22:07:16  bruno
# first pass at the firewall commands. we can do global and host level
# rules, that is, we can add, remove, open (calls add), close (also calls add),
# list and dump the global rules and the host-specific rules.
#
#



import rocks.commands

class Command(rocks.commands.remove.command):
	"""
	Remove a global firewall definition. To remove a service,
	one must supply the service, protocol, network, chain and action. See
	"rocks list firewall service" for all the current defined services.

	<arg type='string' name='service'>
	The service identifier, for example "www".
	</arg>

        <param type='string' name='protocol'>
        The protocol associated with the service to be removed (e.g, "tcp"
	or "udp").
	</param>

        <param type='string' name='network'>
        The network associated with the service to be removed. This is a
	named network (e.g., 'private') and must be listable by the command
        'rocks list network'.
	</param>

        <param type='string' name='output-network' optional='1'>
        The output network associated with the service to be removed. This is a
	named network (e.g., 'private') and must be listable by the command
        'rocks list network'.
	</param>

        <param type='string' name='chain'>
	The chain associated with the service and network (e.g., "INPUT").
	</param>

        <param type='string' name='action'>
	The action associated with the service, network and chain
	(e.g., "ACCEPT").
	</param>
	"""

	def run(self, params, args):
		(args, service) = self.fillPositionalArgs(('service'))
		(network, outnetwork, chain, action, protocol) = \
			self.fillParams([
				('network', ),
				('output-network', ),
				('chain', ),
				('action', ),
				('protocol', )
			 ])
		
		if not service:
			self.abort('service required')
		if not network and not outnetwork:
			self.abort('network or output-network required')
		if not chain:
			self.abort('chain required')
		if not action:
			self.abort('action required')
		if not protocol:
			self.abort('protocol required')

		if network:
			rows = self.db.execute("""select id from subnets where
				name = '%s'""" % network)

			if rows == 0:
				self.abort('network "%s" not in database' %
					network)

			inid, = self.db.fetchone()
		else:
			inid = 'NULL'

		if outnetwork:
			rows = self.db.execute("""select id from subnets where
				name = '%s'""" % outnetwork)

			if rows == 0:
				self.abort('output-network "%s" not in database' % network)

			outid, = self.db.fetchone()
		else:
			outid = 'NULL'

		rows = self.db.execute("""delete from global_firewall where
			service = '%s' and if ('%s' = 'NULL', insubnet is NULL,
			insubnet = %s) and if ('%s' = 'NULL', outsubnet is NULL,
			outsubnet = %s) and chain = '%s' and action = '%s' and
			protocol = '%s'""" % (service, inid, inid, outid,
			outid, chain, action, protocol))

		if rows == 0:
			netname = []
			if network:
				netname.append(network)
			if outnetwork:
				netname.append(outnetwork)

			self.abort('no service in database that matches %s/%s/%s/%s/%s' % (service, protocol, '/'.join(netname), chain, action)) 

