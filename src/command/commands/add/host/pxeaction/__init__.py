# $Id: __init__.py,v 1.13 2008/10/18 00:55:48 mjk Exp $
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
# $Log: __init__.py,v $
# Revision 1.13  2008/10/18 00:55:48  mjk
# copyright 5.1
#
# Revision 1.12  2008/07/11 19:59:41  bruno
# fix 'examples' in help section
#
# Revision 1.11  2008/03/06 23:41:35  mjk
# copyright storm on
#
# Revision 1.10  2008/01/22 17:27:21  bruno
# after removing a pxeaction, need to rebuild the pxe configuration files
#
# Revision 1.9  2007/12/10 21:28:34  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.8  2007/07/05 17:46:45  bruno
# fixes
#
# Revision 1.7  2007/07/04 01:47:37  mjk
# embrace the anger
#
# Revision 1.6  2007/06/29 21:22:05  bruno
# more cleanup
#
# Revision 1.5  2007/06/23 03:54:51  mjk
# - first pass at consistency
# - still needs some docstrings
# - argument processors take SQL wildcards
# - add cannot run twice (must use set)
# - dump does sets not just adds
#
# Revision 1.4  2007/06/19 16:42:40  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.3  2007/06/08 03:26:24  mjk
# - plugins call self.owner.addText()
# - non-existant bug was real, fix plugin graph stuff
# - add set host cpus|membership|rack|rank
# - add list host (not /etc/hosts, rather the nodes table)
# - fix --- padding for only None fields not 0 fields
# - list host interfaces is cool works for incomplete hosts
#
# Revision 1.2  2007/06/07 21:23:03  mjk
# - command derive from verb.command class
# - default is MustBeRoot
# - list.command / dump.command set MustBeRoot = 0
# - removed plugin non-bugfix
#
# Revision 1.1  2007/05/31 20:56:43  bruno
# moved pxeaction
#
# Revision 1.2  2007/05/10 20:37:02  mjk
# - massive rocks-command changes
# -- list host is standardized
# -- usage simpler
# -- help is the docstring
# -- host groups and select statements
# - added viz commands
#
# Revision 1.1  2007/05/02 20:20:53  bruno
# added 'pxeaction' table -- allows for adding and removing pxeboot actions
#
#

import sys
import string
import rocks.commands
import os

class Command(rocks.commands.HostArgumentProcessor,
	rocks.commands.add.command):
	"""
	Add a pxeaction specification for a host.
	
	<arg type='string' name='host' repeat='1' optional='1'>
	List of hosts to add pxeaction definitions. If no hosts are listed,
	then the global definition for 'action=name' is added.
	</arg>

	<param type='string' name='action'>
	Label name for the pxeaction. You can see the pxeaction label names by
	executing: 'rocks list host pxeaction [host(s)]'.
	</param>
	
	<param type='string' name='command'>
	The first line for a pxelinux definition (e.g., 'kernel vmlinuz' or
	'localboot 0').
	</param>
	
	<param type='string' name='args'>
	The second line for a pxelinux definition (e.g., append ks
	initrd=initrd.img ramdisk_size=150000 lang= devfs=nomount pxe
	kssendmac selinux=0)
	</param>
	
	<example cmd='add host pxeaction action=os command="localboot 0"'>
	Add the global 'os' pxeaction
	</example>
	
	<example cmd='add host pxeaction compute-0-0 action=memtest command="kernel memtest"'>
	Add the 'memtest' pxeaction for compute-0-0
	</example>
	"""

	def addPxeaction(self, nodeid, host, action, command, command_args):
		#
		# is there already an entry in the pxeaction table
		#
		rows = self.db.execute("""select id from pxeaction where
			node=%d and action='%s'""" % (nodeid, action))
		if rows < 1:
			#
			# insert a new row
			#
			cols = {}
			cols['node'] = '%s' %  (nodeid)
			cols['action'] = '"%s"' % (action)

			if command != None:
				cols['command'] = '"%s"' % (command)
			if command_args != None:
				cols['args'] = '"%s"' % (command_args)

			self.db.execute('insert into pxeaction '
				'(%s) ' % (string.join(cols.keys(), ',')) + \
				'values '
				'(%s) ' % (string.join(cols.values(), ',')))
		else:
			#
			# update the existing row
			#
			pxeactionid, = self.db.fetchone()

			query = 'update pxeaction set action = "%s" ' % (action)
			if command != None:
				query += ', command = "%s" ' % (command) 
			if command_args != None:
				query += ', args = "%s" ' % (command_args)

			query += 'where id = %s' % (pxeactionid)

			self.db.execute(query)

		return


	def run(self, params, args):
		if len(args) == 0:
			hosts = []
		else:
			hosts = self.getHostnames(args)

		(action, command, command_args) = self.fillParams(
			[('action', ), 
			('command', ),
			('args', )])
			
		if not action:
			self.abort('must supply an action')

		if not hosts:
			#
			# set the global (all nodes) configuration
			#
			self.addPxeaction(0, 'global', action, command,
				command_args)

			#	
			# regenerate all the pxe boot configuration files
			# including the default
			#
			self.command('set.host.pxeboot', self.getHostnames())
			
		else:
			for host in hosts:
				#
				# get the node from the nodes table
				#
				self.db.execute("""select id from nodes where
					name='%s'""" % (host))
				hostid, = self.db.fetchone()

				self.addPxeaction(hostid, host, action,
					command, command_args)
					
				#
				# regenerate the pxe boot configuration
				# file for host
				#
				self.command('set.host.pxeboot', [ host ])

