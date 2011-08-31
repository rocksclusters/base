# $Id: root_pw.py,v 1.2 2011/08/31 00:53:22 anoop Exp $

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
		import shutil
		shutil.move(tfname, '/etc/shadow')
