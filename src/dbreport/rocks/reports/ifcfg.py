#! /opt/rocks/bin/python
#
# creates ifcfg-eth<n> files and modules.conf files from information in
# the database
#
# $Id: ifcfg.py,v 1.11 2008/10/18 00:55:59 mjk Exp $ 
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
# $Log: ifcfg.py,v $
# Revision 1.11  2008/10/18 00:55:59  mjk
# copyright 5.1
#
# Revision 1.10  2008/03/06 23:41:41  mjk
# copyright storm on
#
# Revision 1.9  2007/06/23 04:03:21  mjk
# mars hill copyright
#
# Revision 1.8  2007/06/19 21:45:19  phil
# ifcfg.py should create interface file correctly. Simplify the SQL statement
#
# Revision 1.7  2007/06/19 18:35:13  bruno
# get the netmask from the subnets table, not the networks table
#
# Revision 1.6  2006/09/11 22:47:08  mjk
# monkey face copyright
#
# Revision 1.5  2006/08/10 00:09:30  mjk
# 4.2 copyright
#
# Revision 1.4  2006/06/20 16:38:52  bruno
# don't write a HWADDR entry if there isn't a hardware address in the database
#
# Revision 1.3  2006/01/16 06:48:57  mjk
# fix python path for source built foundation python
#
# Revision 1.2  2005/10/12 18:08:37  mjk
# final copyright for 4.1
#
# Revision 1.1  2005/09/27 05:33:46  phil
# Generate ifcfg-eth<n> files from database
#
#
#
#
# Call as:
#  dbreport ifcfg eth0 compute-0-0
import os
import string
import rocks.ip
import time
import types
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
				% hostname


	def build_modules(self):
		#
		# build 'modules' 
		#
		self.execute('select module, device ' +
			'from networks where node=%d' % (self.nodeid))
		for row in self.fetchall() :
			module = row[0]
			device = row[1]
			print 'alias %s %s' % (device, module)


	def build_ifcfg(self):
		#
		# build 'ifcfg' 
		#
		nrows=self.execute("""select mac,ip,gateway,subnets.netmask 
			from networks,subnets where device="%s" and
			 node=%d and subnets.id=networks.subnet""" %
			(self.iface,self.nodeid));

		if nrows == 0:
			return

		mac,ip,gateway,netmask = self.fetchone()
		
		print 'DEVICE=%s' % (self.iface)

		#
		# if no mac address is present, then don't write a HWADDR
		# entry. otherwise, it will write 'HWADDR=None' and the
		# interface will not be configured
		#
		if mac != None:
			print 'HWADDR=%s' % (mac)

		if ip and netmask:
			print 'IPADDR=%s' % (ip)
			print 'NETMASK=%s' % (netmask)
			print 'BOOTPROTO=none'
			if gateway:
				print 'GATEWAY=%s' % (gateway)
		else:
			print 'BOOTPROTO=dhcp'

		if ip:
			print 'ONBOOT=yes'
		else:

			print 'ONBOOT=no'


	def run(self):
		"Creates configuration files for an interface/hostname" 

		usage = "dbreport ifcfg <if> <hostname> " 
		self.ifcfg = '/etc/sysconfig/network-scripts/ifcfg'
		self.iface = ""
		self.hostname=""
		self.confModules = 0
		comment="#"

		if len(self.args):
			if self.args[0] in ("help","--help"):
				print usage
				return
			elif self.args[0] in ("modules", "--modules") :
				self.confModules = 1
			else :
				self.iface = self.args[0]
			self.hostname = self.args[1]

		self.nodeid = self.getNodeId()
		print self.getHeader(comment)
		
		if self.confModules :
			self.build_modules()			
		if self.iface != "" and self.hostname != "" :
			self.build_ifcfg()
