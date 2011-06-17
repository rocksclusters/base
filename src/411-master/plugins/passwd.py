# $Id: passwd.py,v 1.12 2011/06/17 05:46:32 anoop Exp $

# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4 (Maverick)
# 
# Copyright (c) 2000 - 2010 The Regents of the University of California.
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
# Revision 1.12  2011/06/17 05:46:32  anoop
# -Bug fixes to passwd and shadow filters.
# -The filters now correctly add and remove
#  users with UID > 500 who are not system
#  users.
#
# Revision 1.11  2011/06/16 22:47:27  anoop
# Bug fixes. Remove empty lines and malformed lines while processing
#
# Revision 1.10  2011/06/13 20:10:26  anoop
# Ignore blank lines
#
# Revision 1.9  2011/05/11 19:29:16  anoop
# Bug fix. Make sure even new entries get propogated
#
# Revision 1.8  2011/04/27 00:20:52  anoop
# Transfer only password entries which are greater than UID 500
# Also merge entries into the password file rather than overwriting them
# Merge entries so that only users with UID > 500 are overwritten.
#
# Revision 1.7  2011/04/26 23:23:27  anoop
# Minor modification to 411put. Use a get_filename function instead of
# a filename constant.
#
# Revision 1.6  2011/04/21 17:28:20  anoop
# 411 plugins now take advantage of attributes
#
# Revision 1.5  2010/09/07 23:52:48  bruno
# star power for gb
#
# Revision 1.4  2009/05/01 19:06:50  mjk
# chimi con queso
#
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
import string

class Plugin(rocks.service411.Plugin):

	# THIS IS AN ABSOLUTE MUST FOR ALL PLUGINS. WITHOUT THIS,
	# PLUGINS WONT WORK
	def get_filename(self):
		return "/etc/passwd"

	@staticmethod
	def filter_malformed():
		return lambda(x): len(x.split(':')) == 7

	@staticmethod
	def passwd_lambda():
		return lambda(x): (x.split(':')[0].strip(), x)

	# List of usernames to avoid transferring
	# that may have UIDs greater than 500
	@staticmethod
	def avoid_uname():
		return [
			'nobody',
			'nobody4',
			'noaccess',
			'nfsnobody',
			]

	def pre_send(self, content):
		content = content.rstrip('\n')
		content_lines = content.split('\n')

		# Remove all malformed/empty lines
		lp = filter(self.filter_malformed(), content_lines)

		# Get a list of all usernames in passwd file
		# and keep only those whose UID >= 500
		lp = filter(self.uid_f, lp)

		return string.join(lp, '\n')

	# Function that returns true if UID >= 500
	def uid_f(self, x):
		l = x.split(':')
		if int(l[2]) < 500:
			return False
		if l[0] in self.avoid_uname():
			return False
		return True

	# Function to filter the content of the passwd file
	def filter_content(self, content):

		content = content.rstrip('\n')
		content_lines = content.split('\n')
		
		# Remove empty and malformed lines in input
		content_lines = filter(self.filter_malformed(), content_lines)

		# Merge entries from existing passwd file and
		# passwd file that we just downloaded.
		passwd_recv = dict(map(self.passwd_lambda(), content_lines))
		
		# Original Password file
		f = open('/etc/passwd', 'r')
		lp = map(string.strip, f.readlines())
		f.close()
		# Ignore blank/malformed lines
		lp = filter(self.filter_malformed(), lp)

		new_pw = []

		for line in lp:
			u_name = line.split(':')[0].strip()
			# If we're under 500, add the line
			if not self.uid_f(line):
				new_pw.append(line)
			# If we're over UID 500, and present
			# in the received passwd lines, then add
			else:
				if passwd_recv.has_key(u_name):
					new_pw.append(passwd_recv.pop(u_name))
				else:
					continue
		for pw in passwd_recv:
			new_pw.append(passwd_recv[pw])

		return string.join(new_pw, '\n') + '\n'
		
	def filter_owner(self, oid):
		if self.attrs['os'] == 'linux':
			return oid
		s = os.stat('/etc/passwd')
		import stat
		return '%d.%d' % (s[stat.ST_UID], s[stat.ST_GID])
