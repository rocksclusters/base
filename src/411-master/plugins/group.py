# $Id: group.py,v 1.2 2008/08/12 23:20:13 anoop Exp $

# @Copyright@
# @Copyright@

# $Log: group.py,v $
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
	filename="/etc/group"

	# Function to filter the content of the group file
	def filter_content(self, content):

		# List of groupnames to avoid, irrespective
		# of the GID
		avoid_gname = [
			'nobody',
			'nobody4',
			'noaccess',
			'nfsnobody',
			'nogroup',
			]

		# If the client is a linux box
		# just return the original content
		if self.os == 'linux':
			return content

		# If not, then start filtering
		content = content.rstrip('\n')
		content_lines = content.split('\n')

		# Get all groups greater than 500
		# except for groups.
		group_list = ''
		for line in content_lines:
			line = line.strip()
			entry = line.split(':')
			gid = int(entry[2])
			groupname = entry[0].strip()
			if gid >= 500 and \
				groupname not in avoid_gname:
				group_list = group_list + line + '\n'

		# Open the group file. and read 
		# it's contents, so that we can
		# maintain the UID's less than 500
		# Also maintain all groupnames like
		# nobody, nobody4, etc for solaris
		f = open('/etc/group', 'r')
		group_lines = ''
		line = ''
		for line in f.readlines():
			line = line.strip()
			group_entry = line.split(':')
			gid = int(group_entry[2])
			groupname = group_entry[0].strip()
			if gid < 500 or groupname in avoid_gname:
				group_lines = group_lines + line + '\n'
		f.close()

		group_lines = group_lines + group_list

		return group_lines

	def filter_owner(self, oid):
		if self.os == 'linux':
			return oid
		s = os.stat('/etc/group')
		import stat
		return '%d.%d' % (s[stat.ST_UID], s[stat.ST_GID])
