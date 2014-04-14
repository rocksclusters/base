#! /opt/rocks/bin/python
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 6.1.1 (Sand Boa)
# 
# Copyright (c) 2000 - 2014 The Regents of the University of California.
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
# $Log: clusterdb.py,v $
# Revision 1.24  2012/11/27 00:48:40  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.23  2012/05/06 05:48:46  phil
# Copyright Storm for Mamba
#
# Revision 1.22  2011/07/23 02:30:49  phil
# Viper Copyright
#
# Revision 1.21  2010/09/07 23:53:08  bruno
# star power for gb
#
# Revision 1.20  2009/05/08 22:14:34  anoop
# Add os attribute to the node_attributes table
#
# Revision 1.19  2009/05/01 19:07:08  mjk
# chimi con queso
#
# Revision 1.18  2009/03/23 23:03:57  bruno
# can build frontends and computes
#
# Revision 1.17  2008/10/18 00:56:02  mjk
# copyright 5.1
#
# Revision 1.16  2008/07/23 00:29:55  anoop
# Modified the database to support per-node OS field. This will help
# determine the kind of provisioning for each node
#
# Modification to insert-ethers, rocks command line, and pylib to
# support the same.
#
# Revision 1.15  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.14  2007/06/23 04:03:24  mjk
# mars hill copyright
#
# Revision 1.13  2007/06/09 00:27:08  anoop
# Again, moving away from using device names, to using subnets.
#
# Revision 1.12  2007/06/06 20:28:00  bruno
# need to set the device to eth0 when insert-ethers discovers a redhat rocks
# machine
#
# Revision 1.11  2007/06/05 16:38:37  anoop
# Modified clusterdb.py to accomadate changes to the database schema. Now
# just a little less buggy than my other checkins. Sorry for the delay
#
# Revision 1.10  2007/05/30 20:43:15  anoop
# *** empty log message ***
#
# Revision 1.9  2006/09/11 22:47:23  mjk
# monkey face copyright
#
# Revision 1.8  2006/08/10 00:09:41  mjk
# 4.2 copyright
#
# Revision 1.7  2006/01/16 06:48:59  mjk
# fix python path for source built foundation python
#
# Revision 1.6  2005/10/12 18:08:42  mjk
# final copyright for 4.1
#
# Revision 1.5  2005/09/16 01:02:21  mjk
# updated copyright
#
# Revision 1.4  2005/07/11 23:51:35  mjk
# use rocks version of python
#
# Revision 1.3  2005/05/24 21:21:57  mjk
# update copyright, release is not any closer
#
# Revision 1.2  2005/05/23 23:59:24  fds
# Frontend Restore
#
# Revision 1.1  2005/03/31 02:32:09  fds
# Initial design. Knows how to safely insert nodes into the cluster db.
#
#

import os


class Nodes:
	"""A class that knows how to insert/delete rocks appliances from
	the cluster database"""

	def __init__(self, sql):
		# An open connection to the cluster database. (a rocks.sql.App)
		self.sql = sql
		self.nodeid = -1

	def getNodeId(self):
		"Returns the id of the last node inserted"
		return self.nodeid
		
	def insert(self, name, mid, rack, rank, mac=None, ip=None,
			netmask=None, subnet='private', osname='linux'):

		"""Inserts a new node into the database. Optionally inserts
		networking information as well."""

		self.checkName(name)
		self.checkMembership(mid)
		self.checkMAC(mac)
		self.checkIP(ip)
		self.checkSubnet(subnet)
		
		#
		# create a new row in nodes table
		#
		insert = ('insert into nodes (name,membership,rack,rank,os) '
			'values ("%s", %d, %d, %d, "%s") ' %
			(name, mid, rack, rank, osname))

		self.sql.execute(insert)

		# The last insert id.
		nodeid = self.sql.insertId()

		# Do not go further if there is no networking info.
		if ip is None:
			return

		#
		# now create a new row in the networks table
		#
		# First get the subnet you want to insert the node into. The
		# default is "private", but this should be dynamic enough
		# to accept any kind of string that is valid
		
		self.sql.execute("select id from subnets where name='%s'"
								% (subnet))
		subnet_id = int(self.sql.fetchone()[0])
		
		if mac is None:
			# Happens for a frontend
			insert = ('insert into networks '
				'(node,ip,netmask,name,subnet) '
				'values (%d, "%s", "%s", "%s", %d) '
				% (nodeid, ip, netmask, name, subnet_id))
		else:
			insert = ('insert into networks '
				'(node,mac,ip,netmask,name,subnet) '
				'values (%d, "%s", "%s", "%s", "%s", %d) '
				% (nodeid, mac, \
						ip, netmask, name, subnet_id))

		self.sql.execute(insert)
		self.nodeid = nodeid

		# Set the value of the OS in the host attributes table
		db_cmd = ('insert into node_attributes '
			'(node, attr, value) '
			'values (%d, "%s","%s")' % (nodeid, 'os', osname))

		self.sql.execute(db_cmd)

	def checkName(self, checkname):
		"""Check to make sure we don't insert a duplicate node name or
		other bad things into the DB"""

		host = self.sql.getNodeId(checkname)
		if host:
			msg = 'Node %s already exists.\n' % checkname
			msg += 'Select a different hostname, cabinet '
			msg += 'and/or rank value.'
			raise ValueError, msg
		msg = self.checkNameValidity(checkname)
		if msg :
			raise ValueError, msg


	def checkNameValidity(self, checkname):
		"""check that the checkname is not an appliance name or it is not
		in the form of rack<number> (used by rocks.command.* too).

		If it is incorrect it return an error string otherwise None
		"""

		# check for invalid names for hosts
		# they can not be in the form of rack<number>
		if checkname.startswith('rack'):
			number = checkname.split('rack')[1]
			try:
				int(number)
				msg = ('Hostname %s can not be in the form ' \
					+ 'of rack<number>.\n') % checkname
				msg += 'Select a different hostname.\n'
				return msg
			except ValueError:
				return None
		# they can not be equal to any appliance name
		self.sql.execute('select name from appliances')
		for name, in self.sql.fetchall():
			if checkname == name:
				msg = 'Hostname %s can not be equal to an appliance'\
					' name.\n' % (checkname)
				msg += 'Select a different hostname.\n'
				return msg
		return None


	def checkSubnet(self,subnet):
		"Check to see if the subnet exists"

		rows = self.sql.execute("select id from subnets where name='%s'" % subnet);
		if (rows == 0):
			msg = "subnet %s does not exist. Bailing out" % (subnet)
			raise KeyError, msg
			return

	def checkIP(self, ipaddr):
		"Check if the address is already in the database"
		
		if ipaddr is None:
			return
		
		nodeid = self.sql.getNodeId(ipaddr)

		if nodeid:
			msg = "Duplicate IP '%s' Specified" % ipaddr
			raise ValueError, msg


	def checkMAC(self, mac):
		"""Mac addresses are unique accross all sites."""

		#
		# check if mac is already in the database
		# Special Handling for literal "None"

		if mac is None:
			return

		query = 'select mac from networks where mac = "%s"' % mac

		if self.sql.execute(query) == 1:
			msg = "Duplicate MAC '%s' Specified" % mac
			raise ValueError, msg


	def checkMembershipName(self, name):

		query='select name from memberships where name="%s" ' % (name)
		
		if self.sql.execute(query) == 0:
			msg = 'Could not find Membership "%s"' % name
			raise ValueError, msg


	def checkMembership(self, mid):
		query='select id from memberships where id="%s"' % mid
		if self.sql.execute(query) == 0:
			msg = 'Invalid Membership ID "%s"' % mid
			raise ValueError, msg
