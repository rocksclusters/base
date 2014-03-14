# $Id: __init__.py,v 1.31 2012/11/27 00:48:09 phil Exp $
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
# Revision 1.31  2012/11/27 00:48:09  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.30  2012/05/06 05:48:19  phil
# Copyright Storm for Mamba
#
# Revision 1.29  2011/07/23 02:30:24  phil
# Viper Copyright
#
# Revision 1.28  2011/05/25 19:09:30  anoop
# Missing brackets can ruin your whole day
#
# Revision 1.27  2011/05/24 00:13:15  phil
# Add the appliance name into the category
#
# Revision 1.26  2010/09/14 16:28:28  bruno
# better duplicate checking
#
# Revision 1.25  2010/09/07 23:52:49  bruno
# star power for gb
#
# Revision 1.24  2010/07/27 20:24:37  bruno
# bug fixes
#
# Revision 1.23  2010/07/27 01:38:48  anoop
# Bug fix. DHCP filename by default is always the
# pxe boot file. In this case, "pxelinux.0"; Never kickstart.cgi
#
# Revision 1.22  2010/07/19 18:34:02  anoop
# Individually set "kickstartable", "dhcp_filename" and "dhcp_nextserver"
# attributes for every host/appliance. This way we can control which appliance
# gets the "dhcp_filename" option. This is to resolve a bug where setting
# the dhcp_filename option for devices like switches can cause problems for
# the devices
#
# Revision 1.21  2010/07/14 22:41:14  anoop
# Add the "kickstartable" attribute to appliances. Use this attribute
# to determine if insert-ethers needs to wait for a node to kickstart
# after getting an IP address
#
# Revision 1.20  2010/05/07 23:13:32  bruno
# clean up the help info for the firewall commands
#
# Revision 1.19  2009/05/01 19:06:51  mjk
# chimi con queso
#
# Revision 1.18  2009/03/13 19:44:09  mjk
# - added add.appliance.route
# - added add.os.route
#
# Revision 1.17  2009/03/13 17:29:11  bruno
# cleanup
#
# Revision 1.16  2009/03/13 00:02:59  mjk
# - checkpoint for route commands
# - gateway is dead (now a default route)
# - removed comment rows from schema (let's see what breaks)
# - removed short-name from appliance (let's see what breaks)
# - dbreport static-routes is dead
#
# Revision 1.15  2008/10/18 00:55:48  mjk
# copyright 5.1
#
# Revision 1.14  2008/07/23 00:51:49  anoop
# Modifications to rocks add appliance to support OS field in the database
#
# Revision 1.13  2008/03/06 23:41:34  mjk
# copyright storm on
#
# Revision 1.12  2007/07/05 17:46:45  bruno
# fixes
#
# Revision 1.11  2007/07/04 01:47:37  mjk
# embrace the anger
#
# Revision 1.10  2007/07/03 01:05:18  mjk
# - fillParameters replaced with fillParams (handles default values)
# - fillPamameters is still here and will be deleted soon
# - add appliance cleanup
#
# Revision 1.9  2007/07/02 19:43:58  bruno
# more params/flags cleanup
#
# Revision 1.8  2007/06/19 16:42:40  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.7  2007/06/16 02:39:50  mjk
# - added list roll commands (used for docbook)
# - docstrings should now be XML
# - added parser for docstring to ASCII or DocBook
# - ditched Phil's Network regex stuff (will come back later)
# - updated several docstrings
#
# Revision 1.6  2007/06/11 19:26:58  mjk
# - apache counts as root
# - alphabetized some help flags
# - rocks dump error on arguments
#
# Revision 1.5  2007/06/07 21:23:03  mjk
# - command derive from verb.command class
# - default is MustBeRoot
# - list.command / dump.command set MustBeRoot = 0
# - removed plugin non-bugfix
#
# Revision 1.4  2007/05/11 23:56:02  bruno
# 'rocks add appliance' retooled for latest rocks command line
#
# Revision 1.3  2007/05/10 20:37:00  mjk
# - massive rocks-command changes
# -- list host is standardized
# -- usage simpler
# -- help is the docstring
# -- host groups and select statements
# - added viz commands
#
# Revision 1.2  2007/04/18 21:43:12  bruno
# cleanup
#
# Revision 1.1  2007/04/12 19:48:05  bruno
# added command line: 'rocks add/list/remove appliance'
#
# updated base, hpc, pvfs2 and viz rolls to use new command line.
#
#


import os
import stat
import time
import sys
import string
import rocks.commands

class command(rocks.commands.ApplianceArgumentProcessor,
	rocks.commands.add.command):
	pass

class Command(command):
	"""
	Add an appliance specification to the database.
	
	<arg type='string' name='appliance'>
	The appliance name (e.g., 'compute', 'frontend', 'nas').
	</arg>

	<param type='string' name='graph'>
	The directory name of the graph XML files. The default is 'default'.
	</param>
	
	<param type='string' name='membership'>
	The full membership name of the appliance. This name will be displayed
	in the appliances menu by insert-ethers (e.g., 'NAS Appliance'). If
	not supplied, the membership name is set to the appliance name.
	</param>

	<param type='string' name='node'>
	The name of the root XML node (e.g., 'compute', 'nas', 'viz-tile'). If
	not supplied, the node name is set to the appliance name.
	</param>
	
	<param type='bool' name='public'>
	True means this appliance will be displayed by 'insert-ethers' in 
	the Appliance menu. The default is 'yes'.
	</param>

	<param type='string' name='os'>
	The OS that the appliance type can support. Some appliances can support
	both linux and sunos, where as others can support only one of the two.
	Acceptable values are 'linux' or 'sunos'. Defaults to 'linux'
	</param>

	<param type='string' name='distribution'>
	The rocks distribution that this appliance will use. The distribution must
	be already present in the database (see rocks add distribution).
	Defaults to 'rocks-dist'
	</param>

	<example cmd='add appliance nas membership="NAS Appliance" node=nas graph=default public=yes'>
	</example>
	
	<example cmd='add appliance tile membership=Tile node=viz-tile graph=default public=yes'>
	</example>
	"""

	def run(self, params, args):

		if len(args) != 1:
			self.abort('must supply one appliance')
		app_name = args[0]
					
		(mem_name, node, graph,	public, osname, rocks_distribution) = \
			self.fillParams(
				[('membership', ), 
				('node', ''),
				('graph', ''), 
				('public', 'y'),
				('os','linux'),
				('distribution', 'rocks-dist')])

		public  = self.bool2str(self.str2bool(public))
		
		if node and not graph:
			graph = 'default'

		if not mem_name:
			mem_name = string.capitalize(app_name)

		#
		# check for duplicates
		#
		rows = self.db.execute("""select * from memberships where
			name = "%s" """ % mem_name)
		if rows > 0:
			self.abort('membership "%s" already exists' % mem_name)

		rows = self.db.execute("""select * from appliances where
			name = "%s" """ % app_name)
		if rows > 0:
			self.abort('appliance "%s" already exists' % app_name)

		#
		# ok, we're good to go
		#
		self.db.execute("""insert into appliances 
			(name, graph, node, os) values
			('%s', '%s', '%s', '%s')""" % 
			(app_name, graph, node, osname))

		# Add this appliance name the appliance category
		#
		self.db.execute("""INSERT INTO catindex(name,category) 
			VALUES('%s',mapCategory('appliance')) """ % app_name)

		if not node:
			kickstartable = False
		else:
			kickstartable = True

		self.command('add.appliance.attr', [ app_name, 'kickstartable',
			self.bool2str(kickstartable) ])
		
		if kickstartable:
			next_server = None

			try:
				# this command is called at an early stage while populating the
				# database and there are not host defined so getHostAttr would fail
				for a in self.db.database.getCategoryAttrs('global', 'global'):
					if a.attr == 'Kickstart_PrivateKickstartHost':
						next_server = a.value
			except:
				self.abort("Unable to find Kickstart_PrivateKickstartHost attributes")

			if next_server:
				self.command('add.appliance.attr', [app_name,
					'dhcp_nextserver', next_server])

				self.command('add.appliance.attr', [app_name,
					'dhcp_filename',
					'pxelinux.0' ])

		# add a row to the memberships table

		self.db.execute("""insert into memberships
			(name, appliance, distribution, public)
			values
			('%s',
			(select id from appliances where name='%s'), 
			(select id from distributions where name='%s'),
			'%s')""" %
			(mem_name, app_name, rocks_distribution, public))
