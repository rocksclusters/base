# $Id: plugin_fixnewusers.py,v 1.15 2012/11/27 00:48:31 phil Exp $
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
# $Log: plugin_fixnewusers.py,v $
# Revision 1.15  2012/11/27 00:48:31  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.14  2012/05/06 05:48:38  phil
# Copyright Storm for Mamba
#
# Revision 1.13  2012/04/26 21:21:46  phil
# default to nfsvers=3 for the time being. Can be overwritten
# with Info_HomeDirOptions
#
# Revision 1.12  2011/07/23 02:30:41  phil
# Viper Copyright
#
# Revision 1.11  2010/09/07 23:53:03  bruno
# star power for gb
#
# Revision 1.10  2009/05/01 19:07:04  mjk
# chimi con queso
#
# Revision 1.9  2009/03/04 21:31:44  bruno
# convert all getGlobalVar to getHostAttr
#
# Revision 1.8  2008/10/21 18:14:36  bruno
# add jon forrest's patch to easily incorporate file servers to serve user
# home directories
#
# Revision 1.7  2008/10/18 00:55:58  mjk
# copyright 5.1
#
# Revision 1.6  2008/03/06 23:41:40  mjk
# copyright storm on
#
# Revision 1.5  2007/06/19 16:42:43  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.4  2007/06/08 03:26:25  mjk
# - plugins call self.owner.addText()
# - non-existant bug was real, fix plugin graph stuff
# - add set host cpus|membership|rack|rank
# - add list host (not /etc/hosts, rather the nodes table)
# - fix --- padding for only None fields not 0 fields
# - list host interfaces is cool works for incomplete hosts
#
# Revision 1.3  2007/06/07 21:23:05  mjk
# - command derive from verb.command class
# - default is MustBeRoot
# - list.command / dump.command set MustBeRoot = 0
# - removed plugin non-bugfix
#
# Revision 1.2  2007/06/07 18:04:05  bruno
# in run() method, parameter needs to be 'args' not 'arg'
#
# Revision 1.1  2007/02/05 23:29:19  mjk
# added 'rocks add roll'
# added plugin_* facility
# added 'rocks sync user' (plugin-able)
#

import os
import string
import rocks.commands

class Plugin(rocks.commands.Plugin):
	"""Relocates home directories to location on file server and fixes autofs.home"""

	def provides(self):
		return 'fixnewusers'

	def run(self, args):
		# scan the password file for any '/export/home' entries
		# this is the default entry as setup by useradd
		new_users = []
		default_dir = '/export/home/'

		file = open('/etc/passwd', 'r')

		for line in file.readlines():
			l = string.split(line[:-1], ':')			

			if len(l) < 6:
				continue

			username = l[0]
			homedir = l[5]

			if homedir[:len(default_dir)] == default_dir:
				new_users.append(username)
		file.close()

		# if there is a file server specified in the database
		# use it. otherwise, use the default.
		hostname = self.db.getHostAttr('localhost', 'Info_HomeDirSrv')
		if not hostname:
			hostname = '%s.%s' % (self.db.getHostAttr(
				'localhost', 'Kickstart_PrivateHostname'),
				self.db.getHostAttr('localhost',
					'Kickstart_PrivateDNSDomain'))

		# if there is a home directory specified in the database
		# use it. otherwise, use the default.
		homedirloc = self.db.getHostAttr('localhost', 'Info_HomeDirLoc')
		if not homedirloc:
			homedirloc = '/export/home'
			
		# if there is a mount option specified in the database
		# use it. otherwise, use the default.
		options = self.db.getHostAttr('localhost', 'Info_HomeDirOptions')
		if not options:
			options="nfsvers=3"

		for user in new_users:

			# for each new user, change their default directory to
			# /home/<username>. this is always done whether or not
			# there are file server and home directory names in the
			# database.

			cmd = '/usr/sbin/usermod -d %s %s' % \
				(os.path.join('/home', user), user)
			for line in os.popen(cmd).readlines():
                        	self.owner.addText(line)

			# then update the auto.home file

			new_user_dir = os.path.join(homedirloc, user)
			autofs_entry = '%s\t-%s\t%s:%s' % \
				(user, options, hostname, new_user_dir)

			cmd = 'echo "%s" >> /etc/auto.home' % (autofs_entry)
			for line in os.popen(cmd).readlines():
                        	self.owner.addText(line)




