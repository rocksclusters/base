# $Id: __init__.py,v 1.2 2008/10/18 00:55:56 mjk Exp $
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
# Revision 1.2  2008/10/18 00:55:56  mjk
# copyright 5.1
#
# Revision 1.1  2008/09/23 01:10:18  bruno
# moved 'rocks.config.host.interface|network' to
# moved 'rocks.report.host.interface|network'
#
# Revision 1.6  2008/08/07 00:57:26  anoop
# Removed unnecessary line
#
# Revision 1.5  2008/08/07 00:55:27  anoop
# Solaris networking and interface information now generated through
# the database, rather than left to default
#
# Revision 1.4  2008/07/23 00:01:06  bruno
# tweaks
#
# Revision 1.3  2008/03/06 23:41:36  mjk
# copyright storm on
#
# Revision 1.2  2008/01/16 22:41:36  bruno
# correctly get the membership of a given host
#
# Revision 1.1  2007/12/10 21:28:34  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
#

import rocks.commands

class Command(rocks.commands.report.host.command):
	"""
	Outputs the network configuration file for a host (on RHEL-based
	machines, this is the contents of the file /etc/sysconfig/network).

	<arg type='string' name='host'>
	One host name.
	</arg>

	<example cmd='report host network compute-0-0'>
	Output the network configuration for compute-0-0.
	</example>
	"""

	def run(self, params, args):
                hosts = self.getHostnames(args)

		#
		# only takes one host
		#
		if len(hosts) != 1:
			return

		host = hosts[0]

		self.db.execute("select os from nodes where " +\
				"name='%s'" % host)
		osname, = self.db.fetchone()

		f = getattr(self, 'run_%s' % osname)

		self.beginOutput()
		f(host)
		self.endOutput()

	def run_sunos(self, host):
 
		# Get the default domain for the host
		domain = self.db.getGlobalVar('Kickstart', 
				'PrivateDNSDomain')

 		# Print the /etc/nodename file
		self.addText('<file name="/etc/nodename">\n')
		self.addText('%s\n' % host)
		self.addText('</file>\n')

		# Print out the /etc/defaultdomain file
		self.addText('<file name="/etc/defaultdomain">\n')
		self.addText('%s\n' % domain)
		self.addText('</file>\n')

		# Get all the subnets that this node is associated with
		self.db.execute("select distinctrow subnets.subnet, "	+\
				" subnets.netmask from subnets, "	+\
				"networks, nodes "	+\
				"where nodes.name='%s' and " % (host) 	+\
				"networks.node=nodes.id and "		+\
				"subnets.id=networks.subnet;")

		self.addText('<file name="/etc/netmasks">\n')
		for row in self.db.fetchall():
			self.addText('%s\t%s\n' % row)
		self.addText('</file>\n')

	def run_linux(self, host):
		#
		# get the appliance type
		#
		rows = self.db.execute("""select app.name from
			appliances app, memberships mem, nodes n where
			app.id = mem.appliance and
			n.membership = mem.id and n.name = '%s'""" % (host))

		if rows != 1:
			return

		appliance, = self.db.fetchone()

		self.beginOutput()
		self.addOutput('', '<file name="/etc/sysconfig/network">')

		self.addOutput('', 'NETWORKING=yes')

		hostname = ''
		gateway = ''

		if appliance == 'frontend':
			rows = self.db.execute("""select net.name, net.gateway
				from networks net, nodes n, subnets s where
				n.id = net.node and net.subnet = s.id and
				s.name = 'public' and n.name = '%s'""" % (host))
		
			if rows == 1:
				hostname, gateway = self.db.fetchone()

		else:
			rows = self.db.execute("""select net.gateway
				from networks net, nodes n, subnets s where
				n.id = net.node and net.subnet = s.id and
				s.name = 'private' and n.name = '%s'""" %
				(host))

			if rows == 1:
				gateway, = self.db.fetchone()

			if not gateway:
				gateway = self.db.getGlobalVar('Kickstart',
					'PrivateGateway')

			domain = self.db.getGlobalVar('Kickstart',
				'PrivateDNSDomain')

			hostname = '%s.%s' % (host, domain)

		self.addOutput('', 'HOSTNAME=%s' % hostname)
		self.addOutput('', 'GATEWAY=%s' % gateway)

		self.addOutput('', '</file>')
