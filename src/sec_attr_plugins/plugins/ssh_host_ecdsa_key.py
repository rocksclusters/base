# $Id: ssh_host_dsa_key.py,v 1.1 2012/07/31 23:20:10 phil Exp $
# Sync the host dsa key

import rocks.commands

import os, sys
import tempfile

class plugin(rocks.commands.sec_attr_plugin):
	def get_sec_attr(self):
		return 'ssh_host_ecdsa_key'

	def filter(self, value):
		import grp
		keyfile = '/etc/ssh/ssh_host_ecdsa_key'
		pubkeyfile = keyfile + '.pub'
		# write the ssh_host_key_rsa file 
		if os.path.exists(keyfile):
			os.chmod(keyfile, 0600)
		f = open(keyfile, 'w')
		f.write(value)
		f.close()
		os.chmod(keyfile, 0400)
		
		# regenerate the public key
		if os.path.exists(pubkeyfile):
			os.unlink(pubkeyfile)
		os.system('ssh-keygen -f %s -y > %s' % (keyfile, pubkeyfile))
		os.chmod(pubkeyfile, 0644)
		
		

