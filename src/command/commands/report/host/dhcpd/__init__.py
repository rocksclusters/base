#
# $Id: __init__.py,v 1.6 2008/10/18 00:55:56 mjk Exp $
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
# Revision 1.6  2008/10/18 00:55:56  mjk
# copyright 5.1
#
# Revision 1.5  2008/09/11 18:45:15  bruno
# put nodes that have an IP address assigned to their physical interface
# into /etc/dhcpd.conf
#
# Revision 1.4  2008/09/04 20:57:14  bruno
# ignore hosts that don't have IP addresses (like hosted VMs).
#
# Revision 1.3  2008/08/28 18:12:45  anoop
# Now solaris installations use pxelinux to chainload pxegrub. This
# way we can keep generation of pxelinux files controlled through
# "rocks add host pxeaction" and thus keep the content of
# pxelinux files consistent and managed.
#
# Revision 1.2  2008/07/23 00:29:54  anoop
# Modified the database to support per-node OS field. This will help
# determine the kind of provisioning for each node
#
# Modification to insert-ethers, rocks command line, and pylib to
# support the same.
#
# Revision 1.1  2008/05/22 21:02:06  bruno
# rocks-dist is dead!
#
# moved default location of distro from /export/home/install to
# /export/rocks/install
#
#
#

import os
import os.path
import sys
import rocks
import string
import rocks.commands
import rocks.ip

class Command(rocks.commands.report.host.command):
	"""
	Output the DHCP server configuration file for a specific host.

	<arg optional='0' type='string' name='host' repeat='0'>
	Create a DHCP server configuration for the machine named 'host'. If
	no host name is supplied, then generate a DHCP configuration file
	for this host.
	</arg>

	<example cmd='report host dhcpd frontend-0-0'>
	Output the DHCP server configuration file for frontend-0-0.
	</example>
	"""

	def printOptions(self, prefix, opt, defopt={}):
		map = {}
		map['subnet-mask']         = ('PrivateNetmask',    '')
		map['broadcast-address']   = ('PrivateBroadcast',  '')
		map['domain-name']         = ('PrivateDNSDomain',  '"')
		map['nis-domain']	   = ('PrivateNISDomain',  '"')
		map['routers']		   = ('PrivateGateway',    '')
		map['domain-name-servers'] = ('PrivateDNSServers', '')
		for key in map.keys():
			if opt.has_key(map[key][0]):
				value = opt[map[key][0]]
				# Dont print empty values.
				if not value or not string.strip(value): 
					continue
				quote = map[key][1]
				self.addOutput('', '%soption %s %s%s%s;' %
					(prefix, key, quote, value, quote))

		#
		# drop in the filename option
		#
		override = 0
		try:
			cgi = opt['PrivateKickstartCGI']
			override = 1
		except KeyError:
			cgi = defopt['PrivateKickstartCGI']

		if override:
			#
			# if a filename exist, put in PXE configuration
			#
			cgi = os.path.join(os.sep, 'install', cgi)

			self.addOutput('', prefix + 'if ((substring (option' +
				' vendor-class-identifier, 0, 9)')
			self.addOutput('', prefix + '\t\t= "PXEClient") or')
			self.addOutput('', prefix + '\t(substring (option' +
				' vendor-class-identifier, 0, 9)')
			self.addOutput('', prefix + '\t\t= "Etherboot")) {')
			self.addOutput('', prefix + '\t# i386 and x86_64')
			self.addOutput('', prefix + '\tfilename' +
				' "pxelinux.0";')
			self.addOutput('', prefix + '\tnext-server %s;' %
				(opt['PrivateKickstartHost']))

			self.addOutput('', prefix + '} else {')
			self.addOutput('', prefix + '\tfilename "%s";' % (cgi))
			self.addOutput('', prefix + '\tnext-server %s;' % 
				(opt['PrivateKickstartHost']))
			self.addOutput('', prefix + '}\n')


	def printHost(self, name, hostname, mac, ip, opt, defopt, appliance, osname='linux'):
		self.addOutput('', '\t\thost %s {' % name)
		if mac:
			self.addOutput('', '\t\t\thardware ethernet %s;' % mac)

		self.addOutput('', '\t\t\toption host-name "%s";' % hostname)
		self.addOutput('', '\t\t\tfixed-address %s;' % ip)
		self.printOptions('\t\t\t', opt, defopt)
		self.addOutput('', '\t\t}')

		return
		

	def run(self, params, args):
		if len(args) > 1:
			self.abort('cannot supply more than one host name')
		if len(args) == 0:
			args = [ os.uname()[1] ]

		hosts = self.getHostnames(args)

		self.beginOutput()

		dn = self.db.getGlobalVar('Kickstart', 'PrivateDNSDomain')

		self.db.execute("""select component,value from app_globals
			where membership=0 and site=0 and
			service='Kickstart'""")

		defopt = {}
		for key,value in self.db.fetchall():
			defopt[key] = value

		self.addOutput('', 'ddns-update-style none;')
		self.addOutput('', 'subnet %s netmask %s {'
			% (defopt['PrivateNetwork'], defopt['PrivateNetmask']))

		self.addOutput('', '\tdefault-lease-time 1200;')
		self.addOutput('', '\tmax-lease-time 1200;')

		self.printOptions('\t', defopt)

		self.addOutput('', '\tgroup %s {' % dn)
		ip  = rocks.ip.IPGenerator(defopt['PrivateNetwork'],
			defopt['PrivateNetmask'])
		
		self.db.execute("""select nodes.id,nodes.name,nodes.rack,
			nodes.rank,nodes.os,appliances.name,memberships.id from
			nodes,appliances,memberships where
			nodes.membership=memberships.id and 
			memberships.appliance=appliances.id and nodes.site=0
			order by nodes.id""")

		for row in self.db.fetchall():
			node = rocks.util.Struct()
			node.id		= row[0]
			node.name	= row[1]
			node.rack	= row[2]
			node.rank	= row[3]
			node.osname	= row[4]
			node.appname	= row[5]
			node.membership = row[6]

			self.db.execute("""select component,value from
				app_globals where site=0 and membership=%d and
				service='Kickstart'""" % node.membership)
			opt = {}
			for key,value in self.db.fetchall():
				opt[key] = value
			
			#
			# look for a physical private interface that has an
			# IP address assigned to it.
			#
			self.db.execute("""select mac,ip from networks,subnets
				where networks.node = %d and
				subnets.name = "private" and
				networks.subnet = subnets.id and
				networks.ip is not NULL and
				(networks.vlanid is NULL or
				networks.vlanid = 0)""" % (node.id))

			t_info = self.db.fetchone()
			if t_info == None:
				node.ip = None
				node.mac = None
				pass
			else:
				(node.mac, node.ip) = t_info

			if not node.ip:
				#
				# if the machine doesn't have an IP address,
				# there is nothing for our DHCP server to do
				#
				continue

			if not node.name:
				name  = node.modelname
				if node.rack != None:
					name  = name + '-%d' % node.rack
				if node.rank != None:
					name  = name + '-%d' % node.rank
				node.name = name

			# Go fully-qualified.
			node.name = node.name + "." + dn

			self.printHost(node.name, node.name, node.mac,
				node.ip, opt, defopt, node.appname, node.osname)

			#
			# associate all unassigned macs to this node
			#
			self.db.execute("""select mac from networks where
				node = %d and ip is NULL""" % (node.id))
			extramacs = self.db.fetchall()
	
			i = 1
			for row in extramacs:
				extramac = row[0]
				if extramac is None:
					continue
				self.printHost(node.name + '-%d' % (i),
					node.name, extramac,
					node.ip, opt, defopt, node.appname, node.osname)
				i = i + 1

		self.addOutput('', '\t}')
		self.addOutput('', '}')

		self.endOutput(padChar='')

