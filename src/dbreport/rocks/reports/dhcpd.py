#! /opt/rocks/bin/python
#
# $RCSfile: dhcpd.py,v $
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
# $Log: dhcpd.py,v $
# Revision 1.19  2008/04/25 22:22:57  bruno
# fixes for V
#
# Revision 1.18  2008/03/06 23:41:41  mjk
# copyright storm on
#
# Revision 1.17  2007/08/15 23:56:38  anoop
# Added solaris support
#
# Revision 1.16  2007/06/23 04:03:21  mjk
# mars hill copyright
#
# Revision 1.15  2007/05/30 22:26:50  anoop
# *** empty log message ***
#
# Revision 1.14  2006/09/11 22:47:08  mjk
# monkey face copyright
#
# Revision 1.13  2006/08/10 00:09:30  mjk
# 4.2 copyright
#
# Revision 1.12  2006/07/06 19:23:23  bruno
# fix syntax errors
#
# Revision 1.11  2006/07/06 17:16:17  bruno
# fix for PXE some clients (e.g., sun java workstation w1100z/w2100z).
# added benefit is that the dhcpd.conf file is simpler.
#
# Revision 1.10  2006/01/16 06:48:57  mjk
# fix python path for source built foundation python
#
# Revision 1.9  2005/10/12 18:08:37  mjk
# final copyright for 4.1
#
# Revision 1.8  2005/10/05 18:25:04  bruno
# add default PXE entry. this will match on PXE requests from older NICs.
#
# thanks to Jesse Becker for the fix.
#
# Revision 1.7  2005/09/16 01:02:16  mjk
# updated copyright
#
# Revision 1.6  2005/09/15 22:45:09  mjk
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
# Revision 1.5  2005/07/11 23:51:34  mjk
# use rocks version of python
#
# Revision 1.4  2005/06/17 06:24:49  phil
# next server needs to be in the kickstart.cgi stanza
# fixes a bug that the dhcp server and the kickstart server had to be the same host. (bruno found bug. Phil tested the two-line fix)
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
# Revision 1.22  2004/08/24 01:30:51  mjk
# next-server was incorrectly set to the gateway, should be the kickstart host
#
# Revision 1.21  2004/05/14 21:20:24  bruno
# added support for etherboot -- this allows folks with only a floppy (no CD,
# no pxe-enabled adapter) to pxe boot their compute nodes
#
# Revision 1.20  2004/04/29 18:30:47  bruno
# ia64 doesn't like as many fields set as x86
#
# Revision 1.19  2004/04/29 00:42:12  bruno
# now match for x86 and ia64 PXE clients
#
# Revision 1.18  2004/03/25 03:15:35  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.17  2004/03/03 20:06:39  bruno
# need a separate entry for each host that has an unassigned IP address
# associated with a MAC address
#
# Revision 1.16  2004/02/06 00:43:55  fds
# Schema migration.
#
# Revision 1.15  2004/02/04 17:39:37  bruno
# on what interface do you want to install?
#
# Revision 1.14  2003/09/25 19:55:43  fds
# Alert in comment for tftp server config.
#
# Revision 1.13  2003/09/25 19:46:10  fds
# DHCPD does pxe without 'pxe' package.
#
# Revision 1.12  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.11  2003/07/16 19:44:44  fds
# Reporting fully-qualified domain names in all cases.
#
# Revision 1.10  2003/06/06 21:00:16  fds
# Last commit not needed, rollback to 1.8
#
# Revision 1.8  2003/05/22 16:39:27  mjk
# copyright
#
# Revision 1.7  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.6  2002/11/08 23:32:24  fds
# We can now have a key with a NULL value and do the right thing.
#
# Revision 1.5  2002/10/18 21:33:26  mjk
# Rocks 2.3 Copyright
#
# Revision 1.4  2002/10/17 23:10:08  fds
# Need to check for empty values as well.
#
# Revision 1.3  2002/10/17 23:02:21  fds
# Do not attempt to print an option if we have no value for it. No DNS servers is ok, we have /etc/hosts.
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
    
	def printOptions(self, prefix, opt, defopt={}):
		map = {}
		map['subnet-mask']         = ('PrivateNetmask',    '')
		map['broadcast-address']   = ('PrivateBroadcast',  '')
		map['domain-name']         = ('PrivateDNSDomain',  '"')
		map['nis-domain']	   = ('PrivateNISDomain',  '"')
		map['routers']		   = ('PrivateGateway',    '')
		map['domain-name-servers'] = ('PrivateDNSServers', '')
		for key in map.keys():
			if opt.has_key(map[key][0]):
				value = opt[map[key][0]]
				# Dont print empty values.
				if not value or not string.strip(value): 
					continue
				quote = map[key][1]
				print '%soption %s %s%s%s;' % (prefix,
							       key,
							       quote,
							       value,
							       quote)

		#
		# drop in the filename option
		#
		override = 0
		try:
			basedir = opt['PrivateKickstartBasedir']
			override = 1
		except KeyError:
			basedir = defopt['PrivateKickstartBasedir']
		try:
			cgi = opt['PrivateKickstartCGI']
			override = 1
		except KeyError:
			cgi = defopt['PrivateKickstartCGI']

		if override:
			#
			# if a filename exist, put in PXE configuration
			#
			cgi = os.path.join(os.sep, basedir, cgi)

			print prefix + 'if (substring (option',
			print 'vendor-class-identifier, 0, 20)'
			print prefix + '\t\t= "PXEClient:Arch:00002") {'
			print prefix + '\t# ia64'
			print prefix + '\tfilename',
			print '"elilo.efi";'
			print prefix + '\tnext-server %s;' % \
				(opt['PrivateKickstartHost'])

			print prefix + '} elsif ((substring (option',
			print 'vendor-class-identifier, 0, 9)'
			print prefix + '\t\t= "PXEClient") or'
			print prefix + '\t(substring (option',
			print 'vendor-class-identifier, 0, 9)'
			print prefix + '\t\t= "Etherboot")) {'
			print prefix + '\t# i386 and x86_64'
			print prefix + '\tfilename',
			print '"pxelinux.0";'
			print prefix + '\tnext-server %s;' % \
				(opt['PrivateKickstartHost'])

			print prefix + '} else {'
			print prefix + '\tfilename "%s";' % (cgi)
			print prefix + '\tnext-server %s;' % \
				(opt['PrivateKickstartHost'])
			print prefix + '}\n'


	def printHost(self, name, hostname, mac, ip, opt, defopt, appliance):
		print '\thost %s {' % name
		if mac:
			print '\t\thardware ethernet %s;'  % mac

		print '\t\toption host-name "%s";' % hostname
		print '\t\tfixed-address %s;'      % ip
		self.printOptions('\t\t', opt, defopt)
		if appliance == 'solaris':
			print '\t\tfilename "pxegrub";'
		print '\t}'

		return
		

	def run(self):
		print self.getHeader()
		dn = self.getGlobalVar('Kickstart', 'PrivateDNSDomain')

		self.execute('select component,value from app_globals '
			     'where membership=0 and site=0 and '
			     'service="Kickstart"')

		defopt = {}
		for key,value in self.fetchall():
			defopt[key] = value

		print 'ddns-update-style none;'
		print 'subnet %s netmask %s {' % (defopt['PrivateNetwork'],
						  defopt['PrivateNetmask'])

		print '\tdefault-lease-time 1200;'
		print '\tmax-lease-time 1200;'

		self.printOptions('\t', defopt)

		print '\t group %s {' % dn 
		ip  = rocks.ip.IPGenerator(defopt['PrivateNetwork'],
					   defopt['PrivateNetmask'])
		
		self.execute('select nodes.id,nodes.name,nodes.rack,nodes.rank,'
			     'appliances.name,memberships.id '
			     'from nodes,appliances,memberships '
			     'where nodes.membership=memberships.id and '
			     'memberships.appliance=appliances.id and '
			     'nodes.site=0 '
			     'order by nodes.id')
		for row in self.fetchall():
			node = rocks.util.Struct()
			node.id		= row[0]
			node.name	= row[1]
			node.rack	= row[2]
			node.rank	= row[3]
			node.appname	= row[4]
			node.membership = row[5]

			self.execute('select component,value from app_globals '
				     'where site=0 and membership=%d and '
				     'service="Kickstart"' % node.membership)
			opt = {}
			for key,value in self.fetchall():
				opt[key] = value
			
			self.execute('select mac,ip from networks,subnets where '
				'networks.node = %d and subnets.name="private" and networks.subnet=subnets.id' 
					% (node.id))
			t_info = self.fetchone()
			if t_info == None:
				node.ip=None
				node.mac=None
				pass
			else:
				(node.mac, node.ip) = t_info

			if not node.ip:
				node.ip = ip.dec()

			if not node.name:
				name  = node.modelname
				if node.rack != None:
					name  = name + '-%d' % node.rack
				if node.rank != None:
					name  = name + '-%d' % node.rank
				node.name = name

			# Go fully-qualified.
			node.name = node.name + "." + dn

			self.printHost(node.name, node.name, node.mac,
				node.ip, opt, defopt, node.appname)

			#
			# associate all unassigned macs to this node
			#
			self.execute('select mac from networks ' + 
					'where node=%d ' % (node.id) +
					'and ip is NULL')
			extramacs = self.fetchall()
	
			i = 1
			for row in extramacs:
				extramac = row[0]
				if extramac is None:
					continue
				self.printHost(node.name + '-%d' % (i),
					node.name, extramac,
					node.ip, opt, defopt, node.appname)
				i = i + 1

		print '}'           ## close the group brace
		print '}'


