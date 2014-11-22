# $Id: __init__.py,v 1.16 2012/11/27 00:48:09 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
# 
# Copyright (c) 2000 - 2014 The Regents of the University of California.
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
# Revision 1.16  2012/11/27 00:48:09  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.15  2012/05/06 05:48:19  phil
# Copyright Storm for Mamba
#
# Revision 1.14  2011/07/23 02:30:24  phil
# Viper Copyright
#
# Revision 1.13  2010/09/07 23:52:50  bruno
# star power for gb
#
# Revision 1.12  2009/05/01 19:06:54  mjk
# chimi con queso
#
# Revision 1.11  2008/10/18 00:55:48  mjk
# copyright 5.1
#
# Revision 1.10  2008/03/06 23:41:34  mjk
# copyright storm on
#
# Revision 1.9  2007/07/04 01:47:37  mjk
# embrace the anger
#
# Revision 1.8  2007/06/27 21:30:34  bruno
# cleanup distribution commands
#
# Revision 1.7  2007/06/25 21:26:03  bruno
# correct row count processing
#
# Revision 1.6  2007/06/23 03:54:51  mjk
# - first pass at consistency
# - still needs some docstrings
# - argument processors take SQL wildcards
# - add cannot run twice (must use set)
# - dump does sets not just adds
#
# Revision 1.5  2007/06/19 16:42:40  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.4  2007/06/07 21:23:03  mjk
# - command derive from verb.command class
# - default is MustBeRoot
# - list.command / dump.command set MustBeRoot = 0
# - removed plugin non-bugfix
#
# Revision 1.3  2007/05/30 19:45:43  bruno
# cleaned up the 'rocks * distribution' commands
#
# Revision 1.2  2007/05/10 20:37:00  mjk
# - massive rocks-command changes
# -- list host is standardized
# -- usage simpler
# -- help is the docstring
# -- host groups and select statements
# - added viz commands
#
# Revision 1.1  2007/04/11 19:33:01  bruno
# live from the pub: add-distribution has been converted to the rocks
# command line
#

import rocks.commands

class Command(rocks.commands.DistributionArgumentProcessor,
	rocks.commands.add.command):
	"""
	Add a distribution specification to the database.

	<arg type='string' name='distribution'>
	Name of the new distribution.
	</arg>
	
	<example cmd='add distribution rocks-dist'>
	Adds the distribution named "rocks-dist" into the database.
	</example>
	"""

	def run(self, params, args):
	
		if len(args) != 1:
			self.abort('must supply one distribution')
		dist = args[0]
		
		if dist in self.getDistributionNames():
			self.abort('distribution "%s" exists' % dist)

		self.db.execute("""insert into distributions (name) values 
			('%s')""" % dist)



RollName = "base"
