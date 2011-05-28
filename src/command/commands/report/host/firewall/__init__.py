# $Id: __init__.py,v 1.8 2011/05/28 03:25:26 phil Exp $
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
# Revision 1.8  2011/05/28 03:25:26  phil
# Add Firewall, report firewall now working with resolved rules.
# Created a TEMPTABLES database for temporary SQL tables.
# Still needs full testing.
#
# Revision 1.7  2011/03/24 00:14:58  phil
# priviledged ports are actually 0:1023, 1024 is user space.
#
# Revision 1.6  2010/09/07 23:53:00  bruno
# star power for gb
#
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

		for rulename,i, o, s, p, a, c, f, cmt in self.db.fetchall():
			rule = self.buildRule(host, i, o, s, p, a, c, f, cmt)
			if rule:
				rules[rulename] = rule
				if cmt is not None:
					comments[rulename] = cmt


	def getRules(self, host):
		""" Get all rules that are not NAT Rules """
		rules = {}
		comments = {}

		# Use stored procedure to create this host's TEMPTABLES.fwresolved with
		# rules resolved from all levels. Get all rules except NAT

		self.db.execute("""CALL resolvefirewalls('%s','default')""" % host)
		self.db.execute("""SELECT rulename, insubnet, outsubnet, service,
			protocol, action, chain, flags, comment
			FROM TEMPTABLES.fwresolved WHERE NOT (chain = 'POSTROUTING' AND
                        action = 'MASQUERADE' AND service = 'nat' ) ORDER BY rulename""" )

		self.makeRules(host, rules, comments)

		return (rules, comments)


	def getNat(self, host):
		""" Get all rules that are  NAT Rules """
		rules = {}
		comments = {}

		# Use stored procedure to create this host's TEMPTABLES.fwresolved with
		# rules resolved from all levels. Get all NAT rules

		self.db.execute("CALL resolvefirewalls('%s','default')" % host)
		rows = self.db.execute("""SELECT rulename, insubnet, outsubnet, service,
			protocol, action, chain, flags, comment
			FROM TEMPTABLES.fwresolved WHERE chain = 'POSTROUTING' AND
			action = 'MASQUERADE' AND service = 'nat'""")
	
		if rows > 0:
			self.addOutput(host, '*nat')
			self.makeRules(host,rules, comments)	
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

			rules, comments = self.getRules(host)

			keys = rules.keys()
			keys.sort()
			for key in keys:
				commentLine='# %s: ' % key
				if comments.has_key(key) and comments[key]:
					commentLine = commentLine + "%s" % comments[key]
				
				self.addOutput(host, commentLine) 
				self.addOutput(host, rules[key])

			#
			# default reject rules
			#
			rule = self.buildRule(None, None, None, '0:1023',
				'tcp', 'REJECT', 'INPUT', None, None)
			self.addOutput(host, rule)

			rule = self.buildRule(None, None, None, '0:1023',
				'udp', 'REJECT', 'INPUT', None, None)
			self.addOutput(host, rule)

			self.addOutput(host, 'COMMIT')
			self.addOutput(host, '</file>')

		self.endOutput(padChar='')

