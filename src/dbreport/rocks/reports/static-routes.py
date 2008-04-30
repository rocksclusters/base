#! /opt/rocks/bin/python
#
# Creates static-route files from the routes table 
# $Id: static-routes.py,v 1.14 2008/03/06 23:41:41 mjk Exp $
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
# $Log: static-routes.py,v $
# Revision 1.14  2008/03/06 23:41:41  mjk
# copyright storm on
#
# Revision 1.13  2008/02/26 21:41:27  bruno
# proper location of hostname
#
# Revision 1.12  2008/02/22 20:09:30  bruno
# fix error message
#
# Revision 1.11  2007/06/23 04:03:21  mjk
# mars hill copyright
#
# Revision 1.10  2006/09/11 22:47:08  mjk
# monkey face copyright
#
# Revision 1.9  2006/08/10 00:09:30  mjk
# 4.2 copyright
#
# Revision 1.8  2006/01/16 06:48:57  mjk
# fix python path for source built foundation python
#
# Revision 1.7  2005/11/02 19:33:32  phil
# Make it a host route when netmask=32 and gateway is defined
#
# Revision 1.6  2005/10/12 18:08:37  mjk
# final copyright for 4.1
#
# Revision 1.5  2005/10/01 19:17:01  bruno
# fix for 'host' routes
#
# Revision 1.4  2005/09/21 22:12:19  phil
# Create dev/host routes
#
# Revision 1.3  2005/09/16 01:02:16  mjk
# updated copyright
#
# Revision 1.2  2005/09/15 22:45:09  mjk
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
# Revision 1.1  2005/08/03 17:42:16  phil
# add to the base. update copyright. Use rocks foundation.
#
# Revision 1.1  2005/06/13 18:11:30  phil
# checkin
#
# Revision 1.1  2005/04/23 00:38:18  phil
# Add a static-routes dbreport
#
# Revision 1.1  2005/04/23 00:32:28  phil
# A DB report that uses the routes table to make
# static route entries
#
# Revision 1.3  2005/04/02 06:05:02  phil
# Small edge condition checks.
#
# Revision 1.2  2005/03/29 04:46:26  phil
# writes modules alias file.
#
# Revision 1.1  2005/03/29 04:26:59  phil
# ifcfg.py is a dbreport that creates standard ethernet configuration files
#

import os
import string
import rocks.ip
import time
import types
import re
import rocks.reports.base


class Report(rocks.reports.base.ReportBase):

	def getNodeId(self):
		# Get the id of the installing node

		self.execute('select ID from nodes where name="%s" '
			% self.hostname)
		try:
			return self.fetchone()[0]
		except:
			raise Exception, "Node %s missing from database" \
				% self.hostname

	def getMemberId(self):
		# Get the membership of the installing node

		self.execute('select membership from nodes where name="%s" '
			% self.hostname)
		try:
			return self.fetchone()[0]
		except:
			raise Exception, "Node %s missing from database" \
				% self.hostname

	def print_route(self,network,netmask,gateway,device):
		#
		# print routes. of Gateway looks like and IP assume gw form
		# otherwise assume device form
		#
		# Examples of Database entry vs what is printed:
                #  IP            |  Mask   |   GW          | Device
		#  137.110.246.0 |      24 | 137.110.243.1 | NULL   |
		#      any net 137.110.246.0/24 gw 137.110.243.1
                #  137.110.247.0 |      24 | NULL          | eth0   |
		#      any net 137.110.246.0/24 dev eth0 
                #  137.110.247.8 |      32 | NULL          | eth0   |
		#      any host 137.110.246.0 dev eth0 

		ip_address= re.compile("([0-9]+\.)+")

		if gateway is not None :
			if netmask != 32:
				print 'any net %s/%s gw %s' %(network,netmask,gateway)
			else:
				print 'any host %s gw %s' %(network,gateway)

		elif netmask != 32 : 
			print 'any net %s/%s dev %s' %(network,netmask,device)
		else :
			print 'any host %s dev %s' %(network,device)

	
	def build_global_routes(self):
		#
		# build group routes
		#

		self.execute('select network,netmask,gateway,device ' +
			'from routes where owner="node" and ' +
			'ID=0')
		for row in self.fetchall() :
			network = row[0]
			netmask = row[1]
			gateway = row[2]
			device = row[3]
			self.print_route(network,netmask,gateway,device)

	def build_group_routes(self):
		#
		# build group routes
		#

		self.execute('select network,netmask,gateway,device ' +
			'from routes where owner="membership" and ' +
			'ID=%d' % (self.memberid))
		for row in self.fetchall() :
			network = row[0]
			netmask = row[1]
			gateway = row[2]
			device = row[3]
			self.print_route(network,netmask,gateway,device)

	def build_node_routes(self):
		#
		# build group routes
		#

		self.execute('select network,netmask,gateway,device ' +
			'from routes where owner="node" and ' +
			'ID=%d' % (self.nodeid))
		for row in self.fetchall() :
			network = row[0]
			netmask = row[1]
			gateway = row[2]
			device = row[3]
			self.print_route(network,netmask,gateway,device)

	def run(self):
		"Creates static-routes for a hostname" 

		usage = "dbreport static-routes <hostname>" 
		self.ifcfg = '/etc/sysconfig/network-scripts/static-routes'
		self.hostname=""
		comment="#"

		if len(self.args):
			if self.args[0] in ("help","--help"):
				print usage
				return
			self.hostname = self.args[0]

		self.nodeid=self.getNodeId()
		self.memberid=self.getMemberId()

		print self.getHeader(comment)
		print '# Global routes'
		self.build_global_routes()
		print '# Member routes'
		self.build_group_routes()
		print '# Node Routes'
		self.build_node_routes()
