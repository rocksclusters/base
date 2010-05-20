# $Id: __init__.py,v 1.8 2010/05/20 00:16:12 bruno Exp $
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
# Revision 1.8  2010/05/20 00:16:12  bruno
# new code to add MAC addresses to the database and to track which interface
# is the private one
#
#

import os
import re
import rocks.commands

class Command(rocks.commands.config.host.command):
	"""
	Adds host interfaces to the database based on the settings of
	the environmental variables HTTP_X_RHN_PROVISIONING_MAC*.

	This command should only be called from kickstart.cgi.

	<arg type='string' name='host'>
	Host name of machine
	</arg>
	"""

	def swap(self, host, old_mac, old_iface, new_mac, new_iface):
		#
		# swap two interfaces
		#
		rows = self.db.execute("""select id from networks where
			mac = '%s' and node = (select id from nodes where
			name = '%s') """ % (old_mac, host))
		if rows != 1:
			return

		old_id, = self.db.fetchone()

		rows = self.db.execute("""select id from networks where
			mac = '%s' and node = (select id from nodes where
			name = '%s') """ % (new_mac, host))
		if rows != 1:
			return

		new_id, = self.db.fetchone()

		self.db.execute("""update networks set mac = '%s',
			device = '%s' where id = %s""" % (old_mac, old_iface,
			new_id))

		self.db.execute("""update networks set mac = '%s',
			device = '%s' where id = %s""" % (new_mac, new_iface,
			old_id))


	def run(self, params, args):
		hosts = self.getHostnames(args)

		if len(hosts) != 1:	
			self.abort('must supply only one host')

		sync_config = 0

		host = hosts[0]

		#
		# get the environmental variables
		#
		discovered_macs = [] 

		for i in os.environ:
			if re.match('HTTP_X_RHN_PROVISIONING_MAC_[0-9]+', i):
				devinfo = os.environ[i].split()
				iface = devinfo[0]
				macaddr = devinfo[1].lower()
				module = devinfo[2] 

				ks = ''
				if len(devinfo) > 3:
					ks = 'ks'

				discovered_macs.append((iface, macaddr,
					module, ks))

		#
		# make sure all the MACs are in the database
		#
		for (iface, mac, module, ks) in discovered_macs:
			rows = self.db.execute("""select mac from networks
				where mac = '%s' """ % (mac))
			if rows == 0:
				#
				# the mac is not in the database. but check
				# if the interface is already in the database.
				# if so, # then we just need to set the MAC
				# for the interface.
				#
				rows = self.db.execute("""select * from
					networks where device = '%s' and
					node = (select id from nodes where
					name = '%s')""" % (iface, host))

				if rows == 1:
					self.command('set.host.interface.mac',
						(host, 'iface=%s' % iface,
						'mac=%s' % mac))
				else:
					self.command('add.host.interface', 
						(host, 'iface=%s' % iface,
						'mac=%s' % mac))

				sync_config = 1

		#
		# update the iface-to-mac mapping
		#
		for (iface, mac, module, ks) in discovered_macs:
			self.command('set.host.interface.iface', 
				(host, 'iface=%s' % iface,
					'mac=%s' % mac))

		#
		# let's see if the private interface moved
		#
		for (iface, mac, module, ks) in discovered_macs:
			if ks != 'ks':
				continue

			rows = self.db.execute("""select mac,device from
				networks where subnet = (select id from
				subnets where name = 'private') and node =
				(select id from nodes where name = '%s') """
				% (host))
				
			if rows == 1:
				(old_mac, old_iface) = self.db.fetchone()

				if old_mac != mac:
					#
					# the private network moved. swap the
					# networking info for these two
					# interfaces
					#
					self.swap(host, old_mac, old_iface,
						mac, iface)

					sync_config = 1

		if sync_config:
			self.command('sync.config')	

