# $Id: __init__.py,v 1.14 2012/11/27 00:48:24 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.6 (Emerald Boa)
# 		         version 6.1 (Emerald Boa)
# 
# Copyright (c) 2000 - 2013 The Regents of the University of California.
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
# Revision 1.14  2012/11/27 00:48:24  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.13  2012/05/06 05:48:32  phil
# Copyright Storm for Mamba
#
# Revision 1.12  2011/07/23 02:30:35  phil
# Viper Copyright
#
# Revision 1.11  2010/09/07 23:52:59  bruno
# star power for gb
#
# Revision 1.10  2010/06/30 17:37:33  anoop
# Overhaul of the naming system. We now support
# 1. Multiple zone/domains
# 2. Serving DNS for multiple domains
# 3. No FQDN support for network names
#    - FQDN must be split into name & domain.
#    - Each piece information will go to a
#      different table
# Hopefully, I've covered the basics, and not broken
# anything major
#
# Revision 1.9  2010/04/27 15:41:32  phil
# Tighten up the test for None in a nic name.
#
# Revision 1.8  2009/06/15 23:48:35  bruno
# if a host has an IP address and name (but no device) make sure it shows up
# in /etc/hosts
#
# Revision 1.7  2009/05/01 19:07:01  mjk
# chimi con queso
#
# Revision 1.6  2009/03/21 22:22:55  bruno
#  - lights-out install of VM frontends with new node_rolls table
#  - nuked 'site' columns and tables from database
#  - worked through some bugs regarding entities
#
# Revision 1.5  2009/03/13 17:28:50  bruno
# make a class that can be inherited by lower commands
#
# Revision 1.4  2009/03/04 20:15:31  bruno
# moved 'dbreport hosts' and 'dbreport resolv' into the command line
#
# Revision 1.3  2008/10/18 00:55:56  mjk
# copyright 5.1
#
# Revision 1.2  2008/03/06 23:41:39  mjk
# copyright storm on
#
# Revision 1.1  2008/01/23 19:05:34  bruno
# can now add kernel boot parameters to the running configuration with the rocks
# command line
#
#

import rocks.commands
import rocks.ip
import os.path

class command(rocks.commands.HostArgumentProcessor,
		rocks.commands.report.command):
	pass

class Command(command):
	"""
	Report the host to IP address mapping in the form suitable for
	/etc/hosts.

	<example cmd='report host'>
	Outputs data for /etc/hosts.
	</example>
	"""

	def hostlocal(self, hostsFile):

		# Allow easy addition of extra hosts from a local
		# file.  This change was submitted as a patch from
		# Gouichi Iisaka (HP Japan).

		if os.path.isfile(hostsFile):
			print '# import from %s' % hostsFile
			file = open(hostsFile, 'r')
			for line in file.readlines():
				print line[:-1]
			file.close()


	def extranics(self):
		self.db.execute("""select networks.IP, networks.Name from
			networks,subnets where subnets.name != "private" and
			networks.subnet = subnets.id and
			networks.ip is not NULL order by networks.IP""")

		nodes=[]
		for row in self.db.fetchall():
			node = rocks.util.Struct()
			node.address	= row[0]
			node.name	= [row[1],]
			nodes.append(node)

		for node in nodes:
			if node.name[0] is not None:
				print '%s\t%s' % (node.address,
					' '.join(node.name))


	def hostlines(self, subnet, netmask):

		ip  = rocks.ip.IPGenerator(subnet, netmask)

		domain = self.db.getHostAttr('localhost',
			'Kickstart_PrivateDNSDomain')

		self.db.execute("""select n.id, n.rack, n.rank, a.name
			     from nodes n, appliances a, memberships m 
			     where n.membership=m.id and 
			     m.appliance=a.id order by n.id""")

		nodes=[]
		for row in self.db.fetchall():
			node = rocks.util.Struct()
			node.id		= row[0]
			node.rack	= row[1]
			node.rank	= row[2]
			node.appname	= row[3]
			node.warning    = None

			self.db.execute("""select networks.name, networks.ip
				from networks, subnets where
				networks.node = %d and
				subnets.name = "private" and
				networks.subnet = subnets.id and
				(networks.device not like 'vlan%%' or
				networks.device is NULL)""" %
				(node.id))

			row = self.db.fetchone()
			if row == None:
				continue

			nodes.append(node)
			node.name = [row[0],]
			node.address = row[1]

			if not node.address:
				node.address = ip.dec()

			name  = '%s-%d-%d' % (node.appname, node.rack,
				node.rank)

			# If there is no name in the database, use the
			# generated one.

			if not node.name[0]:
				node.name = [name,]
			
			if node.name[0] != name:
				node.warning = 'originally %s' % name

		# Append names from the Aliases table.
		
		for node in nodes:
			self.db.execute('select name from aliases '
				     'where node = %d' % (node.id))
			for alias, in self.db.fetchall():
				node.name.append(alias)

		# Format the data
		
		for node in nodes:
			fqdn = "%s.%s" % (node.name[0], domain)
			entry = '%s\t%s %s' % (node.address, fqdn,
				' '.join(node.name))
			if node.warning:
				entry = entry + ' # ' + node.warning
			print entry

      
	def run(self, param, args):
		self.beginOutput()
		self.addOutput('localhost', '# Added by rocks report host #')
		self.addOutput('localhost', '#        DO NOT MODIFY       #')
		self.addOutput('localhost', '#  Add any modifications to  #')
		self.addOutput('localhost', '#    /etc/hosts.local file   #\n')
		self.addOutput('localhost','127.0.0.1\tlocalhost.localdomain\tlocalhost\n')

		# First get the zonename for the private Rocks network
		self.db.execute('select dnszone from subnets '	+\
				'where name="private"')
		localzone, = self.db.fetchone()

		# Get a list of all hostnames that are part of the
		# private network. Use the MySQL coalesce function
		# to use name from nodes table if name from networks
		# table is not set/set to NULL
		cmd = 'select nt.ip, a.name, s.dnszone, '	+\
			'coalesce(nt.name,n.name) '		+\
			'from networks nt, subnets s, nodes n '	+\
			'left join aliases a on (a.node=n.id) '	+\
			'where nt.subnet=s.id and nt.ip!="NULL" '	+\
			'and nt.node=n.id order by nt.subnet, nt.name'

		self.db.execute(cmd)

		# The policy we will maintain for every entry in
		# the private zone is the following.
		# <ip> <name>.<private_zone> <name> <alias> <alias>.<private_zone>
		# For all other networks, host entry will be of the format
		# <ip> <name>.<zonename> <alias>.<zonename>
		for (ip, alias, zone, record) in self.db.fetchall():
			# Construct the hosts entry
			# Add <ip> <name>.<zonename>
			h = '%s\t%s.%s' % (ip, record, zone)

			# If it's the private zone
			if zone == localzone:
				# Add the <name> entry
				h = h + '\t' + record
				# and the <alias> entry
				if alias is not None:
					h = h + '\t' + alias
			# Finally add the <alias>.<zonename> entry
			if alias is not None:
				h = h + '\t' + '%s.%s' % (alias, zone)

			self.addOutput('localhost', h)

		# Finally, add the hosts.local file to the list
		hostlocal = '/etc/hosts.local'
		if os.path.exists(hostlocal):
			f = open(hostlocal,'r')
			self.addOutput('localhost','\n# Imported from /etc/hosts.local\n')
			h = f.read()
			self.addOutput('localhost',h)
			f.close()
		
		self.endOutput(padChar='')
