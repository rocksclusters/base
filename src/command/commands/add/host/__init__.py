# $Id: __init__.py,v 1.20 2011/05/24 05:26:54 phil Exp $
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
# Revision 1.20  2011/05/24 05:26:54  phil
# Ugly query to map membership back to appliance.
#
# Revision 1.19  2011/05/24 00:31:29  phil
# add host to 'host' category. Install standard category selections of
# (global,os,appliance,host) for a host
#
# Revision 1.18  2011/03/04 01:57:23  anoop
# when rocks add host is run by hand, we need to set the
# os attribute explicitly.
#
# Revision 1.17  2010/09/07 23:52:50  bruno
# star power for gb
#
# Revision 1.16  2009/05/01 19:06:55  mjk
# chimi con queso
#
# Revision 1.15  2009/03/21 22:22:55  bruno
#  - lights-out install of VM frontends with new node_rolls table
#  - nuked 'site' columns and tables from database
#  - worked through some bugs regarding entities
#
# Revision 1.14  2009/03/13 18:45:58  mjk
# - rocks add host route works
# - added rocks.add.host.command class
# - getHostAttrs|Routes uses getHostname to normalize the host arg
# - fixed getHostRoutes
#
# Revision 1.13  2008/10/18 00:55:48  mjk
# copyright 5.1
#
# Revision 1.12  2008/09/15 20:08:46  bruno
# associate an operating system with a hostname.
#
# Revision 1.11  2008/08/28 20:41:16  bruno
# spelling in help fix
#
# Revision 1.10  2008/03/06 23:41:35  mjk
# copyright storm on
#
# Revision 1.9  2007/07/04 01:47:37  mjk
# embrace the anger
#
# Revision 1.8  2007/07/02 19:43:58  bruno
# more params/flags cleanup
#
# Revision 1.7  2007/06/23 03:54:51  mjk
# - first pass at consistency
# - still needs some docstrings
# - argument processors take SQL wildcards
# - add cannot run twice (must use set)
# - dump does sets not just adds
#
# Revision 1.6  2007/06/19 16:42:40  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.5  2007/06/16 02:39:50  mjk
# - added list roll commands (used for docbook)
# - docstrings should now be XML
# - added parser for docstring to ASCII or DocBook
# - ditched Phil's Network regex stuff (will come back later)
# - updated several docstrings
#
# Revision 1.4  2007/06/08 03:26:24  mjk
# - plugins call self.owner.addText()
# - non-existant bug was real, fix plugin graph stuff
# - add set host cpus|membership|rack|rank
# - add list host (not /etc/hosts, rather the nodes table)
# - fix --- padding for only None fields not 0 fields
# - list host interfaces is cool works for incomplete hosts
#
# Revision 1.3  2007/06/07 21:23:03  mjk
# - command derive from verb.command class
# - default is MustBeRoot
# - list.command / dump.command set MustBeRoot = 0
# - removed plugin non-bugfix
#
# Revision 1.2  2007/06/07 16:19:10  mjk
# - add "rocks add host"
# - add "rocks dump host"
# - add "rocks dump host interface"
# - remove "rocks add host new"
# - add mysql db init script to foundation-mysql
# - more flexible hostname lookup for the command line
#
# Revision 1.1  2007/05/30 20:12:36  anoop
# Command to add a new node to the database. Updates the node table
#

import os
import sys
import string
import rocks.commands

class command(rocks.commands.HostArgumentProcessor, rocks.commands.add.command):
	pass
	
class Command(command):
	"""
	Add an new host to the cluster.

        <arg type='string' name='host'>
        A single host name.  If the hostname is of the standard form of
	basename-rack-rank the default values for the membership, rack,
	and rank parameters are taken from the hostname.
        </arg>

        <param type='int' name='cpus'>
        Number of CPUs (cores) in the given host.  If not provided the
	default of 1 CPU is inserted into the database.
        </param>

	<param type='string' name='membership'>
	Appliance membership name.  If not provided and the host name is of
	the standard form the membership is taken from the basename of 
	the host.
	</param>

        <param type='int' name='rack'>
        The number of the rack where the machine is located. The convention
	in Rocks is to start numbering at 0. If not provided and the host
	name is of the standard form the rack number is taken from the host
	name.
        </param>

	<param type='int' name='rank'>
	The position of the machine in the rack. The convention in Rocks
	is to number from the bottom of the rack to the top starting at 0.
	If not provided and the host name is of the standard form the rank
	number is taken from the host name.
	</param>

	<param type='string' name='os'>
	The operating system name. The default is: linux.
	</param>

	<example cmd='add host compute-0-1'>
	Adds the host "compute-0-0" to the database with 1 CPU, a membership
	name of "compute", a rack number of 0, and rank of 1.
	</example>

	<example cmd='add host frontend rack=0 rank=0 membership=Frontend'>
	Adds the host "frontend" to the database with 1 CPU, a membership name
	of "Frontend", a rack number of 0, and rank of 1.
	</example>

	<related>add host interface</related>

	"""

	def run(self, params, args):
	
		if len(args) != 1:
			self.abort('must supply one host')
		host = args[0]
		
		if host in self.getHostnames():
			self.abort('host "%s" exists' % host)
			
		# If the name is of the form appliancename-rack-rank
		# then do the right thing and figure out the default
		# values for membership, rack, and rank.  If the appliance 
		# name is not found in the database, or the rack/rank numbers
		# are invalid do not guess any defaults.  The name is
		# either 100% used or 0% used.
		
		try:
			basename, rack, rank = host.split('-')
			self.db.execute("""select m.name from 
				appliances a, memberships m where
				a.name="%s" and m.appliance=a.id""" % basename)
			membership, = self.db.fetchone()
			rack = int(rack)
			rank = int(rank)
		except:
			membership = None
			rack = None
			rank = None
			
		# fillParams with the above default values
		
		(membership, numCPUs, rack, rank, osname) = self.fillParams(
			[('membership', membership),
			('cpus', 1),
			('rack', rack),
			('rank', rank),
			('os', None) ])

		if not membership:
			self.abort('membership not specified')
		if rack == None:
			self.abort('rack not specified')
		if rank == None:
			self.abort('rank not specified')

		self.db.execute("""select a.os from appliances a,
			memberships m where m.appliance = a.id and
			m.name='%s'""" % (membership))
		supported_os = list(self.db.fetchone()[0])

		if osname is not None and osname not in supported_os:
			self.abort("%s does not support %s" % (membership,
				osname))

		if osname is None:
			if len(supported_os) == 1:
				osname = supported_os[0]
			else:
				osname = 'linux'

		self.db.execute("""insert into nodes
			(name, membership, cpus, rack, rank, os)
			values ('%s',
			(select id from memberships where name='%s'),
			'%d', '%d', '%d', '%s')""" % (host, membership,
			int(numCPUs), int(rack), int(rank), osname))

		#
		# add this host into the host categories
		# Mirrors the host table entries, for 5.4.3.
		#
		self.db.execute("""INSERT INTO catindex(Name,Category)
			VALUES('%s',mapCategory('host'))""" % host

		# And then make the Default category selections for this host
		self.db.execute("""INSERT INTO hostselections(Host,
			Category, Selection) VALUES (
			mapCategoryIndex('host','%s'), mapCategory('global'),
			mapCategoryIndex('global','global')) """ % host
		self.db.execute("""INSERT INTO hostselections(Host,
			Category, Selection) VALUES (
			mapCategoryIndex('host','%s'), mapCategory('os'),
			mapCategoryIndex('os','%s')) """ % (host,osname))
		self.db.execute("""INSERT INTO hostselections(Host,
			Category, Selection) VALUES (
			mapCategoryIndex('host','%s'), mapCategory('appliance'),
			mapCategoryIndex('appliance',
			(SELECT a.name FROM memberships m JOIN appliances a ON m.appliance=a.id AND m.name='%s'))""" 
				% (host,membership))
		self.db.execute("""INSERT INTO hostselections(Host,
			Category, Selection) VALUES (
			mapCategoryIndex('host','%s'), mapCategory('host'),
			mapCategoryIndex('host','%s'))""" % (host,host)

		#
		#
		# Set the value of the OS in the host attributes table
		db_cmd = ('insert into node_attributes '
			'(node, attr, value) '
			'values ((select id from nodes where name="%s"), '
			'"%s","%s")' % (host, 'os', osname))
		self.db.execute(db_cmd)
