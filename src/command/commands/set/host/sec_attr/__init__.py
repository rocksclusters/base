# $Id: __init__.py,v 1.1 2011/06/03 02:34:39 anoop Exp $

# @Copyright@
# @Copyright@

# $Log: __init__.py,v $
# Revision 1.1  2011/06/03 02:34:39  anoop
# Added code for secure_attributes
#

import os
import sys
import rocks.commands
import sha
import crypt
import rocks.password
import getpass
import random
import string

class Command(rocks.commands.set.host.command):
	"""
	Set a host-specific secure attribute to the database.
	The user also has the option of not supplying the
	value on the command line. The command will prompt
	the user to enter the secure attribute value, and
	will not echo this value on screen.

	If the user chooses to enter the value for the secure
	attribute by prompt, then the value entered must be in
	an unencrypted form.
	<arg type="string" name='host'>
	Host name of machine
	</arg>
	
	<param type='string' name='attr'>
	Name of the attribute
	</param>

	<param type='string' name='value'>
	Value of the attribute
	</param>
	
	<param type='boolean' name='crypted'>
	Is "value" already crypted or not
	</param>

	<param type='string' name='enc'>
	Encryption scheme to use to crypt the value. Currently
	supported values are "sha", "crypt", "portable".
	</param>

	<example cmd='set host sec_attr compute-0-0 attr=db_pw
	value=DatabasePassword crypted=false enc=sha'>
	Sets a secure attribute called db_pw to the crypted value
	of "DatabasePassword" using the sha1 encoding schema.
	</example>

	<example cmd='set host sec_attr compute-0-0 attr=db_pw
	value=77e6674e6d71f898d5fc79424117c86731ca7498 crypted=true'>
	Same as above
	</example>
	"""
	def run(self, params, args):
		hosts = self.getHostnames(args)
		
		# Get params
		(attr, value, crypted, enc) = self.fillParams([('attr', None),
						('value', None),
						('crypted','n'), ('enc', None)])

		if attr is None:
			self.abort('missing attribute name')

		# Check if value is supposed to be crypted
		crypted = self.str2bool(crypted)

		if enc is not None:
			self.enc = rocks.password.Enc()
			if hasattr(self.enc, 'enc_%s' % enc):
				f = getattr(self.enc, 'enc_%s' % enc)
			else:
				self.abort('Encryption method %s not supported' % enc)

		if value is None:
			if crypted == 1:
				sys.stderr.write('Ignoring crypted argument\n')
			crypted = 0
			value = getpass.getpass('  Enter %s: ' % attr)
			c_value = getpass.getpass('Confirm %s: ' % attr)
			if c_value != value:
				self.abort('Values don\'t match')
			


		if enc is not None and crypted == 0:
			enc_value = f(value)

		if crypted == 1:
			enc_value = value

		for host in hosts:
			rows = self.db.execute('select enc from sec_node_attributes ' + \
				'where node=(select id from nodes where name="%s") ' % host +\
				'and attr="%s"' % attr)
			if rows:
				if enc is None and crypted == 0:
					(enc, ) = self.db.fetchone()
					f = getattr(self.enc, 'enc_%s' % enc)
					enc_value = f(value)
				self.db.execute('update sec_node_attributes '	+\
					'set value="%s", enc="%s" where node=' % (enc_value, enc) +\
					'(select id from nodes where name='	+\
					'"%s") and attr="%s"' % (host, attr))
			else:
				if enc is None and crypted == 0:
					enc = 'sha'
					f = getattr(self.enc, 'enc_%s' % enc)
					enc_value = f(value)
				self.db.execute('insert into sec_node_attributes ' +\
				'values ((select id from nodes where name="%s"), "%s", "%s", "%s")' \
				% (host, attr, enc_value, enc))

	def enc_sha(self, value):
		s = sha.sha(value)
		return s.hexdigest()

	def enc_crypt(self, value):
		salt = '$1$'
		for i in range(0, 8):
			salt += random.choice(
			string.ascii_letters +
			string.digits + './')
		return crypt.crypt(value, salt)
	
	def enc_portable(self, value):
		p = rocks.password.Password()
		return p.create_password(value)
