# $Id: __init__.py,v 1.19 2008/07/23 00:29:55 anoop Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		            version 5.0 (V)
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
# Revision 1.19  2008/07/23 00:29:55  anoop
# Modified the database to support per-node OS field. This will help
# determine the kind of provisioning for each node
#
# Modification to insert-ethers, rocks command line, and pylib to
# support the same.
#
# Revision 1.18  2008/07/22 00:34:41  bruno
# first whack at vlan support
#
# Revision 1.17  2008/03/06 23:41:40  mjk
# copyright storm on
#
# Revision 1.16  2008/02/13 01:04:07  anoop
# Bug fix. Now returns gracefully if the solaris node isn't present
#
# Revision 1.15  2007/12/10 21:28:34  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.14  2007/11/09 02:54:12  anoop
# dbreport grub_menu now takes options.
#
# Revision 1.13  2007/09/10 07:07:05  anoop
# The grub menu.lst file needs to be removed after installation of the host
# is complete. So change permissions so that we can delete the file
#
# Revision 1.12  2007/09/10 06:01:10  anoop
# SOLARIS: Now rocks set host pxeboot can set the pxeboot action for Solaris
# as well. At the moment, pxeaction for solaris not set in database but taken
# from a dbreport output. This'll change later as the software matures.
# The changes should not break anything for Linux, as the changes are solaris
# specific, but YMMV
#
# Revision 1.11  2007/07/05 17:46:45  bruno
# fixes
#
# Revision 1.10  2007/07/04 01:47:40  mjk
# embrace the anger
#
# Revision 1.9  2007/06/29 21:22:05  bruno
# more cleanup
#
# Revision 1.8  2007/06/19 16:42:43  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.7  2007/06/09 00:24:45  anoop
# Moving away from device names.
# Also adding interfaces should make sure that device names
# are checked before subnets. This should change in the future
# but absolutely vital now for things to stay stable
#
# Revision 1.6  2007/06/07 16:43:02  mjk
# - moved host(s) argument processing into a top level class
# - list/dump/set host commands now use this
#
# Revision 1.5  2007/05/31 19:35:43  bruno
# first pass at getting all the 'help' consistent on all the rocks commands
#
# Revision 1.4  2007/05/10 20:37:02  mjk
# - massive rocks-command changes
# -- list host is standardized
# -- usage simpler
# -- help is the docstring
# -- host groups and select statements
# - added viz commands
#
# Revision 1.3  2007/05/02 20:20:53  bruno
# added 'pxeaction' table -- allows for adding and removing pxeboot actions
#
# Revision 1.2  2007/05/01 22:48:26  bruno
# pxeboot works for pxe first and pxe last nodes
#
# Revision 1.1  2007/04/30 22:11:11  bruno
# first pass at pxeboot (pxe first) rocks command line
#
#

import sys
import string
import rocks.commands
import os

class Command(rocks.commands.set.host.command):
	"""
	Set a pxeaction for a host. This action defines what configuration
	is sent back to a host the next time it PXE boots.
	
	<arg type='string' name='host' repeat='1'>
	One or more host names.
	</arg>

	<param type='string' name='action'>
	The label name for the pxeaction. For a list of pxeactions,
	execute: 'rocks list host pxeaction'.

	If no action is supplied, then only the configuration file for the
	list of hosts will be rewritten.
	</param>
		
	<example cmd='set host pxeboot compute-0-0 action=os'>
	Set the 'os' pxeaction for compute-0-0.
	</example>
	"""

	def updatePxeboot(self, nodeid, host, action):
		#
		# just make sure there is a command is defined for this host.
		# we will not be using the result from the query, we just
		# want to know if a command exists for this host.
		#
		rows = self.db.execute("""select command from pxeaction where
			(node = %s or node = 0) 
			and pxeaction.action = "%s" """ % (nodeid, action))

		if rows < 1:
			self.abort('PXE command ' + 
				'(%s) is not defined ' % (action) +
				'for host (%s)' % (host))

		#
		# is there already an entry in the pxeboot table
		#
		nrows = self.db.execute("""select id from pxeboot where
						node = %s """ % (nodeid))
		if nrows < 1:
			#
			# insert a new row
			#
			self.db.execute("""insert into pxeboot (node, action)
				values(%s, "%s") """ % (nodeid, action))
		else:
			#
			# update an existing row
			#
			pxebootid, = self.db.fetchone()

			self.db.execute("""update pxeboot set
				action = "%s" where id = %s """ %
							(action, pxebootid))
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
		nrows = self.db.execute("""select command, args from pxeaction
			where action='install' and node = 0 """)

		if nrows == 1:
			command, args = self.db.fetchone()

			filename = '/tftpboot/pxelinux/pxelinux.cfg/default'
			file = open(filename, 'w')	
			file.write('default rocks\n')
			file.write('prompt 0\n')
			file.write('label rocks\n')
			file.write('\t%s\n' % (command))
			if args != None and args != '':
				file.write('\t%s\n' % (args))
			file.close()

			#
			# make sure apache can update the file
			#
			os.system('chown root.apache %s' % (filename))
			os.system('chmod 664 %s' % (filename))


	def writePxebootCfg(self, node, nodeid):
		#
		# there is a case where the host name may be in the nodes table
		# but not in the pxeboot table. in this case, remove the current
		# configuration file (if it exists) and return
		#
		filename = self.getFilename(nodeid)

		rows = self.db.execute("""select * from pxeboot where
			node = %s """ % (nodeid))
		if rows < 1:
			if filename != None and \
				os.path.exists(filename):

				os.unlink(filename)

			return

		#
		# get the PXE boot command (e.g., the kernel) and the
		# arguments for that command
		#
		nrows = self.db.execute("""select
			pxeaction.command, pxeaction.args from
			pxeaction, pxeboot where pxeboot.node = %s and
			pxeaction.action = pxeboot.action and
			pxeaction.node = %s """ % (nodeid, nodeid))

		if nrows == 1:
			command, args = self.db.fetchone()
		else:
			#
			# get the global command
			#
			nrows = self.db.execute("""select
				pxeaction.command, pxeaction.args from
				pxeaction, pxeboot where pxeboot.node = %s and
				pxeaction.action = pxeboot.action and
				pxeaction.node = 0 """ % (nodeid))

			if nrows == 1:
				command, args = self.db.fetchone()
			else:
				rocks.commands.Abort('PXE command ' +
					'(%s) does not exist ' % (command) +
					'for host (%s).' % (node))

		if filename != None:
			file = open(filename, 'w')	
			file.write('default rocks\n')
			file.write('prompt 0\n')
			file.write('label rocks\n')
			file.write('\t%s\n' % (command))
			if args != None and args != '':
				file.write('\t%s\n' % (args))
			file.close()

			#
			# make sure apache can update the file
			#
			os.system('chown root.apache %s' % (filename))
			os.system('chmod 664 %s' % (filename))


	# Solaris Function Only
	def writePxegrub(self, host, nodeid):
		rows = self.db.execute("select action from pxeboot"
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
					nodes.membership = memberships.id""" % host)

				(nodeid, node_os) = self.db.fetchone()
			
				if action:
					self.updatePxeboot(nodeid, host, action)
			
				if node_os == 'sunos':
					self.writePxegrub(host, nodeid)
				else:
					self.writePxebootCfg(host, nodeid)

