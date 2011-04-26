# $Id: shadow.py,v 1.1 2011/04/26 23:24:04 anoop Exp $
#
# @Copyright@
# @Copyright@
#
# $Log: shadow.py,v $
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

	def pre_send(self, content):
		
		content = content.rstrip('\n')
		content_lines = content.split('\n')

		# Create a dictionary of the shadow file
		# with all usernames as keys
		shadow_lam = self.get_shadow_lambda()
		shadow_dict = dict(map(shadow_lam, content_lines))

		# Get a list of all usernames in passwd file
		# that are over UID 500
		f = open('/etc/passwd', 'r')
		lp = f.readlines()
		f.close()
		
		# Reduce lines to only those whose UID >= 500
		lp = filter(self.uid_f, lp)

		# Get only usernames out of list
		s = lambda(x):	\
			x.split(':')[0].strip()

		lp = map(s, lp)

		# Reduce shadow dictionary using only the
		# remaining entries in passwd lines
		filtered_content = []
		for key in shadow_dict:
			if key in lp:
				filtered_content.append(shadow_dict[key])

		return string.join(filtered_content, '\n') + '\n'

	# Function that returns true if UID >= 500
	@staticmethod
	def uid_f(x):
		l = x.split(':')
		if int(l[2]) >= 500:
			return True
		else:
			return False

	@staticmethod
	def get_shadow_lambda():
		return lambda(x): \
			(x.split(':')[0].strip(), x.strip())

	def filter_content(self, content):

		content = content.rstrip('\n')
		content_lines = content.split('\n')

		# Open shadow file.
		f = open('/etc/shadow', 'r')
		ls = f.readlines()
		f.close()

		# This lambda function returns a tuple
		# of the form (username, user_entry_in_shadow)
		shadow_lam = self.get_shadow_lambda()

		# Get a list of tuples from /etc/shadow
		shadow = map(shadow_lam, ls)

		# The received list of shadow entries are also
		# subject to the lambda filter, and then a dictionary
		# is created from the list of tuples. This will help
		# us filter the content easily
		recv_shadow_dict = dict(map(shadow_lam, content_lines))

		new_shadow = []
		for entry in shadow:
			u_name = entry[0]
			if recv_shadow_dict.has_key(u_name):
				new_shadow.append(recv_shadow_dict[u_name])
			else:
				new_shadow.append(entry[1])

		return string.join(new_shadow, '\n') + '\n'
