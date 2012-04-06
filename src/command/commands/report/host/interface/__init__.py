#$Id: __init__.py,v 1.25 2012/04/06 01:53:32 clem Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4.3 (Viper)
# 
# Copyright (c) 2000 - 2011 The Regents of the University of California.
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
# 	Development Team at the San Diego Supercomputer Center at the
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
# Revision 1.25  2012/04/06 01:53:32  clem
# Modified verision of the report interface to support kvm networking
#
# Revision 1.24  2012/03/29 03:44:06  clem
# bootproto can be only none bootp or dhcp
#
# Revision 1.23  2011/07/23 02:30:35  phil
# Viper Copyright
#
# Revision 1.22  2011/02/01 21:14:00  bruno
# tweaks for the new OpenIPMI.
#
# also, can now set the IPMI password.
#
# Revision 1.21  2010/10/06 19:41:10  phil
# Document and interpret linux-only options: dhcp, noreport.
# Needed by EC2.
#
# Revision 1.20  2010/09/30 19:13:26  phil
# Break should be continue. Fixes problem the problem that when ipmi was being configured all
# other interfaces in the select statement were not being config'ed
#
# Revision 1.19  2010/09/20 17:58:40  phil
# Allow VMs to define VLANed interfaces. In other words, load the gun,
# let the user shoot it.
#
# Revision 1.18  2010/09/07 23:53:00  bruno
# star power for gb
#
# Revision 1.17  2010/06/18 17:40:07  anoop
# Solaris Fix: Add netmask information to
# hostname.<interface> file
#
# Revision 1.16  2010/06/10 19:14:54  mjk
# use channel (not module) for ipmi
#
# Revision 1.15  2010/05/03 19:30:25  anoop
# IPMI support for solaris
#
# Revision 1.14  2010/04/20 17:22:36  bruno
# initial support for channel bonding
#
# Revision 1.13  2010/04/19 21:22:15  bruno
# can now set and report 'options' for network interface modules.
#
# this will be handy for setting interrupt coalescing and for setting up
# channel bonding.
#
# Revision 1.12  2010/01/20 00:55:16  mjk
# for ipmi don't create the ifcfg-ipmi files
#
# Revision 1.11  2009/10/28 21:45:56  bruno
# don't pad output
#
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

import re
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


	def isKVMContainer(self, host):
		"""return True if host can run kvm vm host 
		(aka it means that we have different networking) """
		#TODO move this function probably vm.py is a good candidate
		try:
			import rocks.vmconstant
			if rocks.vmconstant.virt_engine != "kvm":
				return False
		except ImportError:
			#xen or kvm roll not installed
			return False
		appliance = self.db.getHostAttr(host, 'appliance' )
		if appliance and appliance == 'vm-container':
			#we could use getHostAttr(host, 'kvm')
			return True
		if appliance and appliance == 'frontend':
			return True
		return False


	def writeIPMI(self, host, ip, channel, netmask):
		defaults = [ ('IPMI_SI', 'yes'),
			('DEV_IPMI', 'yes'),
			('IPMI_WATCHDOG', 'no'),
			('IPMI_WATCHDOG_OPTIONS', '"timeout=60"'),
			('IPMI_POWEROFF', 'no'),
			('IPMI_POWERCYCLE', 'no'),
			('IPMI_IMB', 'no') ]

		self.addOutput(host,
			'<file name="/etc/sysconfig/ipmi" perms="500">')

		for var, default in defaults:
			attr = self.db.getHostAttr(host, var)
			if not attr:
				attr = default
			self.addOutput(host, '%s=%s' % (var, attr))

		self.addOutput(host, 'ipmitool lan set %s ipaddr %s'
			% (channel, ip))
		self.addOutput(host, 'ipmitool lan set %s netmask %s'
			% (channel, netmask))
		self.addOutput(host, 'ipmitool lan set %s arp respond on'
			% (channel))

		attr = self.db.getHostAttr(host, 'ipmi_password')
		if attr:
			password = attr
		else:
			password = 'admin'

		self.addOutput(host, 'ipmitool user set password 1 %s'
			% (password))

		self.addOutput(host, 'ipmitool lan set %s access on'
			% (channel))
		self.addOutput(host, 'ipmitool lan set %s user'
			% (channel))
		self.addOutput(host, 'ipmitool lan set %s auth ADMIN PASSWORD'
			% (channel))

		self.addOutput(host, '</file>')

	def writeBridgedConfig(self, host, mac, ip, device,
                                                netmask, vlanid, mtu, options, channel, active):
		""" called when the interface is on a host that can host KVM VM """
		brName = device
		device = "p" + device
		testOptions="%s" % options
		if re.match('dhcp', testOptions.lower()):
			dhcp = 1 # tell device to dhcp, explicitly
		else:
			dhcp = 0

		#    ------      physical dev in promisc mode
		s = '<file name="/etc/sysconfig/network-scripts/ifcfg-'
		s += '%s">' % (device)
		self.addOutput(host, s)
		#add output
		self.addOutput(host, 'DEVICE=%s' % device)
		if mac:
			self.addOutput(host, 'HWADDR=%s' % mac)
		if vlanid:
			#if this is a vlan we don't create the bridge 
			#and we use the macvtap driver for kvm
			self.addOutput(host, 'VLAN=yes')
			if ip and netmask:
				self.addOutput(host, 'IPADDR=%s' % ip)
				self.addOutput(host, 'NETMASK=%s' % netmask)
			if dhcp:
				self.addOutput(host, 'BOOTPROTO=dhcp')
		else:
			self.addOutput(host, 'BRIDGE="%s"' % brName)
		if active :
			self.addOutput(host, 'ONBOOT=yes')
		else : 
			self.addOutput(host, 'ONBOOT=no' )
		self.addOutput(host, 'BOOTPROTO=none' )
		if mtu:
			self.addOutput(host, 'MTU=%s' % mtu)
		self.addOutput(host, '</file>')

		if not vlanid:
			#    ------      bridge dev with IP
			s = '<file name="/etc/sysconfig/network-scripts/ifcfg-'
			s += '%s">' % brName
			self.addOutput(host, s)
			self.addOutput(host, 'DEVICE=%s' % brName)
			self.addOutput(host, 'TYPE=Bridge')
			if ip and netmask:
				self.addOutput(host, 'IPADDR=%s' % ip)
				self.addOutput(host, 'NETMASK=%s' % netmask)
			if dhcp:
				self.addOutput(host, 'BOOTPROTO=dhcp')
			else:
				self.addOutput(host, 'BOOTPROTO=none' )
			if active :
				self.addOutput(host, 'ONBOOT=yes')
			else : 
				self.addOutput(host, 'ONBOOT=no' )
			if mtu:
				self.addOutput(host, 'MTU=%s' % mtu)
			self.addOutput(host, '</file>')
		




	def writeConfig(self, host, mac, ip, device, netmask, vlanid, mtu,
			options, channel):

		configured = 0

		# Should we set up DHCP on this device?
		testOptions="%s" % options
		if re.match('dhcp', testOptions.lower()):
			dhcp = 1 # tell device to dhcp, explicitly
		else:
			dhcp = 0

		reg = re.compile('bond[0-9]+')

		self.addOutput(host, 'DEVICE=%s' % device)

		if mac:
			self.addOutput(host, 'HWADDR=%s' % mac)

		if ip and netmask:
			if dhcp:
				self.addOutput(host, 'BOOTPROTO=dhcp')
			else:	
				self.addOutput(host, 'IPADDR=%s' % ip)
				self.addOutput(host, 'NETMASK=%s' % netmask)
				self.addOutput(host, 'BOOTPROTO=none')

			self.addOutput(host, 'ONBOOT=yes')

			if reg.match(device) and options:
				self.addOutput(host, 'BONDING_OPTS="%s"' %
					options)

			configured = 1

		if vlanid:
			self.addOutput(host, 'VLAN=yes')
			self.addOutput(host, 'ONBOOT=yes')
			configured = 1

		#
		# check if this is part of a bonded channel
		#
		if channel and reg.match(channel):
			self.addOutput(host, 'BOOTPROTO=none')
			self.addOutput(host, 'ONBOOT=yes')
			self.addOutput(host, 'MASTER=%s' % channel)
			self.addOutput(host, 'SLAVE=yes')
			configured = 1

		if not configured:
			if dhcp:
				self.addOutput(host, 'BOOTPROTO=dhcp')
				self.addOutput(host, 'ONBOOT=yes')
			else:
				self.addOutput(host, 'BOOTPROTO=none')
				self.addOutput(host, 'ONBOOT=no')

		if mtu:
			self.addOutput(host, 'MTU=%s' % mtu)
		

	def writeModprobe(self, host, device, module, options):
		if not module:
			return

		reg = re.compile('bond[0-9]+')

		self.addOutput(host, '<![CDATA[')
		self.addOutput(host, 'grep -v "\<%s\>" /etc/modprobe.conf > /tmp/modprobe.conf' % (device))

		self.addOutput(host,
			"echo 'alias %s %s' >> /tmp/modprobe.conf" %
			(device, module))

		#
		# don't write the options here if this is a bonded interface,
		# they written in the ifcfg-bond* file (see writeConfig() above)
		#
		if options and not reg.match(device):
			self.addOutput(host,
				"echo 'options %s %s' >> /tmp/modprobe.conf" %
				(module, options))

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

		self.endOutput(padChar = '')

	def run_sunos(self, host):
		# Ignore IPMI devices and get all the other configured
		# interfaces
		self.db.execute("select networks.ip, networks.device, "	+\
				"subnets.netmask from networks, nodes, " +\
				"subnets where nodes.name='%s' " % (host)+\
				"and networks.subnet=subnets.id " +\
				"and networks.device!='ipmi' "	+\
				"and networks.node=nodes.id")

		for row in self.db.fetchall():
			(ip, device, netmask) = row
			if ip is not None:
				self.write_host_file_sunos(ip, netmask, device)
		
		# Get all the IPMI interfaces
		self.db.execute("select networks.ip, networks.module, " +\
				"subnets.netmask from networks, nodes, "+\
				"subnets where nodes.name='%s' " %(host)+\
				"and networks.device='ipmi' "		+\
				"and networks.subnet=subnets.id "		+\
				"and networks.node=nodes.id")

		for row in self.db.fetchall():
			(ip, channel, netmask) = row
			self.addOutput(host, 'ipmitool lan set %s ipsrc static'
				% (channel))
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
	
	def write_host_file_sunos(self, ip, netmask, device):
		s = '<file name="/etc/hostname.%s">\n' % device
		s += "%s netmask %s\n" % (ip, netmask)
		s += '</file>\n'
		self.addText(s)
		
	def run_linux(self, host):
		self.db.execute("""select distinctrow 
			net.mac, net.ip, net.device,
			if(net.subnet, s.netmask, NULL), net.vlanid,
			net.subnet, net.module, s.mtu, net.options, net.channel
			from
			networks net, nodes n, subnets s where net.node = n.id
			and if(net.subnet, net.subnet = s.id, true) and
			n.name = "%s" order by net.id""" % (host))


		for row in self.db.fetchall():
			(mac, ip, device, netmask, vlanid, subnetid, module,
				mtu, options, channel) = row

			testOptions="%s" % options
			if re.match('noreport', testOptions.lower()):
				continue # don't do anything if noreport set

			if device == 'ipmi':
				self.writeIPMI(host, ip, channel, netmask)
				continue # ipmi is special, skip the standard stuff
			if device and device[0:4] != 'vlan':
				#
				# output a script to update modprobe.conf
				#
				self.writeModprobe(host, device, module,
					options)

			if vlanid:
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
						netmask, vlanid, mtu, options,
						channel)
			else:
				if self.isKVMContainer(host):
					#we have to set up bridged devices
					if vlanid != None and ip == None:
						#vlan interface are not configured by RH network script!
						pass
					else:
						if subnetid:
							#active interface
							self.writeBridgedConfig(host, mac, ip, device,
								netmask, vlanid, mtu, options, channel, True)
						else:
							#inactive... don't bring it up when you boot
							self.writeBridgedConfig(host, mac, ip, device,
								netmask, vlanid, mtu, options, channel, False)
				else:
					s = '<file name="'
					s += '/etc/sysconfig/network-scripts/ifcfg-'
					s += '%s">' % (device)
					self.addOutput(host, s)
					self.writeConfig(host, mac, ip, device,
						netmask, vlanid, mtu, options, channel)
					self.addOutput(host, '</file>')


