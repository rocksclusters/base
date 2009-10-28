#$Id: __init__.py,v 1.10 2009/10/28 07:03:49 mjk Exp $
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
# Revision 1.10  2009/10/28 07:03:49  mjk
# - fixes for ipmi init script change from RHEL 5.3
# - use dmidecode to decide if we should start ipmi service
#
# Revision 1.9  2009/10/07 21:25:47  mjk
# - added openipmi support
# - from green roll (manual steps removed)
# - default passwd is admin, user can change manually
#
# Revision 1.4  2009/09/04 22:13:13  phil
# Really update for 5.2
#
# Revision 1.3  2009/09/04 21:48:37  phil
# Update to Rocks5.2 compatible interface command.
#
# Revision 1.7  2009/06/03 21:28:52  bruno
# add MTU to the subnets table
#
# Revision 1.6  2009/05/01 19:07:02  mjk
# chimi con queso
#
# Revision 1.5  2009/03/30 20:03:05  bruno
# first check if the vm_nodes table exists -- it may be the case that someone
# wants to set up vlans on physical hosts *and* they don't have the xen roll
# installed.
#
# Revision 1.4  2009/03/13 00:02:59  mjk
# - checkpoint for route commands
# - gateway is dead (now a default route)
# - removed comment rows from schema (let's see what breaks)
# - removed short-name from appliance (let's see what breaks)
# - dbreport static-routes is dead
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
#

import rocks.commands

class Command(rocks.commands.HostArgumentProcessor,
	rocks.commands.report.command):
	"""
	Output the network configuration file for a host's interface.

	<arg type='string' name='host'>
	One host name.
	</arg>

	<param type='string' name='iface'>
	Output a configuration file for this host's interface (e.g. 'eth0').
	If no 'iface' parameter is supplied, then configuration files
	for every interface defined for the host will be output (and each
	file will be delineated by &lt;file&gt; and &lt;/file&gt; tags).
	</param>

	<example cmd='report host interface compute-0-0 iface=eth0'>
	Output a network configuration file for compute-0-0's eth0 interface.
	</example>
	"""

	def isPhysicalHost(self, host):
		#
		# determine if this is 'physical' machine, that is, not a VM.
		#
		rows = self.db.execute("""show tables like 'vm_nodes' """)

		if rows == 0:
			#
			# the Xen roll is not installed, so all hosts are
			# physical hosts
			#
			retval = 1
		else:
			rows = self.db.execute("""select vn.id from
				vm_nodes vn, nodes n where
				n.name = '%s' and vn.node = n.id""" % (host))

			if rows == 0:
				#
				# this host is *not* in the VM nodes table, so
				# it is a physical host
				#
				retval = 1
			else:
				retval = 0

		return retval


	def writeIPMI(self, host, ip, channel, netmask):
		self.addOutput(host,
			'<file name="/etc/sysconfig/ipmi-settings">')
		self.addOutput(host, 'ipmitool lan set %s ipaddr %s'
			% (channel, ip))
		self.addOutput(host, 'ipmitool lan set %s netmask %s'
			% (channel, netmask))
		self.addOutput(host, 'ipmitool lan set %s arp respond on'
			% (channel))
		self.addOutput(host, 'ipmitool user set password 1 admin')
		self.addOutput(host, 'ipmitool lan set %s access on'
			% (channel))
		self.addOutput(host, 'ipmitool lan set %s user'
			% (channel))
		self.addOutput(host, 'ipmitool lan set %s auth ADMIN PASSWORD'
			% (channel))
		self.addOutput(host, '</file>')

	def writeConfig(self, host, mac, ip, device, netmask, vlanid, mtu):
		configured = 0

		self.addOutput(host, 'DEVICE=%s' % device)

		if mac:
			self.addOutput(host, 'HWADDR=%s' % mac)

		if ip and netmask:
			self.addOutput(host, 'IPADDR=%s' % ip)
			self.addOutput(host, 'NETMASK=%s' % netmask)
			self.addOutput(host, 'BOOTPROTO=static')
			self.addOutput(host, 'ONBOOT=yes')
			configured = 1

		if vlanid and self.isPhysicalHost(host):
			self.addOutput(host, 'VLAN=yes')
			self.addOutput(host, 'ONBOOT=yes')
			configured = 1

		if not configured:
			self.addOutput(host, 'BOOTPROTO=none')
			self.addOutput(host, 'ONBOOT=no')

		if mtu:
			self.addOutput(host, 'MTU=%s' % mtu)
		

	def writeModprobe(self, host, device, module):
		if not module:
			return

		self.addOutput(host, '<![CDATA[')
		self.addOutput(host, 'grep -v "\<%s\>" /etc/modprobe.conf > /tmp/modprobe.conf' % (device))
		self.addOutput(host, "echo 'alias %s %s' >> /tmp/modprobe.conf" % (device, module))
		self.addOutput(host, 'mv /tmp/modprobe.conf /etc/modprobe.conf')
		self.addOutput(host, 'chmod 444 /etc/modprobe.conf')
		self.addOutput(host, ']]>')


	def run(self, params, args):

		self.iface, = self.fillParams([('iface', ), ])
		self.beginOutput()

                for host in self.getHostnames(args):
			osname = self.db.getHostAttr(host, 'os')               
			f = getattr(self, 'run_%s' % (osname))
			f(host)

		self.endOutput()

	def run_sunos(self, host):
		self.db.execute("select networks.ip, networks.device " +\
				"from networks, nodes where "	+\
				"nodes.name='%s' " % (host)	+\
				"and networks.node=nodes.id")

		for row in self.db.fetchall():
			(ip, device) = row
			if ip is not None:
				self.write_host_file_sunos(ip, device)
		
	def write_host_file_sunos(self, ip, device):
		s = '<file name="/etc/hostname.%s">\n' % device
		s += "%s\n" % ip
		s += '</file>\n'
		self.addText(s)
		
	def run_linux(self, host):
		self.db.execute("""select distinctrow 
			net.mac, net.ip, net.device,
			if(net.subnet, s.netmask, NULL), net.vlanid,
			net.subnet, net.module, s.mtu from
			networks net, nodes n, subnets s where net.node = n.id
			and if(net.subnet, net.subnet = s.id, true) and
			n.name = "%s" order by net.id""" % (host))


		for row in self.db.fetchall():
			mac,ip,device,netmask,vlanid,subnetid,module,mtu = row


			if device == 'ipmi':
				self.writeIPMI(host, ip, module, netmask)

			if device and device[0:4] != 'vlan':
				#
				# output a script to update modprobe.conf
				#
				self.writeModprobe(host, device, module)

			if vlanid and self.isPhysicalHost(host):
				#
				# look up the name of the interface that
				# maps to this VLAN spec
				#
				rows = self.db.execute("""select net.device from
					networks net, nodes n where
					n.id = net.node and n.name = '%s'
					and net.subnet = %d and
					net.device not like 'vlan%%' """ %
					(host, subnetid))

				if rows:
					dev, = self.db.fetchone()
					#
					# check if already referencing 
					# a physical device
					#
					if dev != device:
						device = '%s.%d' % (dev, vlanid)

			if self.iface:
				if self.iface == device:
					self.writeConfig(host, mac, ip, device,
						netmask, vlanid, mtu)
			else:
				s = '<file name="'
				s += '/etc/sysconfig/network-scripts/ifcfg-'
				s += '%s">' % (device)

				self.addOutput(host, s)
				self.writeConfig(host, mac, ip, device,
					netmask, vlanid, mtu)
				self.addOutput(host, '</file>')


