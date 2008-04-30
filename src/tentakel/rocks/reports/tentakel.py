#!/opt/rocks/bin/python
#
# $RCSfile: tentakel.py,v $
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
# $Log: tentakel.py,v $
# Revision 1.3  2008/03/06 23:41:46  mjk
# copyright storm on
#
# Revision 1.2  2008/01/25 19:37:30  bruno
# only put nodes that are managed by rocks in /etc/tentakel.conf.
# a managed rocks node is one that has an entry in the 'node' column of
# the appliances table.
#
# also, when getting the name of frontend, don't use the hardcoded value of 1.
# look for the membership name 'Frontend'.
#
# Revision 1.1  2008/01/04 22:44:44  bruno
# moved tentakel from the hpc to the base roll
#
# Revision 1.6  2007/06/23 04:03:45  mjk
# mars hill copyright
#
# Revision 1.5  2006/09/11 22:48:56  mjk
# monkey face copyright
#
# Revision 1.4  2006/08/10 00:11:00  mjk
# 4.2 copyright
#
# Revision 1.3  2006/01/16 06:49:12  mjk
# fix python path for source built foundation python
#
# Revision 1.2  2005/12/30 05:58:31  mjk
# added insert-ethers plugin
#
# Revision 1.1  2005/12/29 23:21:56  mjk
# possible cluster-fork replacement
#

import os
import socket
import string
import rocks.reports.base


class Report(rocks.reports.base.ReportBase):

	def run(self):
		print self.getHeader()
		print 'set method="rocks"'
		print

                # build a list of group and their node members.
		# tentakel uses a lex parses and need all group names
		# to be standard c-tokens so need to change the names a bit

		self.execute("""select n.name, a.name from
			nodes n, appliances a, memberships m where
			(a.node IS NOT NULL and length(a.node) > 0) and
			n.membership = m.id and m.appliance = a.id""")

		groups = {}
		for node,group in self.fetchall():
			grouptoken = group.replace('-', '_')
			if not groups.has_key(grouptoken):
				groups[grouptoken] = []
			groups[grouptoken].append(node)

		# determine the group name for the frontend machine

		self.execute("""select n.name, a.name from
			nodes n, appliances a, memberships m where 
			n.membership = m.id and m.name = 'Frontend' and
			m.appliance = a.id""")

		frontendName, frontendGroup = self.fetchone()

		# build a list of racks to create rack groups in the form
		# racksN where the group contains all non-frontend 
		# machines

		self.execute("""select n.name, n.rack from
			nodes n, appliances a, memberships m where
			(a.node IS NOT NULL and length(a.node) > 0) and
			n.membership = m.id and m.appliance = a.id""")

		racks = {}
		for node,rack in self.fetchall():
			racktoken = 'rack%d' % int(rack)
			if not racks.has_key(racktoken):
				racks[racktoken] = []
			if not node == frontendName:
				racks[racktoken].append(node)
			

		# the default group includes all other groups except the
		# frontend machine

		print 'group default ()'
		for key in groups.keys():
			if key != frontendGroup:
				print '\t@%s' % key
		print

		# print appliance groups

		for key in groups.keys():
			print 'group %s ()' % key
			for node in groups[key]:
				print '\t+%s' % node
			print

		# print rack groups

		for key in racks.keys():
			print 'group %s ()' % key
			for node in racks[key]:
				print '\t+%s' % node
			print

