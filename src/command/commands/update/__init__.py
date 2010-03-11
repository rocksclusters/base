# $Id: __init__.py,v 1.1 2010/03/11 03:11:11 mjk Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
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
# Revision 1.1  2010/03/11 03:11:11  mjk
# added 'rocks update' command (just for rocks packages, not os)
#

import string
import os
import rocks.commands

class command(rocks.commands.Command):
	MustBeRoot = 1

	
class Command(command):
	"""
	Download and install updated packages and Rolls from Rocks.  This
	does not include any OS packages.
	
	This does not rebuild the distribution or update the backend nodes.
	
	<example cmd='update'>
	Updates the Frotend.
	</example>
	"""
	
	def run(self, params, args):
		if len(args):
			self.abort('command does not take arguments')

		ver	= self.db.getHostAttr('localhost', 'rocks_version')
		url	= self.db.getHostAttr('localhost', 'updates_url')
		path	= self.db.getHostAttr('localhost', 'updates_path')
		
		if not ver:
			self.abort('unknown rocks version')

		if not url:
			url  = 'http://www.rocksclusters.org/'
			url += 'ftp-site/pub/rocks/rocks-%s/%s/updates/' % \
				(ver, self.os)

		if not path:
			path = '/export/rocks/updates'

		try:
			host = url.split('//', 1)[1].split('/')[0]
		except:
			self.abort('invalid url')

		if not os.path.exists(path):
			os.system('mkdir -p %s' % path)

		os.chdir(path)
		self.command('create.mirror', [ url, 'rollname=rocks-updates' ])
		os.system('createrepo %s' % host)

		# Always re-write the rocks-updates.repo yum file

		repo = '/etc/yum.repos.d/rocks-updates.repo'
		file = open(repo, 'w')
		file.write('[Rocks-%s-Updates]\n' % ver)
		file.write('name=Rocks %s Updates\n' % ver)
		file.write('baseurl=file://%s/%s\n' % (path, host))
		file.close()

		# Add the updates roll and enable it, but do not rebuild the
		# distribution.  The user should do this when they are ready.

		self.command('add.roll', [
			'rocks-updates-%s-0.%s.disk1.iso' % (ver, self.arch),
			'clean=yes'
			])
		self.command('enable.roll', [
			'rocks-updates',
			'arch=%s' % self.arch,
			'version=%s' % ver
			])

		# Update the packages on the frontend, but only from this new
		# YUM repository.

		os.system('yum --disablerepo="*" '
			'--enablerepo=Rocks-%s-Updates update' % ver)

		# Scan the updates for any .sh files and run these to update
		# the Frontend after the RPMs are installed.
		dir = url.split('//', 1)[1]
		for file in os.listdir(dir):
			if os.path.splitext(file)[1] != '.sh':
				continue
			os.system('sh -x %s' % os.path.join(dir, file))
