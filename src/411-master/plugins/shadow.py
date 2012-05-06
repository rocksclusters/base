# $Id: shadow.py,v 1.7 2012/05/06 05:48:16 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.5 (Mamba)
# 		         version 6.0 (Mamba)
# 
# Copyright (c) 2000 - 2012 The Regents of the University of California.
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
# $Log: shadow.py,v $
# Revision 1.7  2012/05/06 05:48:16  phil
# Copyright Storm for Mamba
#
# Revision 1.6  2011/07/23 02:30:23  phil
# Viper Copyright
#
# Revision 1.5  2011/06/17 05:46:32  anoop
# -Bug fixes to passwd and shadow filters.
# -The filters now correctly add and remove
#  users with UID > 500 who are not system
#  users.
#
# Revision 1.4  2011/06/16 22:47:27  anoop
# Bug fixes. Remove empty lines and malformed lines while processing
#
# Revision 1.3  2011/05/11 19:29:16  anoop
# Bug fix. Make sure even new entries get propogated
#
# Revision 1.2  2011/04/27 00:03:39  anoop
# Minor improvements to the way shadow entries are transmitted.
#
# Revision 1.1  2011/04/26 23:24:04  anoop
# Added shadow file plugin to only transfer shadow information
# for users over UID 500
#

import os
import sys
import string
import re
import rocks
import rocks.service411

class Plugin(rocks.service411.Plugin):

	def get_filename(self):
		return '/etc/shadow'

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

	def get_uid_map(self):
		# Get a list of all usernames in passwd file
		# that are over UID 500
		f = open('/etc/passwd', 'r')
		lp = f.readlines()
		f.close()
		
		p_lam = lambda(x): len(x.split(':')) == 7
		lp = filter(p_lam, lp)

		# Get only usernames, and UIDs out of list
		s = lambda(x):	\
			(x.split(':')[0].strip(),x.split(':')[2].strip())
		passwd_map = map(s, lp)
		return passwd_map

	def pre_send(self, content):
		
		content = content.rstrip('\n')
		content_lines = content.split('\n')

		# Create a dictionary of the shadow file
		# with all usernames as keys
		shadow_lam = self.get_shadow_lambda()
		shadow_dict = dict(map(shadow_lam, content_lines))

		lp = self.get_uid_map()

		# Filter out all shadow entries for
		# users with UID < 500
		p = lambda(x): ( int(x[1]) >= 500 and \
			not x[0] in self.avoid_uname())
		lp = filter(p, lp)
		u_names = map((lambda(x): x[0]), lp)

		filtered_content = []
		for key in shadow_dict:
			if key in u_names:
				filtered_content.append(shadow_dict[key])

		return  string.join(filtered_content, '\n')

	@staticmethod
	def get_shadow_lambda():
		return lambda(x): \
			(x.split(':')[0].strip(), x.strip())

	def filter_content(self, content):

		content = content.rstrip('\n')
		content_lines = content.split('\n')

		# Remove empty and malformed lines in input
		f_malformed= lambda(x): (len(x.split(':')) == 9)
		content_lines = filter(f_malformed, content_lines)

		# Open shadow file.
		f = open('/etc/shadow', 'r')
		ls = f.readlines()
		f.close()
		# Ignore blank/malformed lines
		ls = filter(f_malformed, ls)

		# This lambda function returns a tuple
		# of the form (username, user_entry_in_shadow)
		shadow_lam = self.get_shadow_lambda()

		# Get a list of tuples from /etc/shadow
		shadow = map(shadow_lam, ls)

		lp = self.get_uid_map()

		# Filter out all shadow entries for
		# users with UID < 500
		#p = lambda(x): ( int(x[1]) >= 500 and \
		#	not x[0] in self.avoid_uname())
		#lp = filter(p, lp)
		u_names = map((lambda(x): x[0]), lp)
	
		# The received list of shadow entries are also
		# subject to the lambda filter, and then a dictionary
		# is created from the list of tuples. This will help
		# us filter the content easily
		recv_shadow_dict = dict(map(shadow_lam, content_lines))

		new_shadow = []

		# Merge existing entries in original shadow file
		# with existing entries in received content
		for entry in shadow:
			u = entry[0]
			e = entry[1]
			# If we don't find the username in the password
			# file, remove from shadow as well
			if not u in u_names:
				continue
			else:
				if u in recv_shadow_dict.keys():
					new_shadow.append(recv_shadow_dict.pop(u))
				else:
					new_shadow.append(e)

		for s in recv_shadow_dict:
			new_shadow.append(recv_shadow_dict[s])
			
		return string.join(new_shadow, '\n') + '\n'
