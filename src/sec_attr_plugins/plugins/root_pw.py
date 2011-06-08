# $Id: root_pw.py,v 1.1 2011/06/08 00:51:33 anoop Exp $

import rocks.commands

import os, sys
import tempfile

class plugin(rocks.commands.sec_attr_plugin):
	def get_sec_attr(self):
		return 'root_pw'

	def filter(self, value):
		# Open the shadow file
		f = open('/etc/shadow', 'r')
		# Write changes to temporary file
		tf, tfname= tempfile.mkstemp()
		for line in f.readlines():
			line = line.strip()
			split_line = line.split(':')
			# Look for root in shadow file
			if split_line[0].strip() == 'root':
				# if we find it, change it's password
				split_line[1] = value
			# Write back new file
			os.write(tf, ':'.join(split_line) + '\n')
		f.close()
		os.close(tf)
		# Move temporary file back to original file
		os.rename(tfname, '/etc/shadow')
