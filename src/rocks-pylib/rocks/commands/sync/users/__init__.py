# $Id: __init__.py,v 1.19 2012/11/27 00:48:31 phil Exp $
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
# Revision 1.19  2012/11/27 00:48:31  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.18  2012/05/06 05:48:38  phil
# Copyright Storm for Mamba
#
# Revision 1.17  2011/07/23 02:30:41  phil
# Viper Copyright
#
# Revision 1.16  2010/09/07 23:53:03  bruno
# star power for gb
#
# Revision 1.15  2009/05/01 19:07:04  mjk
# chimi con queso
#
# Revision 1.14  2008/10/18 00:55:58  mjk
# copyright 5.1
#
# Revision 1.13  2008/03/06 23:41:40  mjk
# copyright storm on
#
# Revision 1.12  2007/07/04 01:47:40  mjk
# embrace the anger
#
# Revision 1.11  2007/07/02 18:41:01  bruno
# added 'rocks sync config' (insert-ethers --update) and more sync cleanup
#
# Revision 1.10  2007/07/02 17:38:51  bruno
# cleanup the help and make sure the 411 files are 'force' updated and that
# autofs is restarted on all known hosts.
#
# Revision 1.9  2007/06/19 16:42:43  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.8  2007/06/08 03:26:25  mjk
# - plugins call self.owner.addText()
# - non-existant bug was real, fix plugin graph stuff
# - add set host cpus|membership|rack|rank
# - add list host (not /etc/hosts, rather the nodes table)
# - fix --- padding for only None fields not 0 fields
# - list host interfaces is cool works for incomplete hosts
#
# Revision 1.7  2007/06/07 21:23:05  mjk
# - command derive from verb.command class
# - default is MustBeRoot
# - list.command / dump.command set MustBeRoot = 0
# - removed plugin non-bugfix
#
# Revision 1.6  2007/06/07 00:03:22  bruno
# build hpl against openmpi from RHEL, not from us
#
# Revision 1.5  2007/05/31 19:35:43  bruno
# first pass at getting all the 'help' consistent on all the rocks commands
#
# Revision 1.4  2007/05/10 20:37:02  mjk
# - massive rocks-command changes
# -- list host is standardized
# -- usage simpler
# -- help is the docstring
# -- host groups and select statements
# - added viz commands
#
# Revision 1.3  2007/02/27 01:53:58  mjk
# - run(self, args) => run(self, flags, args)
# - replaced rocks list host xml with more complete code
# - replaced rocks lust node xml with kpp shell (not a command now)
#
# Revision 1.2  2007/02/08 17:31:25  mjk
# Added root check for root-only commands
# Added syslog tracking to record changes to the cluster
#
# Revision 1.1  2007/02/05 23:29:19  mjk
# added 'rocks add roll'
# added plugin_* facility
# added 'rocks sync user' (plugin-able)
#

import rocks.commands


class Command(rocks.commands.sync.command):
	"""
	Update all user-related files (e.g., /etc/passwd, /etc/shadow, etc.)
	on all known hosts. Also, restart autofs on all known hosts.

	<example cmd='sync users'>
	Send all user info to all known hosts.
	</example>
	"""

	def run(self, params, args):
		self.runPlugins()


RollName = "base"
