# $Id: plugin_physical_host.py,v 1.11 2011/02/14 04:20:39 phil Exp $
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
# $Log: plugin_physical_host.py,v $
# Revision 1.11  2011/02/14 04:20:39  phil
# Treat HVM virtual machines as physical.
#
# Revision 1.10  2011/01/28 22:43:22  bruno
# changed the calls to 'self.abort' to 'print' + 'sys.exit'. we can't
# call abort from a plugin
#
# Revision 1.9  2010/09/07 23:53:01  bruno
# star power for gb
#
# Revision 1.8  2010/08/20 17:57:39  bruno
# make sure the IP is not null
#
# Revision 1.7  2010/07/27 19:51:11  anoop
# Cleaned code: Moved rocks report grub to rocks report host grub
#
# Revision 1.6  2010/05/03 22:50:15  mjk
# - add the ipappend 2 line if ksdevice=bootif arg is in the db
# - add static ip information of ksdevice= is used
#
# Revision 1.5  2009/05/01 19:07:03  mjk
# chimi con queso
#
# Revision 1.4  2009/04/22 02:27:19  anoop
# Moved solaris dbreport to rocks command line
#
# Revision 1.3  2009/03/04 21:31:44  bruno
# convert all getGlobalVar to getHostAttr
#
# Revision 1.2  2009/02/13 20:21:12  bruno
# make sure physical hosts look at the 'runaction' or 'installaction'
# columns in the nodes table in order to reference the correct bootaction.
#
# Revision 1.1  2009/01/16 23:58:15  bruno
# configuring the boot action and writing the boot files (e.g., PXE host config
# files and Xen config files) are now done in exactly the same way.
#
# Revision 1.3  2009/01/14 00:20:56  bruno
# unify the physical node and VM node boot action functionality
#
# - all bootaction's are global
#
# - the node table has a 'runaction' (what bootaction should the node do when
#   a node normally boots) and an 'installaction (the bootaction for installs).
#
# - the 'boot' table has an entry for each node and it dictates what the node
#   will do on the next boot -- it will look up the runaction in the nodes table
#   (for a normal boot) or the installaction in the nodes table (for an install).
#
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

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'physical-host'

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
			bootaction where action='install' """)

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

		nrows = self.db.execute("""select action from boot where
			node = %s """ % (nodeid))
		if nrows < 1:
			if filename != None and os.path.exists(filename):
				os.unlink(filename)

			return
		else:
			action, = self.db.fetchone()

		#
		# get the bootaction from the 'installaction' or
		# 'runaction' column
		#
		if action in [ 'os', 'run' ]:
			nrows = self.db.execute("""select runaction from 
				nodes where name = '%s' """ % node)
		elif action in [ 'install' ]:
			nrows = self.db.execute("""select installaction from 
				nodes where name = '%s' """ % node)
		else:
			print 'action "%s" for host "%s" is invalid' % \
				(action, node)
			sys.exit(-1)

		if nrows == 1:
			bootaction, = self.db.fetchone()
		else:
			print 'failed to get bootaction'
			sys.exit(-1)

		nrows = self.db.execute("""select kernel, ramdisk, args from
			bootaction where action = '%s' """% bootaction)

		if nrows == 1:
			kernel, ramdisk, args = self.db.fetchone()
		else:
			print 'bootaction "%s" for host "%s" is invalid' % \
				(action, node)
			sys.exit(-1)

		# If the ksdevice= is set fill in the ip information
		# a well.  This will avoid the DHCP request inside
		# anaconda.

		if args and args.find('ksdevice=') != -1:
			self.db.execute("""select net.ip
				from networks net, subnets s, nodes n
				where n.name='%s' and net.node=n.id and
				s.id=net.subnet and s.name='private' and
				net.ip is not NULL""" % node)
			ip, = self.db.fetchone()
			args += ' ip=%s ' % ip
			attrs = self.db.getHostAttrs(node)
			args += 'gateway=%s netmask=%s dns=%s nextserver=%s'%(\
				attrs['Kickstart_PrivateGateway'],
				attrs['Kickstart_PrivateNetmask'],
				attrs['Kickstart_PrivateDNSServers'],
				attrs['Kickstart_PrivateKickstartHost'])

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

			# If using ksdevice=bootif we need to
			# pass the PXE information to loader.
			
			if args and args.find('bootif') != -1:
				file.write('\tipappend 2\n')

			file.close()

			#
			# make sure apache can update the file
			#
			os.system('chown root.apache %s' % (filename))
			os.system('chmod 664 %s' % (filename))


	# Solaris Function Only
	def writePxegrub(self, host, nodeid):
		nrows = self.db.execute("select action from boot"
				" where node='%s'" % (nodeid))

		if nrows < 1:
			return
		action, = self.db.fetchone()

		mac_addr = self.get_formatted_mac(host, nodeid)
		grub_conf_file = "/tftpboot/pxelinux/menu.lst.%s" % mac_addr
		try:
			if action == 'os':
				os.unlink(grub_conf_file)
			if action == 'install':
				os.system('/opt/rocks/bin/rocks report host grub %s > ' %(host) +
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


	def run(self, host):
		nrows = self.db.execute("""select id from nodes where
			name = '%s' """ % host)
		if nrows > 0:
			nodeid, = self.db.fetchone()
		else:
			print 'could not find host "%s" in the database' % host
			sys.exit(-1)

		#
		# if this host is the frontend, then generate the
		# default configuration file
		#
		frontend_host = self.db.getHostAttr('localhost',
			'Kickstart_PrivateHostname')

		if host == frontend_host:
			self.writeDefaultPxebootCfg()
		else:
			#
			# only write PXE configuration file for 'real'
			# machines (e.g., not VMs)
			#
			physnode = 1

			nrows = self.db.execute("""show tables like
				'vm_nodes' """)

			if nrows == 1:
				# HVM Virtual Machines act like Physical Hosts. Treat them
				# that way
				nrows = self.db.execute("""select vn.id from
					vm_nodes vn, nodes n
					where vn.node = n.id and
					vn.virt_type != 'hvm' and
					n.name = "%s" """ % (host))
				if nrows == 1:
					physnode = 0

			if physnode:
				node_os = self.db.getHostAttr(host, "os")
				if node_os == 'sunos':
					self.writePxegrub(host, nodeid)

				self.writePxebootCfg(host, nodeid)

