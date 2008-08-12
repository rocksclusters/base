# $Id: passwd.py,v 1.2 2008/08/12 23:20:13 anoop Exp $

# @Copyright@
# @Copyright@

# $Log: passwd.py,v $
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
