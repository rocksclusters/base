# $Id: __init__.py,v 1.1 2008/12/15 22:27:21 bruno Exp $
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
# Revision 1.1  2008/12/15 22:27:21  bruno
# convert pxeboot and pxeaction tables to boot and bootaction tables.
#
# this enables merging the pxeaction and vm_profiles tables
#
#

import sys
import string
import rocks.commands
import os

class Command(rocks.commands.HostArgumentProcessor,
	rocks.commands.add.command):
	"""
	Add a bootaction specification for a host.
	
	<arg type='string' name='host' repeat='1' optional='1'>
	List of hosts to add bootaction definitions. If no hosts are listed,
	then the global definition for 'action=name' is added.
	</arg>

	<param type='string' name='action'>
	Label name for the bootaction. You can see the bootaction label names by
	executing: 'rocks list host bootaction [host(s)]'.
	</param>
	
	<param type='string' name='kernel'>
	The name of the kernel that is associated with this boot action.
	</param>

	<param type='string' name='ramdisk'>
	The name of the ramdisk that is associated with this boot action.
	</param>
	
	<param type='string' name='args'>
	The second line for a pxelinux definition (e.g., ks ramdisk_size=150000
	lang= devfs=nomount pxe kssendmac selinux=0)
	</param>
	
	<example cmd='add host bootaction action=os kernel="localboot 0"'>
	Add the global 'os' bootaction.
	</example>
	
	<example cmd='add host bootaction compute-0-0 action=memtest command="memtest"'>
	Add the 'memtest' bootaction for compute-0-0
	</example>
	"""

	def addBootAction(self, nodeid, host, action, kernel, ramdisk,
		bootargs):

		#
		# is there already an entry in the pxeaction table
		#
		rows = self.db.execute("""select id from bootaction where
			node = %d and action = '%s'""" % (nodeid, action))
		if rows < 1:
			#
			# insert a new row
			#
			cols = {}
			cols['node'] = '%s' %  (nodeid)
			cols['action'] = '"%s"' % (action)

			if kernel != None:
				cols['kernel'] = '"%s"' % (kernel)
			if ramdisk != None:
				cols['ramdisk'] = '"%s"' % (ramdisk)
			if bootargs != None:
				cols['args'] = '"%s"' % (bootargs)

			self.db.execute('insert into bootaction '
				'(%s) ' % (string.join(cols.keys(), ',')) + \
				'values '
				'(%s) ' % (string.join(cols.values(), ',')))
		else:
			#
			# update the existing row
			#
			bootactionid, = self.db.fetchone()

			query = 'update bootaction set action = "%s" ' \
				% (action)

			if kernel != None:
				query += ', kernel = "%s" ' % (kernel) 
			if ramdisk != None:
				query += ', ramdisk = "%s" ' % (ramdisk) 
			if bootargs != None:
				query += ', args = "%s" ' % (bootargs)

			query += 'where id = %s' % (bootactionid)

			self.db.execute(query)

		return


	def run(self, params, args):
		if len(args) == 0:
			hosts = []
		else:
			hosts = self.getHostnames(args)

		(action, kernel, ramdisk, bootargs) = self.fillParams(
			[('action', ), 
			('kernel', ),
			('ramdisk', ),
			('args', )])
			
		if not action:
			self.abort('must supply an action')

		if not hosts:
			#
			# set the global (all nodes) configuration
			#
			self.addBootAction(0, 'global', action, kernel,
				ramdisk, bootargs)

			#	
			# regenerate all the pxe boot configuration files
			# including the default
			#
			self.command('set.host.boot', self.getHostnames())
			
		else:
			for host in hosts:
				#
				# get the node from the nodes table
				#
				self.db.execute("""select id from nodes where
					name = '%s'""" % (host))
				hostid, = self.db.fetchone()

				self.addBootAction(hostid, host, action, kernel,
					ramdisk, bootargs)
					
				#
				# regenerate the pxe boot configuration
				# file for host
				#
				self.command('set.host.boot', [ host ])

