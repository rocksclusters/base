# $Id: plugin_dns.py,v 1.16 2009/06/26 19:02:15 bruno Exp $
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
# $Log: plugin_dns.py,v $
# Revision 1.16  2009/06/26 19:02:15  bruno
# alias fix.
#
# thanks to Mike Hallock of UIUC for the fix.
#
# Revision 1.15  2009/05/26 23:04:42  bruno
# mo' bugs
#
# Revision 1.14  2009/05/26 21:36:48  bruno
# fix from scott hamilton for subnets that have prefixes larger than 24 bits.
#
# Revision 1.13  2009/05/01 19:07:04  mjk
# chimi con queso
#
# Revision 1.12  2009/03/21 22:22:55  bruno
#  - lights-out install of VM frontends with new node_rolls table
#  - nuked 'site' columns and tables from database
#  - worked through some bugs regarding entities
#
# Revision 1.11  2009/03/13 21:19:16  bruno
# no more riding the shortname
#
# Revision 1.10  2009/03/04 21:31:44  bruno
# convert all getGlobalVar to getHostAttr
#
# Revision 1.9  2008/10/18 00:55:58  mjk
# copyright 5.1
#
# Revision 1.8  2008/09/22 18:34:31  bruno
# vlan fix for the case where a vlan interface is configured with and IP
# but with no hostname
#
# Revision 1.7  2008/08/29 22:12:35  bruno
# fix for reverse.rocks.domain.*.local
#
# Revision 1.6  2008/07/22 00:34:41  bruno
# first whack at vlan support
#
# Revision 1.5  2008/03/06 23:41:40  mjk
# copyright storm on
#
# Revision 1.4  2008/02/19 23:20:24  bruno
# katz made me do it.
#
# Revision 1.3  2007/09/14 18:48:24  bruno
# if there is no short name for an appliance, then don't make an alias for
# it in /var/named/rocks.domain
#
# Revision 1.2  2007/08/08 22:23:34  bruno
# also import reverse domain local entries
#
# Revision 1.1  2007/08/08 22:14:41  bruno
# moved 'dbreport named' and 'dbreport dns' to rocks command line
#
#

import os
import time
import string
import types
import rocks.commands

preamble_template = """
$TTL 3D
@ IN SOA ns.%s. root.ns.%s. (
	%s ; Serial
	8H ; Refresh
	2H ; Retry
	4W ; Expire
	1D ) ; Min TTL
;
	NS ns.%s.
	MX 10 mail.%s.

"""


class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'dns'
		

	def hostonly(self, name):
		"""Returns only the host part of the name Not stictly
		necessary, but protects against wierd node names."""
		return string.split(name,".")[0]

	
	def hostlines(self, file):
		"Lists the name->IP mappings for all hosts"

		file.write("localhost A 127.0.0.1\n")
		file.write("ns A 127.0.0.1\n\n")

		self.db.execute("""select n.id, n.name, n.rack, n.rank,
			a.name from nodes n, appliances a,
			memberships m where n.membership=m.id and
			m.appliance=a.id order by n.id""")

		for row in self.db.fetchall():
			node = rocks.util.Struct()
			node.id = row[0]
			node.names = {}
			node.rack = row[2]
			node.rank = row[3]
			node.appname = row[4]

			# Name each active subnet

			self.db.execute("""select n.ip, s.name, n.name from
				networks n, subnets s where n.node = %d
				and n.subnet=s.id""" % (node.id))

			for ip, subnet, hostname in self.db.fetchall():
				if not ip or not hostname:
					continue

				# Do nothing with FQDN names.
				# Fixes bug #61 (trac.rocksclusters.org)

				if hostname and hostname.find('.') != -1:
					continue 


				# The name in Nodes table is the authority,
				# but can be overridden by the name in the 
				# Networks table.
				if not hostname:
					hostname = row[1]

				if subnet not in node.names:
					node.names[subnet] = []

				# This interface has a name and IP
				node.names[subnet].append( (hostname, ip) )

			# Append canonical names from the Aliases table.
			self.db.execute('select name from aliases '
				     'where node = %d' % (node.id))
			for alias, in self.db.fetchall():
				node.names['private'].append( (alias, None) )
			
			# Talk DNS language. 
			for subnets, names in node.names.items():
				#
				# Address records have an IP - canonical names
				# do not
				#
				cname, addr = names[0]
				for a in names:
					name, addr = a
					alias = self.hostonly(name)
					if (addr is not None):
						file.write('%s A %s\n' %
							(name, addr))
					elif (alias != cname):
						file.write('%s CNAME %s\n' %
							(alias, cname))

			file.write('\n')
				

	def hostlocal(self, outputfile, filename):
		"Appends any manually defined hosts to domain file"

		if os.path.isfile(filename):
			outputfile.write("; import from %s\n" % filename)
			file = open(filename, 'r')
			for line in file.readlines():
				outputfile.write(line)
			file.close()


	def reverseIP(self, addr, mask):
		"Reverses the elements of a dot-decimal address."

		if type(addr) != types.ListType:
			addr = string.split(addr,".")

		addr.reverse()

		clip = mask/8
		if mask % 8:
			clip += 1

		#
		# this is needed if the subnet is prefix is larger than 24.
		# thanks to Scott Hamilton for the fix.
		# 
		if clip == 4:
			clip = 3

		# Only show the host portion of the address.
		addr = addr[:-clip]

		reversed = addr[0]
		for i in addr[1:]:
			reversed = "%s.%s" % (reversed, i)

		return reversed


	def reversehostlines(self, file, subnet):
		"Lists the IP -> name mappings for all hosts. "
		"Handles only IPv4 addresses."

		mask = self.owner.getNetmask()

		self.db.execute('select id,name from nodes')

		for row in self.db.fetchall():
			nodeid, name = row
			self.db.execute("""select networks.ip from
				networks,subnets where networks.node = %d and
				subnets.name = "private" and
				networks.subnet = subnets.id and
				(networks.device is NULL or 
				networks.device not like 'vlan%%') """ % nodeid)
			t_address = self.db.fetchone()
			if t_address is None:
				continue
			else:
				(address, ) = t_address

			if subnet == address[0:len(subnet)]:
				file.write("%s PTR %s.%s.\n" %
					(self.reverseIP(address, mask),
					name, self.dn))


	def writeForward(self, serial):
		file = open('/var/named/rocks.domain', 'w')
		file.write(preamble_template % (self.dn, self.dn, serial,
			self.dn, self.dn))
		self.hostlines(file)
		self.hostlocal(file, '/var/named/rocks.domain.local')
		file.close()


	def writeReverse(self, serial):
		for subnet in self.owner.getSubnets():
			forward_sn = string.join(subnet, '.')

			subnet.reverse()
			reverse_sn = string.join(subnet, '.')

			filename = '/var/named/reverse.rocks.domain.%s'\
				% (reverse_sn)
			file = open(filename, 'w')

			file.write(preamble_template % (self.dn, self.dn,
				serial, self.dn, self.dn))

			self.reversehostlines(file, forward_sn)

			#
			# handle reverse local additions
			#
			# first check if there is a local file present, if not
			# then create a stub file
			#
			filename = '/var/named/reverse.rocks.domain.%s.local' \
				% (reverse_sn)

			if not os.path.exists(filename):
				f = open(filename, 'w')
				f.write('; Extra reverse host mappings here. ')
				f.write('Like:\n')
				f.write(';2.2.2 PTR myhost.local.\n')
				f.close()

			self.hostlocal(file, filename)

			file.close()
			

	def run(self, args):
		serial = int(time.time())
		self.dn = self.db.getHostAttr('localhost',
			'Kickstart_PrivateDNSDomain')

		self.writeForward(serial)
		self.writeReverse(serial)

