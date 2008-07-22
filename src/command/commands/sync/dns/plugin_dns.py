# $Id: plugin_dns.py,v 1.6 2008/07/22 00:34:41 bruno Exp $
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
# $Log: plugin_dns.py,v $
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
			a.name, a.shortname from nodes n, appliances a,
			memberships m where n.membership=m.id and
			m.appliance=a.id and n.site=0 order by n.id""")

		for row in self.db.fetchall():
			node = rocks.util.Struct()
			node.id = row[0]
			node.names = {}
			node.rack = row[2]
			node.rank = row[3]
			node.appname = row[4]
			node.appalias = row[5]

			# Name each active subnet

			self.db.execute("""select n.ip, s.name, n.name from
				networks n, subnets s where n.node = %d
				and n.subnet=s.id""" % (node.id))

			for ip, subnet, hostname in self.db.fetchall():
				if not ip:
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

				# Canotical names get an address too.
				node.names[subnet].append( (hostname, ip) )

			# Append names from the Aliases table.
			self.db.execute('select name from aliases '
				     'where node = %d' % (node.id))
			for alias, in self.db.fetchall():
				node.names['private'].append(alias)
			
			# Talk DNS language. 
			for subnets, names in node.names.items():

				# The canotical name is first
				name, addr = names[0]
				cname = self.hostonly(name)
				file.write('%s A %s\n' % (cname, addr))

				for a in names[1:]:
					alias = self.hostonly(a)
					if alias == cname:
						continue
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
		if (mask % 8):
			clip += 1

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

		self.db.execute('select id,name from nodes where site=0')

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
			filename = '/var/named/reverse.rocks.domain.%s.local'\
				% (reverse_sn)
			self.hostlocal(file, filename)
			file.close()
			

	def run(self, args):
		serial = int(time.time())
		self.dn = self.db.getGlobalVar('Kickstart', 'PrivateDNSDomain')

		self.writeForward(serial)
		self.writeReverse(serial)

