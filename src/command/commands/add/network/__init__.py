# $Id: __init__.py,v 1.8 2008/09/05 20:11:58 bruno Exp $
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
# $Log: __init__.py,v $
# Revision 1.8  2008/09/05 20:11:58  bruno
# get rid of sql warning messages when adding a network
#
# Revision 1.7  2008/03/06 23:41:35  mjk
# copyright storm on
#
# Revision 1.6  2007/07/05 17:46:45  bruno
# fixes
#
# Revision 1.5  2007/07/04 01:47:37  mjk
# embrace the anger
#
# Revision 1.4  2007/07/02 19:43:58  bruno
# more params/flags cleanup
#
# Revision 1.3  2007/06/23 03:54:51  mjk
# - first pass at consistency
# - still needs some docstrings
# - argument processors take SQL wildcards
# - add cannot run twice (must use set)
# - dump does sets not just adds
#
# Revision 1.2  2007/06/19 16:42:40  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.1  2007/06/12 01:10:41  mjk
# - 'rocks add subnet' is now 'rocks add network'
# - added set network subnet|netmask
# - added list network
# - other cleanup
#
# Revision 1.2  2007/06/07 21:23:03  mjk
# - command derive from verb.command class
# - default is MustBeRoot
# - list.command / dump.command set MustBeRoot = 0
# - removed plugin non-bugfix
#
# Revision 1.1  2007/05/30 20:10:53  anoop
# Added rocks add subnet - Command adds a subnet to the subnets table
# in the database. Is currently beta


import os
import sys
import types
import string
import rocks.commands

class Command(rocks.commands.add.command):
	"""
	Add a network to the database. By default both the "public" and
	"private" networks are already defined by Rocks.
		
	<arg type='string' name='name'>
	Name of the new network.
	</arg>
	
	<arg type='string' name='subnet'>
	The IP network address for the new network.
	</arg>

	<arg type='string' name='netmask'>
	The IP network mask for the new network.
	</arg>

	<param type='string' name='subnet'>
	Can be used in place of the subnet argument.
	</param>
	
	<param type='string' name='netmask'>
	Can be used in place of the netmask argument.
	</param>
	
	<example cmd='add network optiputer 192.168.1.0 255.255.255.0'>
	Adds the optiputer network address of 192.168.1.0/255.255.255.0.
	</example>

	<example cmd='add network optiputer subnet=192.168.1.0 netmask=255.255.255.0'>
	Same as above.
	</example>
	"""

        def run(self, params, args):
        	
        	(args, subnet, netmask) = self.fillPositionalArgs(
        		('subnet', 'netmask'))

        	if len(args) != 1:
        		self.abort('must supply one network')
        	name = args[0]

		if not subnet:
                        self.abort('subnet not specified')
		if not netmask:
                        self.abort('netmask not specified')

		# Insert the name of the new network into the subnets
		# table if it does not already exist
			
		rows = self.db.execute("""select * from subnets where 
			name='%s'""" % name)
		if rows > 0:
			self.abort('network "%s" exists' % name)
		
		self.db.execute("""insert into subnets (name, subnet, netmask)
			values ('%s', '%s', '%s')""" % (name, subnet, netmask))

