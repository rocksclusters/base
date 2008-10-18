# $Id: passwd.py,v 1.3 2008/10/18 00:55:47 mjk Exp $

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

# $Log: passwd.py,v $
# Revision 1.3  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.2  2008/08/12 23:20:13  anoop
# Added filter for auto.master
#
# Modified 411 transport to encode content of the file
# and filter before encrypting them. This helps with the
# problem of stripping whitespaces, and returns the content
# of the files exactly as they should be.
#
# Also modified the password and group filters just a little
# to make them return the correct whitespaces
#
# Revision 1.1  2008/08/09 19:27:51  anoop
# beginning of actual usable 411 plugins. For now password and group file
# plugins
#

import os
import sys
import rocks
import rocks.service411

class Plugin(rocks.service411.Plugin):

	# THIS IS AN ABSOLUTE MUST FOR ALL PLUGINS. WITHOUT THIS,
	# PLUGINS WONT WORK
	filename="/etc/passwd"

	# Function to filter the content of the passwd file
	def filter_content(self, content):

		# List of usernames to avoid, irrespective
		# of the UID
		avoid_uname = [
			'nobody',
			'nobody4',
			'noaccess',
			'nfsnobody',
			]

		# If the client is a linux box
		# just return the original content
		if self.os == 'linux':
			return content

		# If not, then start filtering
		content = content.rstrip('\n')
		content_lines = content.split('\n')

		# Get all users greater than 500
		# except for users.
		user_list = ''
		for line in content_lines:
			line = line.strip()
			entry = line.split(':')
			uid = int(entry[2])
			username = entry[0].strip()
			if uid >= 500 and \
				username not in avoid_uname:
				user_list = user_list + line + '\n'

		# Open the password file. and read 
		# it's contents, so that we can
		# maintain the UID's less than 500
		# Also maintain all usernames like
		# nobody, nobody4, etc for solaris
		f = open('/etc/passwd', 'r')
		passwd_lines = ''
		line = ''
		for line in f.readlines():
			line = line.strip()
			passwd_entry = line.split(':')
			uid = int(passwd_entry[2])
			username = passwd_entry[0].strip()
			if uid < 500 or username in avoid_uname:
				passwd_lines = passwd_lines + line + '\n'
		f.close()

		passwd_lines = passwd_lines + user_list

		return passwd_lines

	def filter_owner(self, oid):
		if self.os == 'linux':
			return oid
		s = os.stat('/etc/passwd')
		import stat
		return '%d.%d' % (s[stat.ST_UID], s[stat.ST_GID])
