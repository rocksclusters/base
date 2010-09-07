# $Id: __init__.py,v 1.6 2010/09/07 23:53:00 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4 (Maverick)
# 
# Copyright (c) 2000 - 2010 The Regents of the University of California.
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
# Revision 1.6  2010/09/07 23:53:00  bruno
# star power for gb
#
# Revision 1.5  2009/10/14 22:54:05  bruno
# need quotes
#
# Revision 1.4  2009/10/07 19:09:17  bruno
# throttle the number of concurrent connections. useful for large clusters.
# thanks to Roy Dragseth for this fix.
#
# Revision 1.3  2009/10/06 22:42:42  bruno
# patch from anoop
#
# Revision 1.2  2009/05/01 19:07:02  mjk
# chimi con queso
#
# Revision 1.1  2009/03/24 22:24:04  bruno
# moved 'dbreport tentakel' to rocks command line
#
#

import rocks.commands.report

class Command(rocks.commands.report.command):
	"""
        Create a report that can be used to configure tentakel.
        
        <example cmd='report tentakel'>                
        Create a tentakel configuration file.
        </example>
	"""
	
	def run(self, params, args):
		self.addText('set method="rocks"\n')
		self.addText('set maxparallel="100"\n\n')

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

		self.db.execute("""select n.name, n_attr.value, n.rack, a.name
				from nodes as n inner join (memberships m,
				node_attributes n_attr, appliances a) on 
				(n.membership=m.id and m.appliance=a.id 
				and n.id=n_attr.node and n_attr.attr='os'
				and a.name!='frontend')""")

		# The classification of nodes is done as follows.
		# The groups are 
		# 1. Default group, which is a metagroup containing OS
		#    metagroups
		# 2. OS metagroups containing groups classified as
		#    (appliance & os)
		# 3. appliance metagroup containing groups of (appliance & os)
		# 4. rack metagroup containing groups of rack & os
		# 5. appliance & os group containing nodes which belong 
		#    to a particular appliance type and OS type
		# 6. rack & os group containing nodes which belong to
		#    a particular rack and OS type
		# Logically, the OS metagroup and the appliance metagroup
		# are the same

		for (node, osname, rack, appliance) in self.db.fetchall():
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

		self.db.execute("""select n.name, a.name from nodes n, 
			appliances a, memberships m where
			n.membership = m.id and
			m.appliance = a.id and a.name = 'frontend' """)

		frontend_name, frontend_group = self.db.fetchone()
		groups[frontend_group] = []
		groups[frontend_group].append(frontend_name)

		# Start creating the output. First the default group
		self.addText('group default ()\n')
		for group in groups.pop('default'):
			self.addText('\t%s\n' % group)
		self.addText('\n')

		# Get a list of all the remaining groups and 
		# print them out in the format that tentakel will
		# understand. 
		# A note by previous developer - 
		# tentakel uses a lex parses and need all group names
		# to be standard c-tokens 
		for group in groups:
			self.addText('group %s ()\n' % group)
			for i in groups[group]:
				if i.startswith('@'):
					self.addText('\t%s\n' % i)
				else:
					self.addText('\t+%s\n' % i)
			self.addText('\n')

