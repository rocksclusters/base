# $Id: __init__.py,v 1.5 2010/05/27 00:11:32 bruno Exp $
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
# Revision 1.5  2010/05/27 00:11:32  bruno
# firewall fixes
#
# Revision 1.4  2010/05/13 21:50:14  bruno
# almost there
#
# Revision 1.3  2010/05/11 22:28:16  bruno
# more tweaks
#
# Revision 1.2  2010/05/04 22:04:15  bruno
# more firewall commands
#
# Revision 1.1  2010/04/30 22:07:17  bruno
# first pass at the firewall commands. we can do global and host level
# rules, that is, we can add, remove, open (calls add), close (also calls add),
# list and dump the global rules and the host-specific rules.
#
#

import string
import rocks.commands

class Command(rocks.commands.HostArgumentProcessor,
	rocks.commands.report.command):
	"""
	Create a report that outputs the firewall rules for a host.

	<arg optional='0' type='string' name='host'>
	Host name of machine
	</arg>
	
	<example cmd='report host firewall compute-0-0'>
	Create a report of the firewall rules for compute-0-0.
	</example>
	"""

	def getPreamble(self, host):
		self.addOutput(host, '*filter')
		self.addOutput(host, ':INPUT ACCEPT [0:0]')
		self.addOutput(host, ':FORWARD DROP [0:0]')
		self.addOutput(host, ':OUTPUT ACCEPT [0:0]')
		self.addOutput(host, '-A INPUT -i lo -j ACCEPT')


	def translateService(self, service):
		#
		# a service can look like:
		#
		#	all, nat
		#	8069
		#	0:1024
		#
		if service in [ 'all', 'nat' ]:
			return ''

		return service


	def buildRule(self, host, inid, outid, service, protocol, action,
		chain, flags, comment):

		rule = '-A %s' % chain

		#
		# get the interface name that maps to the 'in' network
		#
		if inid:
			rows = self.db.execute("""select net.device from
				networks net, nodes n where
				net.node = n.id and n.name = '%s' and
				net.device not like 'vlan%%' and
				net.subnet = %s""" % (host, '%s' % inid))

			if rows == 1:
				iface, = self.db.fetchone()
				rule += ' -i %s' % iface
			else:
				#
				# the 'network' was specified, but there isn't
				# a network that is configured for this
				# interface, that is, there is no subnet
				# associated with it. in this case, skip this
				# rule
				#
				return None

		#
		# get the interface name that maps to the 'out' network
		#
		if outid:
			rows = self.db.execute("""select net.device from
				networks net, nodes n where
				net.node = n.id and n.name = '%s' and
				net.device not like 'vlan%%' and
				net.subnet = %s""" % (host, '%s' % outid))

			if rows == 1:
				oface, = self.db.fetchone()
				rule += ' -o %s' % oface
			else:
				#
				# the 'output-network' was specified, but
				# there isn't a network that is configured for
				# this interface, that is, there is no subnet
				# associated with it. in this case, skip this
				# rule
				#
				return None

		#
		# if the service is not 'all', then try to find a match
		# in the *_firewall tables
		#
		if service == 'all':
			if protocol and protocol != 'all':
				#
				# this is useful for icmp rules
				#
				rule += ' -p %s' % protocol
		elif service == 'nat':
			pass
		else:
			s = self.translateService(service)
			if s:
				rule += ' -p %s --dport %s' % (protocol, s)

		if flags:
			rule += ' %s' % flags

		rule += ' -j %s' % action

		return rule


	def makeRules(self, host, rules, comments):
		for i, o, s, p, a, c, f, cmt in self.db.fetchall():
			rule = self.buildRule(host, i, o, s, p, a, c, f, cmt)
			if rule:
				key = '%s-%s-%s-%s-%s-%s-%s' % \
					(c, i, o, s, p, a, f)
				rules[key] = rule
				comments[key] = cmt


	def getRules(self, host, action):
		rules = {}
		comments = {}

		# global
		self.db.execute("""select insubnet, outsubnet, service,
			protocol, action, chain, flags, comment from
			global_firewall where action = '%s' order by chain""" %
			(action))

		self.makeRules(host, rules, comments)

		# os
		self.db.execute("""select insubnet, outsubnet, service,
			protocol, action, chain, flags, comment
			from os_firewall where
			os = (select os from nodes where name = '%s') and
			action = '%s' order by chain""" % (host, action))

		self.makeRules(host, rules, comments)

		# appliance
		self.db.execute("""select insubnet, outsubnet, service,
			protocol, action, chain, flags, comment
			from appliance_firewall where
			appliance = (select a.id from appliances a,
			nodes n, memberships m where n.name = '%s' and
			n.membership = m.id and m.appliance = a.id) and
			action = '%s' order by chain""" % (host, action))

		self.makeRules(host, rules, comments)

		# host
		self.db.execute("""select insubnet, outsubnet, service,
			protocol, action, chain, flags, comment
			from node_firewall where
			node = (select id from nodes where name = '%s') and
			action = '%s' order by chain""" % (host, action))

		self.makeRules(host, rules, comments)

		return (rules, comments)


	def getNat(self, host):
		#
		# does this host have NAT?
		#
		nat = 0

		# global
		rows = self.db.execute("""select * from
			global_firewall where chain = 'POSTROUTING' and
			action = 'MASQUERADE' and service = 'nat' """)
	
		if rows > 0:
			nat = 1

		# os
		rows = self.db.execute("""select * from
			os_firewall where chain = 'POSTROUTING' and
			os = (select os from nodes where name = '%s') and
			action = 'MASQUERADE' and service = 'nat' """ % host)
	
		if rows > 0:
			nat = 1

		# appliance
		rows = self.db.execute("""select * from
			appliance_firewall where chain = 'POSTROUTING' and
			appliance = (select a.id from appliances a,
			nodes n, memberships m where n.name = '%s' and
			n.membership = m.id and m.appliance = a.id) and
			action = 'MASQUERADE' and service = 'nat' """ % host)
	
		if rows > 0:
			nat = 1

		# host
		rows = self.db.execute("""select * from
			node_firewall where chain = 'POSTROUTING' and
			node = (select id from nodes where name = '%s') and
			action = 'MASQUERADE' and service = 'nat'""" % host)
	
		if rows > 0:
			nat = 1

		if nat:
			self.addOutput(host, '*nat')
			rules, comments = self.getRules(host, 'MASQUERADE')
			for (key, rule) in rules.items():
				if comments.has_key(key) and comments[key]:
					self.addOutput(host,
						'# %s' % comments[key])
				self.addOutput(host, rule)
			self.addOutput(host, 'COMMIT')
			self.addOutput(host, '')
			
	
	def run(self, params, args):
		self.beginOutput()

		for host in self.getHostnames(args):
			s = '<file name="/etc/sysconfig/iptables" perms="500">'
			self.addOutput(host, s)

			self.getNat(host)

			self.getPreamble(host)

			rules, comments = self.getRules(host, 'ACCEPT')

			keys = rules.keys()
			keys.sort()
			for key in keys:
				if comments.has_key(key) and comments[key]:
					self.addOutput(host,
						'# %s' % comments[key])
				self.addOutput(host, rules[key])

			rules, comments = self.getRules(host, 'REJECT')
			keys = rules.keys()
			keys.sort()
			for key in keys:
				if comments.has_key(key) and comments[key]:
					self.addOutput(host,
						'# %s' % comments[key])
				self.addOutput(host, rules[key])

			#
			# default reject rules
			#
			rule = self.buildRule(None, None, None, '0:1024',
				'tcp', 'REJECT', 'INPUT', None, None)
			self.addOutput(host, rule)

			rule = self.buildRule(None, None, None, '0:1024',
				'udp', 'REJECT', 'INPUT', None, None)
			self.addOutput(host, rule)

			self.addOutput(host, 'COMMIT')
			self.addOutput(host, '</file>')

		self.endOutput(padChar='')

