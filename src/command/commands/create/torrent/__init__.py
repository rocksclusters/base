# $Id: __init__.py,v 1.10 2008/03/06 23:41:36 mjk Exp $
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
# Revision 1.10  2008/03/06 23:41:36  mjk
# copyright storm on
#
# Revision 1.9  2007/07/04 01:47:37  mjk
# embrace the anger
#
# Revision 1.8  2007/07/02 18:35:24  bruno
# create cleanup
#
# Revision 1.7  2007/06/23 03:54:52  mjk
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
# Revision 1.5  2007/06/07 21:23:04  mjk
# - command derive from verb.command class
# - default is MustBeRoot
# - list.command / dump.command set MustBeRoot = 0
# - removed plugin non-bugfix
#
# Revision 1.4  2007/05/11 21:18:24  bruno
# in the new style of the katz
#
# Revision 1.3  2007/05/10 20:37:01  mjk
# - massive rocks-command changes
# -- list host is standardized
# -- usage simpler
# -- help is the docstring
# -- host groups and select statements
# - added viz commands
#
# Revision 1.2  2007/02/27 01:53:58  mjk
# - run(self, args) => run(self, flags, args)
# - replaced rocks list host xml with more complete code
# - replaced rocks lust node xml with kpp shell (not a command now)
#
# Revision 1.1  2006/12/19 20:40:26  bruno
# the new hotness in torrent creation
#
#

import os
import stat
import time
import sys
import string
import BitTorrent.bencode
import rocks.file
import rocks.commands



class Command(rocks.commands.create.command):
	"""
	Create a torrent file for a regular file. This command is heavily used
	by rocks-dist in order to prepare the RPMS for the Avalanche Installer.

	<arg type='string' name='path'>
	The pathname of the file or directory requiring torrent files.
	</arg>

	<param type='string' name='time'>
	The timestamp to be encoded within the torrent. If none is provided
	the current time is used.
	</param>

	<example cmd='create torrent kernel-2.6.9-42.0.2.EL.i686.rpm'>
	Generates a torrent file named kernel-2.6.9-42.0.2.EL.i686.rpm.torrent
	in the current directory.
	</example>
	
	<example cmd='create torrent rocks-dist/lan/i386/RedHat/RPMS'>
	Generates torrent files for every file in the RPMS directory.
	</example>
	"""

	def maketorrent(self, filename, data):
		info = {}
		info['length'] =  os.stat(filename)[stat.ST_SIZE]
		info['name'] =  os.path.basename(filename)

		data['info'] = info

		encoded = BitTorrent.bencode.bencode(data)
		
		file = open('%s.torrent' % (filename), 'w')
		file.write(encoded)
		file.close()


	def run(self, params, args):
		
		if len(args) != 1:
			self.abort('must supply one file')
		filename = args[0]

		(timestamp, ) = self.fillParams([('timestamp', time.time())])		
		try:
			creation_date = int(timestamp)
		except:
			creation_date = int(time.time())
			
		data = {}

		#
		# announce string
		#
		localhost = self.db.getGlobalVar('Kickstart', 'PrivateAddress')
		data['announce'] = 'http://%s:7625/announce' % (localhost)

		data['creation date'] = creation_date

		#
		# if this is a directory, then build a torrent file for
		# each file under this directory
		#
		if os.path.isdir(filename):
			tree = rocks.file.Tree(filename)
			for dir in tree.getDirs():
				for file in tree.getFiles(dir):
					self.maketorrent(file.getFullName(),
						data)
		else:
			self.maketorrent(filename, data)

