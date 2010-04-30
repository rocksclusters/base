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

import string
import rocks.commands

class Command(rocks.commands.HostArgumentProcessor,
	rocks.commands.add.command):
	"""
	Add a firewall rule for the specified hosts.

	<arg type='string' name='host'>
	Host name of machine
	</arg>

	<arg type='string' name='service'>
	The service identifier, port number or port range. For example
	"www", 8080 or 0:1024.
	</arg>

	<param type='string' name='protocol'>
	The protocol associated with the service. For example, "tcp" or "udp".
	</param>
	
        <param type='string' name='network'>
        The network this service should be opened on. This is a named network
        (e.g., 'private') and must be listable by the command
        'rocks list network'.
	</param>

        <param type='string' name='output-network' optional='1'>
        The output network this service should be added to. This is a named
	network (e.g., 'private') and must be listable by the command
        'rocks list network'.
	</param>

        <param type='string' name='chain'>
	The iptables 'chain' this service/network should be applied to (e.g.,
	INPUT, OUTPUT, FORWARD).
	</param>

        <param type='string' name='action'>
	The iptables 'action' this service/network should be applied to (e.g.,
	ACCEPT, REJECT, DROP).
	</param>
	"""

	def serviceCheck(self, service):
		#
		# a service can look like:
		#
		#	reserved words: all, nat
		#       named service: ssh
		#       specific port: 8069
		#       port range: 0:1024
		#
		if service in [ 'all', 'nat' ]:
			#
			# valid
			#
			return

		if service[0] in string.digits:
			#
			# if the first character is a number, then assume
			# this is a port or port range:
			#
			ports = service.split(':')
			if len(ports) > 2:
				msg = 'port range "%s" is invalid. ' % service
				msg += 'it must be "integer:integer"'
				self.abort(msg)

			for a in ports:
				try:
					i = int(a)
				except:
					msg = 'port specification "%s" ' % \
						service
					msg += 'is invalid. '
					msg += 'it must be "integer" or '
					msg += '"integer:integer"'
					self.abort(msg)

		#
		# if we made it here, then the service definition looks good
		#
		return


	def run(self, params, args):
		(args, service) = self.fillPositionalArgs(('service'))
		(network, outnetwork, chain, action, protocol, flags,
			comment) = self.fillParams([
				('network', ),
				('output-network', ),
				('chain', ),
				('action', ),
				('protocol', ),
				('flags', ),
				('comment', )
			])
		
		if not service:
			self.abort('service required')
		if not network and not outnetwork:
			self.abort('network or output-network required')
		if not chain:
			self.abort('chain required')
		if not action:
			self.abort('action required')
		if service not in [ 'all', 'nat' ] and not protocol:
			self.abort('protocol required')

		#
		# check if the network exists
		#
		inid = 'NULL'
		if network == 'all':
			inid = 0
		elif network:
			rows = self.db.execute("""select id from subnets where
				name = '%s'""" % (network))

			if rows == 0:
				self.abort('network "%s" not in the database. Run "rocks list network" to get a list of valid networks.')

			inid, = self.db.fetchone()

		outid = 'NULL'
		if outnetwork == 'all':
			outid = 0
		elif outnetwork:
			rows = self.db.execute("""select id from subnets where
				name = '%s'""" % (outnetwork))

			if rows == 0:
				self.abort('output-network "%s" not in the database. Run "rocks list network" to get a list of valid networks.')

			outid, = self.db.fetchone()

		hosts = self.getHostnames(args)
		
		self.serviceCheck(service)

		action = action.upper()
		chain = chain.upper()

		if protocol:
			protocol = '"%s"' % protocol
		else:
			protocol = 'NULL'

		if flags:
			flags = '"%s"' % flags
		else:
			flags = 'NULL'

		if comment:
			comment = '"%s"' % comment
		else:
			comment = 'NULL'

		for host in hosts:
			rows = self.db.execute("""select nf.node from
				node_firewall nf, nodes n where
				n.name = '%s' and n.id = nf.node and
				nf.service = '%s' and nf.action = '%s' and
				nf.chain = '%s' and
				if ('%s' = 'NULL', nf.insubnet is NULL,
					nf.insubnet = %s) and
				if ('%s' = 'NULL', nf.outsubnet is NULL,
					nf.outsubnet = %s) and
				if ('%s' = 'NULL', nf.protocol is NULL,
					nf.protocol = %s) and
				if ('%s' = 'NULL', nf.flags is NULL,
					nf.flags = %s) """ % (host, service,
				action, chain, inid, inid, outid, outid,
				protocol, protocol, flags, flags))

			if rows:
				self.abort('firewall rule already exists')
			
		#
		# all input has been verified. add the rows
		#
		for host in hosts:
			self.db.execute("""insert into node_firewall
				(node, insubnet, outsubnet, service, protocol,
				action, chain, flags, comment) values (
				(select id from nodes where name='%s'), %s, %s,
				'%s', %s, '%s', '%s', %s, %s)""" %
				(host, inid, outid, service, protocol, action,
				chain, flags, comment))

