#
# $Id: ConfigNetworks.py,v 1.13 2008/07/23 00:01:07 bruno Exp $
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
# $Log: ConfigNetworks.py,v $
# Revision 1.13  2008/07/23 00:01:07  bruno
# tweaks
#
# Revision 1.12  2008/07/22 00:34:41  bruno
# first whack at vlan support
#
# Revision 1.11  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.10  2007/06/23 04:03:24  mjk
# mars hill copyright
#
# Revision 1.9  2007/06/20 18:36:08  bruno
# more empty netmask fixes
#
# Revision 1.8  2007/06/11 20:45:32  bruno
# make sure an interface name is assigned to all discovered interfaces
#
# Revision 1.7  2007/06/09 02:41:58  anoop
# You can't compare a NULL value with a known value in SQL.
# Who knew?
# Bug Fix: removes duplicate lines from the networks table when
# a node has more than 1 interface, and the cables are switched
# around.
#
# Revision 1.6  2007/06/09 00:26:00  anoop
# Small cleanup of code
#
# Revision 1.5  2007/05/30 20:43:15  anoop
# *** empty log message ***
#
# Revision 1.4  2006/09/21 04:26:50  bruno
# sort the ethernet interfaces in numerical order. when the devices are
# reassigned (for example, the cable for eth0 is moved), this makes the
# reassignments much more rational.
#
# Revision 1.3  2006/09/11 22:47:22  mjk
# monkey face copyright
#
# Revision 1.2  2006/08/10 00:09:40  mjk
# 4.2 copyright
#
# Revision 1.1  2006/06/21 05:39:52  bruno
# moved to pylib
#
# Revision 1.27  2006/06/16 05:30:23  bruno
# all non-configured interfaces are not enabled
#
# Revision 1.26  2005/10/12 18:09:39  mjk
# final copyright for 4.1
#
# Revision 1.25  2005/09/16 01:03:16  mjk
# updated copyright
#
# Revision 1.24  2005/05/24 21:22:41  mjk
# update copyright, release is not any closer
#
# Revision 1.23  2005/05/23 23:55:27  fds
# Fixed recent checkin log
#
# Revision 1.22  2005/05/23 23:52:43  fds
# Frontend Restore
#
# Revision 1.21  2005/03/31 04:29:01  phil
# only update the networks table if any macs have changed.
# This will happen
# a) the first time node installs
# b) if cable is switched
# c) new ethernet devices are added
#
# This allows a user to more extensively reassign the MAC <--> logical interface
# and have those changes remain between installs.
#
# known edge condition: if b) or c) and other ethernet devices have IP's assigned
# with add-extra-nic and the  #interfaces > 2, other interfaces will likely get their logical mapping changed. The end user then readjusts the networks table mapping and reinstalls to fix (eth0 is always right, no matter what).
#
# Revision 1.20  2005/03/31 03:47:29  bruno
# changed references to modules.conf to modprobe.conf
#
# Revision 1.19  2005/03/12 00:01:53  bruno
# minor checkin
#
# Revision 1.18  2004/10/22 05:14:45  mjk
# python, c, what hell language am I in?
#
# Revision 1.17  2004/10/22 05:02:00  mjk
# allow device routes (no gateway)
#
# Revision 1.16  2004/10/19 01:01:26  fds
# fixed --membership kcgi flag case.
#
# Revision 1.15  2004/08/27 23:00:17  fds
# Tweaks. Threw away some dead code.
#
# Revision 1.14  2004/08/26 23:11:32  fds
# Shepherd has his staff. Tested and looking good.
#
# Revision 1.13  2004/08/24 01:56:55  fds
# New insert-ethers --update structure (need to run as root).
#
# Revision 1.12  2004/08/20 23:51:43  fds
# Dont mess with database if being run on cmdline.
#
# Revision 1.11  2004/08/17 17:17:09  fds
# Does not rely on name in nodes table.
#
# Revision 1.10  2004/08/17 03:19:29  bruno
# added support for configuring IP address for IB and myrinet interfaces
#
# Revision 1.9  2004/08/16 20:41:37  fds
# Support for cluster shepard. Broke code into smaller functions
# for readability and maintaining. Kept old logic.
#
# Revision 1.8  2004/04/17 00:18:21  bruno
# made the code a bit more lean.
#
# this didn't need to be done, but it was the first attempt at trying to
# solve the frontend overload problem (the real fix is in loader -- see ftp.c).
#
# but, since this works, let's check it in.
#
# Revision 1.7  2004/04/12 18:19:06  bruno
# kickstart from any network, even if the node has different types of
# network cards
#
# Revision 1.6  2004/03/25 03:16:07  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.5  2004/03/04 19:57:49  bruno
# added gateway column to networks table -- it is populated by add-extra-nic
# and ConfigNetworks writes the GATEWAY field into the ifcfg file
#
# Revision 1.4  2004/03/04 00:02:42  bruno
# cleanup
#
# Revision 1.3  2004/02/13 20:13:24  bruno
# restart rocks services when needed
#
# Revision 1.2  2004/02/13 05:47:47  bruno
# touch ups
#
# Revision 1.1  2004/02/04 17:39:39  bruno
# on what interface do you want to install?
#
#

import os
import string
import re
import sys
import syslog
import rocks.sql

#
# uncomment for testing
#
#os.environ['HTTP_X_RHN_PROVISIONING_MAC_0'] = 'eth0 00:09:3d:00:09:61 tg3'
#os.environ['HTTP_X_RHN_PROVISIONING_MAC_1'] = 'eth1 00:09:3d:00:08:fd tg3 ks'
#os.environ['HTTP_X_RHN_PROVISIONING_MAC_2'] = 'eth0 00:07:e9:03:ee:49 tg3'
#os.environ['HTTP_X_RHN_PROVISIONING_MAC_3'] = 'eth1 00:07:e9:03:ee:48 fat'
#os.environ['Node_Hostname'] = 'compute-0-0'

class App(rocks.sql.Application):

	def __init__(self):
		rocks.sql.Application.__init__(self)
		self.ifcfg = '/etc/sysconfig/network-scripts/ifcfg'
		self.route = '/etc/sysconfig/static-routes'

		self.install_nic = ''
		self.node_id = 0
		self.restart_rocks_services = 0
		self.discovered_macs = []
		self.macsChanged = 0


	def getMacs(self):
		#
		# extract the mac address from the installing node's
		# request and find which node it should be associated to
		#
	
		devnames = {}

		for i in os.environ:
			if re.match('HTTP_X_RHN_PROVISIONING_MAC_[0-9]+', i):
				devinfo = string.split(os.environ[i])
				device = devinfo[0]
				macaddr = string.lower(devinfo[1])
				module = devinfo[2]

				#
				# get the number of the ethernet device.
				# that way, we can do a numeric sort rather
				# than an alphabetical sort.
				#
				d = string.split(device, 'eth')
				if len(d) > 1:
					try: 
						devnames[int(d[1])] = \
							(macaddr, module)
					except:
						pass

				if len(devinfo) > 3 and devinfo[3] == 'ks':
					#
					# this is the ethernet device that
					# we are installing on
					#
					self.install_nic = macaddr

		l = devnames.keys()
		l.sort()
		for dev in l:
			self.discovered_macs.append(devnames[dev])

		hostname = os.environ['Node_Hostname']
		node_id = self.getNodeId(hostname)
		if node_id:
			self.node_id = node_id


	def setPrimary(self):
		"Set the primary device to the MAC we kickstarted from"

		if not self.install_nic:
			return

		self.execute("""select n.id, n.mac from networks n, subnets s
			where n.node = %s and s.name = 'private' and
			n.subnet = s.id and (n.device is NULL or 
			n.device not like 'vlan%%') """
			% self.node_id)

		id, mac = self.fetchone()
		if mac == self.install_nic:
			return

		# We are changing the mac. Important to restart services.

		self.macsChanged = 1
		self.execute('update networks set mac="%s" where id=%s' 
			% (self.install_nic, id))
		self.restart_rocks_services = 1


	def updateModules(self):
		"Keep modules correctly associated with MACs."
		#
		# see if all the incoming MAC address are in the
		# database. if not, then add the missing MAC addresses and
		# associate them with this compute node.
		#

		for (mac, module) in self.discovered_macs:
			self.execute('select module from networks ' +
				'where mac="%s"' % (mac))

			row = self.fetchone()

			if row == None:
				#
				# insert the mac info
				#
				insert = 'insert into networks ' + \
					'(node, mac, module) ' + \
					'values(%d, "%s", "%s")' \
					% (self.node_id, mac, module)

				self.execute(insert)
				self.macsChanged = 1

				#
				# this operation requires that the
				# appropriate rocks services are restarted
				#
				self.restart_rocks_services = 1
			elif row[0] != module:
				#
				# make sure the modules info is up to date
				#
				update = 'update networks set ' + \
					'module = "%s" ' % (module) + \
					'where mac = "%s"' % (mac)

				self.execute(update)


	def adjustPrivateDevice(self):
		"""Check if the installing device changed from the last time.
		Must preserve any network attributes added by 'add-extra-nic'.
		"""
		#
		# using the networks table, get the ID that points to the
		# entry in the nodes table for this installing client
		# 
		self.execute("""select networks.id, networks.mac from
			networks, subnets where networks.node = %d and
			subnets.name = "private" and
			IFNULL(networks.subnet,0) != subnets.id and
			(networks.device is NULL or
			networks.device not like 'vlan%%') """ % (self.node_id))

		for row in self.fetchall():
			id, mac = row
			if mac == self.install_nic:
				# We know this mac is repeated for eth0
				self.execute('delete from networks where id=%s' % id)
				continue


	def assignDeviceNames(self):
		#
		# the installing device will be 'eth0'. the other devices
		# will be named in the order in which they were enumerated
		#
		devicenum = 1

		for (mac, module) in self.discovered_macs:
			#
			# need to make sure that the device
			# and mac addresses are correct.
			#
			# this covers the case when the installation
			# network moves from one interface to another
			#
			if mac == self.install_nic:
				devname = 'eth0'
			else:
				devname = 'eth%d' % (devicenum)
				devicenum = devicenum + 1

			self.execute('select device from networks ' +
				'where mac="%s"' % (mac))
			row = self.fetchone()

			if row != None and row[0] != devname and \
					(self.macsChanged or row[0] == None):

				update = 'update networks set ' + \
					'device = "%s" ' % (devname) + \
					'where mac = "%s"' % (mac)
			
				self.execute(update)

	def addRoute(self, net, mask, gw, dev):
		if gw:
			print('<file name="%s" mode="append">' % (self.route))
			print('any net %s netmask %s gw %s' % (net, mask, gw))
			print('</file>')
		elif dev:
			print('<file name="%s" mode="append">' % (self.route))
			print('any net %s netmask device %s' % (net, mask, dev))
			print('</file>')
		else:
			print('# ConfigNetworks: error no gw or dev for %s' % net)


        def run(self):
		self.connect()
		try:
			self.getMacs()
		except:
			return
		self.setPrimary()
		self.updateModules()
		self.adjustPrivateDevice()
		self.assignDeviceNames()
		self.close()

