# $Id: __init__.py,v 1.16 2009/03/13 17:32:21 bruno Exp $
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
# Revision 1.16  2009/03/13 17:32:21  bruno
# nuked 'comment'
#
# Revision 1.15  2009/01/14 00:20:56  bruno
# unify the physical node and VM node boot action functionality
#
# - all bootaction's are global
#
# - the node table has a 'runaction' (what bootaction should the node do when
#   a node normally boots) and an 'installaction (the bootaction for installs).
#
# - the 'boot' table has an entry for each node and it dictates what the node
#   will do on the next boot -- it will look up the runaction in the nodes table
#   (for a normal boot) or the installaction in the nodes table (for an install).
#
# Revision 1.14  2008/10/18 00:55:49  mjk
# copyright 5.1
#
# Revision 1.13  2008/03/06 23:41:37  mjk
# copyright storm on
#
# Revision 1.12  2007/08/14 18:50:09  bruno
# set and list comment field for hosts
#
# Revision 1.11  2007/07/04 01:47:38  mjk
# embrace the anger
#
# Revision 1.10  2007/06/28 20:26:25  bruno
# done with 'rocks list'
#
# Revision 1.9  2007/06/28 19:45:44  bruno
# all the 'rocks list host' commands now have help
#
# Revision 1.8  2007/06/19 16:42:41  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.7  2007/06/08 03:26:24  mjk
# - plugins call self.owner.addText()
# - non-existant bug was real, fix plugin graph stuff
# - add set host cpus|membership|rack|rank
# - add list host (not /etc/hosts, rather the nodes table)
# - fix --- padding for only None fields not 0 fields
# - list host interfaces is cool works for incomplete hosts
#
# Revision 1.6  2007/06/07 21:23:04  mjk
# - command derive from verb.command class
# - default is MustBeRoot
# - list.command / dump.command set MustBeRoot = 0
# - removed plugin non-bugfix
#
# Revision 1.5  2007/06/07 16:43:02  mjk
# - moved host(s) argument processing into a top level class
# - list/dump/set host commands now use this
#
# Revision 1.4  2007/06/07 16:19:10  mjk
# - add "rocks add host"
# - add "rocks dump host"
# - add "rocks dump host interface"
# - remove "rocks add host new"
# - add mysql db init script to foundation-mysql
# - more flexible hostname lookup for the command line
#
# Revision 1.3  2007/05/11 18:33:15  mjk
# - fix list host profiles
# - [hosts] -> [host(s)]
#
# Revision 1.2  2007/05/10 20:37:01  mjk
# - massive rocks-command changes
# -- list host is standardized
# -- usage simpler
# -- help is the docstring
# -- host groups and select statements
# - added viz commands
#

import rocks.commands

class command(rocks.commands.HostArgumentProcessor,
	rocks.commands.list.command):
	pass
	
class Command(command):
	"""
	List the membership, CPU count and physical position info for
	a list of hosts.

	<arg optional='1' type='string' name='host' repeat='1'>
	Zero, one or more host names. If no host names are supplied, info about
	all the known hosts is listed.
	</arg>
	
	<example cmd='list host compute-0-0'>
	List info for compute-0-0.
	</example>

	<example cmd='list host'>
	List info for all known hosts.
	</example>
	"""

	def run(self, params, args):
		self.beginOutput()

		for host in self.getHostnames(args):
			self.db.execute("""select m.name, n.cpus,
				n.rack, n.rank, n.runaction, n.installaction
				from nodes n, memberships m where 
				n.membership=m.id and n.name='%s'""" % host)
			self.addOutput(host, self.db.fetchone())
			
		self.endOutput(header=['host', 'membership', 'cpus', 'rack',
			'rank', 'runaction', 'installaction'])
		
