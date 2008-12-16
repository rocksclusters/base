# $Id: __init__.py,v 1.2 2008/12/16 00:29:11 bruno Exp $
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
# Revision 1.2  2008/12/16 00:29:11  bruno
# fix
#
# Revision 1.1  2008/12/15 22:27:21  bruno
# convert pxeboot and pxeaction tables to boot and bootaction tables.
#
# this enables merging the pxeaction and vm_profiles tables
#
#

import sys
import string
import rocks.commands
import os

class Command(rocks.commands.set.host.command):
	"""
	Set a bootaction for a host. This action defines what configuration
	is sent back to a host the next time it boots.
	
	<arg type='string' name='host' repeat='1'>
	One or more host names.
	</arg>

	<param type='string' name='action'>
	The label name for the bootaction. For a list of bootactions,
	execute: 'rocks list host bootaction'.

	If no action is supplied, then only the configuration file for the
	list of hosts will be rewritten.
	</param>
		
	<example cmd='set host boot compute-0-0 action=os'>
	On the next boot, compute-0-0 will boot from its local disk.
	</example>
	"""

	def updateBoot(self, nodeid, host, action):
		#
		# just make sure there is a action is defined for this host.
		# we will not be using the result from the query, we just
		# want to know if a action exists for this host.
		#
		rows = self.db.execute("""select action from bootaction where
			(node = %s or node = 0) 
			and bootaction.action = "%s" """ % (nodeid, action))

		if rows < 1:
			self.abort('Boot action ' + 
				'(%s) is not defined ' % (action) +
				'for host (%s)' % (host))

		#
		# is there already an entry in the pxeboot table
		#
		nrows = self.db.execute("""select id from boot where
						node = %s """ % (nodeid))
		if nrows < 1:
			#
			# insert a new row
			#
			self.db.execute("""insert into boot (node, action)
				values(%s, "%s") """ % (nodeid, action))
		else:
			#
			# update an existing row
			#
			bootid, = self.db.fetchone()

			self.db.execute("""update boot set action = "%s"
				where id = %s """ % (action, bootid))
		return


	def getFilename(self, nodeid):
		#
		# convert the ipaddress into a pxeboot configuration file
		# name
		#
		nrows = self.db.execute("""select networks.ip from
			networks,subnets where
			networks.node = %s and subnets.name = "private" and
			networks.subnet = subnets.id and
			(networks.device is NULL or
			networks.device not like 'vlan%%') """ % (nodeid))

		if nrows < 1:
			return None

		ipaddr, = self.db.fetchone()

		filename = '/tftpboot/pxelinux/pxelinux.cfg/'
		for i in string.split(ipaddr, '.'):
			hexstr = '%02x' % (int(i))
			filename += '%s' % hexstr.upper()

		return filename


	def writeDefaultPxebootCfg(self):
		nrows = self.db.execute("""select kernel, ramdisk, args from
			bootaction where action='install' and node = 0 """)

		if nrows == 1:
			kernel, ramdisk, args = self.db.fetchone()

			filename = '/tftpboot/pxelinux/pxelinux.cfg/default'
			file = open(filename, 'w')	
			file.write('default rocks\n')
			file.write('prompt 0\n')
			file.write('label rocks\n')

			if len(kernel) > 6 and kernel[0:7] == 'vmlinuz':
				file.write('\tkernel %s\n' % (kernel))
			if len(ramdisk) > 0:
				if len(args) > 0:
					args += ' initrd=%s' % ramdisk
				else:
					args = 'initrd=%s' % ramdisk
			if len(args) > 0:
				file.write('\tappend %s\n' % (args))

			file.close()

			#
			# make sure apache can update the file
			#
			os.system('chown root.apache %s' % (filename))
			os.system('chmod 664 %s' % (filename))


	def writePxebootCfg(self, node, nodeid):
		#
		# there is a case where the host name may be in the nodes table
		# but not in the boot table. in this case, remove the current
		# configuration file (if it exists) and return
		#
		filename = self.getFilename(nodeid)

		rows = self.db.execute("""select * from boot where
			node = %s """ % (nodeid))
		if rows < 1:
			if filename != None and os.path.exists(filename):
				os.unlink(filename)

			return

		#
		# get the PXE boot kernel, ramdisk and the boot arguments
		#
		nrows = self.db.execute("""select
			bootaction.kernel, bootaction.ramdisk,
			bootaction.args from bootaction, boot where
			boot.node = %s and bootaction.action = boot.action
			and bootaction.node = %s """ % (nodeid, nodeid))

		if nrows == 1:
			kernel, ramdisk, args = self.db.fetchone()
		else:
			#
			# get the global command
			#
			nrows = self.db.execute("""select
				bootaction.kernel, bootaction.ramdisk,
				bootaction.args from bootaction, boot where
				boot.node = %s and
				bootaction.action = boot.action and
				bootaction.node = 0 """ % (nodeid))

			if nrows == 1:
				kernel, ramdisk, args = self.db.fetchone()
			else:
				rocks.commands.Abort('PXE action ' +
					'does not exist ' +
					'for host (%s).' % (node))

		if filename != None:
			file = open(filename, 'w')	
			file.write('default rocks\n')
			file.write('prompt 0\n')
			file.write('label rocks\n')

			if kernel:
				if kernel[0:7] == 'vmlinuz':
					file.write('\tkernel %s\n' % (kernel))
				else:
					file.write('\t%s\n' % (kernel))

			if ramdisk and len(ramdisk) > 0:
				if len(args) > 0:
					args += ' initrd=%s' % ramdisk
				else:
					args = 'initrd=%s' % ramdisk

			if args and len(args) > 0:
				file.write('\tappend %s\n' % (args))

			file.close()

			#
			# make sure apache can update the file
			#
			os.system('chown root.apache %s' % (filename))
			os.system('chmod 664 %s' % (filename))


	# Solaris Function Only
	def writePxegrub(self, host, nodeid):
		rows = self.db.execute("select action from boot"
				" where node='%s'" % (nodeid))

		if rows < 1:
			return
		action, = self.db.fetchone()

		mac_addr = self.get_formatted_mac(host, nodeid)
		grub_conf_file = "/tftpboot/pxelinux/menu.lst.%s" % mac_addr
		try:
			if action == 'os':
				os.unlink(grub_conf_file)
			if action == 'install':
				os.system('/opt/rocks/bin/dbreport grub_menu %s > ' %(host) +
					'%s 2> /dev/null' % (grub_conf_file))
				os.system('chown root.apache %s' % (grub_conf_file))
				os.system('chmod 664 %s' % (grub_conf_file))
		except OSError:
			pass

	# Solaris Function Only
	def get_formatted_mac(self, host, nodeid):
		# Return a properly formatted mac address
		cmd = "select mac from networks where name='%s' " % (host)  +\
			"and node=%d" % (int(nodeid))
		self.db.execute(cmd)
		mac_addr, = self.db.fetchone()

		# The following converts the string from 00:0a:0b:0c:0d:0e to
		# 01000A0B0C0D0E. This is the suffix that pxegrub for solaris
		# can understand. The grub menu.lst files that are created are
		# suffixed with this string
		formatted_mac = ''.join(['01',] + string.upper(mac_addr).split(':'))
		return formatted_mac


	def run(self, params, args):
		(action,) = self.fillParams([('action', )])
		
		if not len(args):
			self.abort('must supply host')

		frontend_host = self.db.getGlobalVar('Kickstart',
			'PrivateHostname')

		for host in self.getHostnames(args):

			if type(host) == type(()):
				host, = host

			#
			# if this host is the frontend, then generate the
			# default configuration file
			#
			if host == frontend_host:
				self.writeDefaultPxebootCfg()

			else:
				#
				# get the nodeid from the nodes table
				#
				self.db.execute("""select nodes.id,
					nodes.os from nodes, memberships 
					where nodes.name = '%s' and
					nodes.membership = memberships.id"""
					% host)

				(nodeid, node_os) = self.db.fetchone()
			
				if action:
					self.updateBoot(nodeid, host, action)

				#
				# only write PXE configuration file for 'real'
				# machines (e.g., not paravirtualized machines)
				#
				physnode = 1

				rows = self.db.execute("""show tables like
					'vm_nodes' """)

				if rows == 1:
					rows = self.db.execute("""select
						vn.id from vm_nodes vn, nodes n
						where vn.node = n.id and
						n.name = "%s" """ % (host))
					if rows == 1:
						physnode = 0

				if physnode:
					if node_os == 'sunos':
						self.writePxegrub(host, nodeid)

					self.writePxebootCfg(host, nodeid)

