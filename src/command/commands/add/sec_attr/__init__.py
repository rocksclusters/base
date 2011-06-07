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

class Command(rocks.commands.add.command):
	"""
	Add a secure attribute to the database.
	The user also has the option of not supplying the
	value on the command line. The command will prompt
	the user to enter the secure attribute value, and
	will not echo this value on screen.

	If the user chooses to enter the value for the secure
	attribute by prompt, then the value entered must be in
	an unencrypted form.
	
	<arg type='string' name='attr'>
	Name of the attribute
	</arg>

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

	<example cmd='add sec_attr db_pw
	value=DatabasePassword crypted=false enc=sha'>
	Sets a secure attribute called db_pw to the crypted
	value of "DatabasePassword" using the sha1 encoding schema.
	</example>

	<example cmd='add sec_attr db_pw 
	value=77e6674e6d71f898d5fc79424117c86731ca7498 crypted=true'>
	Same as above
	</example>
	"""
	def run(self, params, args):
		
		(args, attr) = self.fillPositionalArgs(('attr'))
		# Get params
		(attr, value, crypted, enc) = self.fillParams([('attr', attr),
						('value', None),
						('crypted','n'), ('enc', 'sha')])

		if attr is None:
			self.abort('missing attribute name')

		# Check if value is supposed to be crypted
		crypted = self.str2bool(crypted)

		self.enc = rocks.password.Enc()
		if hasattr(self.enc, 'enc_%s' % enc):
			f = getattr(self.enc, 'enc_%s' % enc)
		else:
			self.abort("%s encryption method unsupported" % enc)
		t_host_list = []

		rows = self.db.execute('select * from sec_global_attributes ' + \
			'where attr="%s"' % attr)
		if rows:
			self.abort('Attribute %s already exists' % attr)

		if value is None:
			if crypted == 1:
				sys.stderr.write('Ignoring crypted argument\n')
			crypted = 0
			value = getpass.getpass('  Enter %s: ' % attr)
			c_value = getpass.getpass('Confirm %s: ' % attr)
			if c_value != value:
				self.abort('Values don\'t match')
			


		if crypted == 0:
			enc_value = f(value)
		else:
			enc_value = value

		self.db.execute('insert into sec_global_attributes ' +\
				'values ("%s", "%s", "%s")' \
				% (attr, enc_value, enc))
