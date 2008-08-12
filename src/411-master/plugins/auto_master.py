# $Id: auto_master.py,v 1.1 2008/08/12 23:20:13 anoop Exp $

# @Copyright@
# @Copyright@

# $Log: auto_master.py,v $
# Revision 1.1  2008/08/12 23:20:13  anoop
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

import os
import sys
import stat
import rocks.service411

class Plugin(rocks.service411.Plugin):
	filename = '/etc/auto.master'

	def filter_name(self, fname):
		if self.os == 'linux':
			return '/etc/auto.master'
		if self.os == 'sunos':
			return '/etc/auto_master'
