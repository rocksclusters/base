#!/opt/rocks/bin/python
#
# $RCSfile: tentakel.py,v $
# $Id: tentakel.py,v 1.4 2008/08/27 02:38:58 anoop Exp $
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
# Revision 1.4  2008/08/27 02:38:58  anoop
# Complete overhaul to the process of generation of the tentakel
# configuration. Now, the tentakel configuration is OS aware,
# and nodes are grouped by OS, rack, and appliance type
#
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
		# print the dbreport header
		print self.getHeader()
		print 
		print 'set method="rocks"'
		print 

		# The groups dictionary that is used to form
		# the entire tree of groups
		groups = {}

		# A default group
		groups['default'] = []

		# Select all nodes that Rocks knows about, except 
		# for the frontend, along with their rack, 
		# appliance_type and OS with which they've
		# been provisioned. This information is used to
		# classify the nodes.
		sql_cmd = "select n.name, n.os, n.rack, a.name " +\
			"from nodes n, appliances a, memberships m "+\
			"where n.membership = m.id and "	 +\
			"m.appliance = a.id and a.name != 'frontend'"

		self.execute(sql_cmd)

		# The classification of nodes is done as follows.
		# The groups are 
		# 1. Default group, which is a metagroup containing OS metagroups
		# 2. OS metagroups containing groups classified as (appliance & os)
		# 3. appliance metagroup containing groups of (appliance & os)
		# 4. rack metagroup containing groups of rack & os
		# 5. appliance & os group containing nodes which belong 
		#    to a particular appliance type and OS type
		# 6. rack & os group containing nodes which belong to
		#    a particular rack and OS type
		# Logically, the OS metagroup and the appliance metagroup
		# are the same

		for (node, osname, rack, appliance) in self.fetchall():
			if not groups.has_key(osname):
				groups[osname] = []
			if '@' + osname not in groups['default']:
				groups['default'].append('@' + osname)

			app_metagroup = appliance.replace('-','_')
			app_group = app_metagroup + '_' + osname
			if not groups.has_key(app_metagroup):
				groups[app_metagroup] = []
			if '@' + app_group not in groups[app_metagroup]:
				groups[app_metagroup].append('@' + app_group)
			if not groups.has_key(app_group):
				groups[app_group] = []
			groups[app_group].append(node)
			
			rack_metagroup = "rack%d" % int(rack)
			rack_group = rack_metagroup + '_' + osname
			if not groups.has_key(rack_metagroup):
				groups[rack_metagroup] = []
			if '@' + rack_group not in groups[rack_metagroup]:
				groups[rack_metagroup].append('@' + rack_group)
			if not groups.has_key(rack_group):
				groups[rack_group] = []
			groups[rack_group].append(node)

			if '@' + app_group not in groups[osname]:
				groups[osname].append('@' + app_group)

		# Create a frontend group, containing only the frontend
		# This will not be a part of the default group
		sql_cmd = "select n.name, a.name from nodes n, " +\
			"appliances a, memberships m where "	 +\
			"n.membership = m.id and "	+\
			"m.appliance = a.id and a.name = 'frontend'"

		self.execute(sql_cmd)
		frontend_name, frontend_group = self.fetchone()
		groups[frontend_group] = []
		groups[frontend_group].append(frontend_name)


		# Start creating the output. First the default group
		print "group default ()"
		for group in groups.pop('default'):
			print "\t%s" % group
		print '\n'

		# Get a list of all the remaining groups and 
		# print them out in the format that tentakel will
		# understand. 
		# A note by previous developer - 
		# tentakel uses a lex parses and need all group names
		# to be standard c-tokens 
		for group in groups:
			print "group %s ()" % group
			for i in groups[group]:
				if i.startswith('@'):
					print '\t%s' % i
				else:
					print '\t+%s' % i
			print '\n'
