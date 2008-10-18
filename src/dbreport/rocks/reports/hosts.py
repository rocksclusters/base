#! /opt/rocks/bin/python
#
# $RCSfile: hosts.py,v $
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
# $Log: hosts.py,v $
# Revision 1.18  2008/10/18 00:55:59  mjk
# copyright 5.1
#
# Revision 1.17  2008/09/08 23:10:50  bruno
# nuke short names from host file
#
# Revision 1.16  2008/07/22 00:34:41  bruno
# first whack at vlan support
#
# Revision 1.15  2008/03/06 23:41:41  mjk
# copyright storm on
#
# Revision 1.14  2008/01/16 22:31:57  bruno
# if the shortname in the appliances field has the string "NULL", then
# don't print an alias in /etc/hosts
#
# Revision 1.13  2007/06/23 04:03:21  mjk
# mars hill copyright
#
# Revision 1.12  2007/05/30 22:48:55  anoop
# Cleanup
#
# Revision 1.11  2006/09/11 22:47:08  mjk
# monkey face copyright
#
# Revision 1.10  2006/08/10 00:09:30  mjk
# 4.2 copyright
#
# Revision 1.9  2006/07/11 22:18:46  bruno
# now that the frontend's info is in the database just like a compute node,
# the 'extranics' function will correctly print the public address of
# the frontend for /etc/hosts
#
# Revision 1.8  2006/01/16 06:48:57  mjk
# fix python path for source built foundation python
#
# Revision 1.7  2005/10/12 18:08:37  mjk
# final copyright for 4.1
#
# Revision 1.6  2005/09/16 01:02:16  mjk
# updated copyright
#
# Revision 1.5  2005/09/15 22:45:09  mjk
# - copyright updated, but not the final notice for 4.1 (ignore this change)
# - resolv.conf now uses "search" domains for private, then public
# - resolv.conf no longer uses "domain" (replaced by "search")
# - named.conf is now created from dbreport (includes rocks.zone)
# - dns.py requires an argument ("zone", or "reverse")
# - dns config removed (now in named)
# - general dns.py cleanup (simpler logic, tossed dead code)
# - removed domain name related functions from base.py
# - added getGlobalVar to base.py (don't have to go through self.sql anymore)
# - did a diff of the reports vs existing files on rocks-153, looks good
#
# Revision 1.4  2005/07/11 23:51:34  mjk
# use rocks version of python
#
# Revision 1.3  2005/05/24 21:21:52  mjk
# update copyright, release is not any closer
#
# Revision 1.2  2005/05/23 23:59:22  fds
# Frontend Restore
#
# Revision 1.1  2005/03/01 02:02:46  mjk
# moved from core to base
#
# Revision 1.20  2004/09/30 14:18:23  mjk
# - Can we just ignore public interface if no IP is present?
# - Might allow us to support DHCP on public side, but still needs a NIC there.
#
# Revision 1.19  2004/06/07 20:47:33  fds
# Geon and others are having problems with our hosts file. This uses the
# PrivateAddress in app_globals to set the IP mapping for the frontend.
#
# Revision 1.18  2004/03/25 03:15:35  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.17  2004/02/28 22:11:47  fds
# Added localhost.localdomain to hosts report. Suggested by Stephen Connolly.
#
# Revision 1.16  2004/02/10 01:44:54  fds
# Schema migration
#
# Revision 1.15  2004/02/04 17:39:37  bruno
# on what interface do you want to install?
#
# Revision 1.14  2003/09/10 00:19:09  mjk
# - removed some dead DHCP pool code
# - Added Gouichi Iisaka (HP) patch to support non-db hosts in /etc/hosts.local
#
# Revision 1.13  2003/08/28 21:14:22  bruno
# new way to generate public name of the host
#
# Revision 1.12  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.11  2003/08/07 23:14:33  fds
# Localhost resolves to frontend public interface
# so MAUI will work.
#
# Revision 1.10  2003/07/16 19:44:45  fds
# Reporting fully-qualified domain names in all cases.
#
# Revision 1.9  2003/06/21 00:23:33  fds
# Better argument handling, defaults to '.local' and is smarter
# about fully-qualified alias names.
#
# Revision 1.8  2003/06/09 21:41:00  fds
# Putting fully-qualified names in hosts.
# This report is complete for the private side network.
#
# Revision 1.7  2003/05/22 16:39:27  mjk
# copyright
#
# Revision 1.6  2003/04/01 23:16:30  fds
# New DNS server dbreports.
#
# Revision 1.5  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.4  2003/01/07 18:26:43  bruno
# fix for sge -- thanks najib
#
# Revision 1.3  2002/10/18 21:33:26  mjk
# Rocks 2.3 Copyright
#
# Revision 1.2  2002/09/13 18:03:55  mjk
# added missing imports
#
# Revision 1.1  2002/09/13 17:55:21  mjk
# Initial checking
#

import os
import string
import rocks.ip
import rocks.reports.base


class Report(rocks.reports.base.ReportBase):
    
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
		self.execute("""select networks.IP, networks.Name from
			networks,subnets where subnets.name != "private" and
			networks.subnet = subnets.id and
			networks.ip is not NULL order by networks.IP""")

		nodes=[]
		for row in self.fetchall():
			node = rocks.util.Struct()
			node.address	= row[0]
			node.name	= [row[1],]
			nodes.append(node)

		for node in nodes:
			if node.name:
				print '%s\t%s' % (node.address,
						  string.join(node.name, ' '))


	def hostlines(self, subnet, netmask):

		ip  = rocks.ip.IPGenerator(subnet, netmask)

		domain = self.getGlobalVar('Kickstart', 'PrivateDNSDomain')

		self.execute('select n.id, n.rack, n.rank, a.name '
			     'from nodes n, appliances a, memberships m '
			     'where n.membership=m.id and '
			     'm.appliance=a.id and n.site=0 '
			     'order by n.id')

		nodes=[]
		for row in self.fetchall():
			node = rocks.util.Struct()
			node.id		= row[0]
			node.rack	= row[1]
			node.rank	= row[2]
			node.appname	= row[3]
			node.warning    = None

			self.execute("""select networks.name, networks.ip from
				networks, subnets where networks.node = %d and
				subnets.name = "private" and
				networks.subnet = subnets.id and
				networks.device not like 'vlan%%' """ %
				(node.id))

			row = self.fetchone()
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
			self.execute('select name from aliases '
				     'where node = %d' % (node.id))
			for alias, in self.fetchall():
				node.name.append(alias)

		# Format the data
		
		for node in nodes:
			fqdn = "%s.%s" % (node.name[0], domain)
			entry = '%s\t%s %s' % (node.address, fqdn,
					    string.join(node.name, ' '))
			if node.warning:
				entry = entry + ' # ' + node.warning
			print entry

      
	def run(self):
		print self.getHeader()
		print '127.0.0.1\tlocalhost.localdomain\tlocalhost' 
		
		# Build the static addresses
		
		netmask = self.sql.getGlobalVar('Kickstart', 'PrivateNetmask')
		network = self.sql.getGlobalVar('Kickstart', 'PrivateNetwork')

		self.hostlines(network, netmask)
		self.extranics()
		self.hostlocal('/etc/hosts.local')

