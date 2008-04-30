#!/usr/bin/python

import os
import sys
import re

script_dir = '/etc/rc.d/rocksconfig.d/'

#
# get a directory listing of postconfig.d, then sort it
#
scripts = os.listdir(script_dir)
scripts.sort()

command = sys.argv[1]

# Execute each script in order, and lock the command so it isn't
# repeated.  We used to erase the evidence, but this made debugging
# hard.

for i in scripts:
	if not os.path.isfile('/var/lock/%s' % command):
		#
		# write the error output of the script to a debug file
		#
		cmd = '%s > /tmp/%s.debug 2>&1' % \
					(os.path.join(script_dir, i), i)

		if command == 'before-rc':
			if re.match('^pre.*', i) != None:
				os.system(cmd)
		elif command == 'after-rc':
			if re.match('^post.*', i) != None:
				os.system(cmd)
	

file = open('/var/lock/%s' % command, 'w')
file.close()

