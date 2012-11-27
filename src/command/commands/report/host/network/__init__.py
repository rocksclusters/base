# $Id: __init__.py,v 1.15 2012/11/27 00:48:25 phil Exp $
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
# Revision 1.15  2012/11/27 00:48:25  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.14  2012/05/06 05:48:32  phil
# Copyright Storm for Mamba
#
# Revision 1.13  2011/09/01 21:55:27  anoop
# Solaris network information made a little more flexible
#
# Revision 1.12  2011/07/23 02:30:35  phil
# Viper Copyright
#
# Revision 1.11  2010/10/06 21:34:09  phil
# Guard against user mistakes. If a name is not associated with the
# private_net network, just don't print the HOSTNAME= line and continue.
#
# Revision 1.10  2010/09/20 20:22:50  bruno
# use the 'primary_net' attribute to dictate which interface should be used
# as the 'primary'. we'll get the domain name from the subnets table and we'll
# set the hostname accordingly.
#
# Revision 1.9  2010/09/07 23:53:00  bruno
# star power for gb
#
# Revision 1.8  2010/05/03 19:34:10  anoop
# Remove ipmi networks from host network information for solaris
#
# Revision 1.7  2009/07/31 01:05:20  anoop
# Bug fix. We should not get the OS of a node from the nodes table. It should
# always key off of the node_attributes table
#
# Revision 1.6  2009/05/01 19:07:02  mjk
# chimi con queso
#
# Revision 1.5  2009/03/13 00:03:00  mjk
# - checkpoint for route commands
# - gateway is dead (now a default route)
# - removed comment rows from schema (let's see what breaks)
# - removed short-name from appliance (let's see what breaks)
# - dbreport static-routes is dead
#
# Revision 1.4  2009/03/04 21:31:44  bruno
# convert all getGlobalVar to getHostAttr
#
# Revision 1.3  2009/03/04 20:15:31  bruno
# moved 'dbreport hosts' and 'dbreport resolv' into the command line
#
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

class Command(rocks.commands.HostArgumentProcessor,
	rocks.commands.report.command):
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

		self.beginOutput()
		
		for host in self.getHostnames(args):
			osname = self.db.getHostAttr(host, 'os')
			f = getattr(self, 'run_%s' % osname)
			f(host)
			
		self.endOutput(padChar='')

	def run_sunos(self, host):

		subnet = self.db.getHostAttr(host, 'primary_net')
		if subnet is None:
			subnet = 'private'

		cmd = 'select nt.name, s.dnszone from ' +\
			'networks nt, subnets s, nodes n where '  +\
			'n.name="%s" and s.name="%s" ' % (host, subnet) +\
			'and nt.node=n.id and nt.subnet=s.id'

		self.db.execute(cmd)

		(hostname, domain) = self.db.fetchone()
		if hostname is None:
			hostname = host
 		# Print the /etc/nodename file
		self.addOutput(host, '<file name="/etc/nodename">')
		self.addOutput(host, hostname)
		self.addOutput(host, '</file>')

		# Print out the /etc/defaultdomain file
		self.addOutput(host, '<file name="/etc/defaultdomain">')
		self.addOutput(host, domain)
		self.addOutput(host, '</file>\n')

		# Get all the subnets that this node is associated with
		# except the ipmi network
		self.db.execute("""select distinctrow 
			subnets.subnet, subnets.netmask from
			subnets, networks, nodes
			where nodes.name='%s' and 
			networks.node=nodes.id and
			networks.device!='ipmi' and
			subnets.id=networks.subnet""" % host)

		self.addOutput(host, '<file name="/etc/netmasks">')
		for row in self.db.fetchall():
			self.addOutput(host, '%s\t%s' % row)
		self.addOutput(host, '</file>')

		defaultrouter = self.db.getHostAttr(host, 'defaultrouter')
		if defaultrouter is None:
			defaultrouter = self.db.getHostAttr(host, 'Kickstart_PrivateGateway')
		self.addOutput(host, '<file name="/etc/defaultrouter">')
		self.addOutput(host, defaultrouter)
		self.addOutput(host, '</file>')

	def run_linux(self, host):
		#
		# get the appliance type
		#
		self.db.execute("""select app.name from
			appliances app, memberships mem, nodes n where
			app.id = mem.appliance and
			n.membership = mem.id and n.name = '%s'""" % (host))
		appliance, = self.db.fetchone()

		self.addOutput(host, '<file name="/etc/sysconfig/network">')
		self.addOutput(host, 'NETWORKING=yes')

		gateway = None
		for (key, val) in self.db.getHostRoutes(host).items():
			if key == '0.0.0.0' and val[0] == '0.0.0.0':
				gateway = val[1]

		interface = self.db.getHostAttr(host, 'primary_net')

		if not interface:
			interface = 'private'

		self.db.execute("""select net.name, s.dnszone from 
			networks net, nodes n, subnets s where
			n.id = net.node and net.subnet = s.id and
			s.name = '%s' and n.name = '%s'""" % (interface, host))
		try:
			(hostname, domain) = self.db.fetchone()
			self.addOutput(host, 'HOSTNAME=%s.%s' % (hostname, domain))
		except:
			pass

		if gateway:
			self.addOutput(host, 'GATEWAY=%s' % gateway)

		self.addOutput(host, '</file>')
