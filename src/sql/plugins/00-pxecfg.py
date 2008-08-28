#
# insert-ethers plugin module for generating pxelinux cfg files

# $Id: 00-pxecfg.py,v 1.1 2008/08/28 18:12:45 anoop Exp $
# 
# @Copyright@
# @Copyright@
#
# $Log: 00-pxecfg.py,v $
# Revision 1.1  2008/08/28 18:12:45  anoop
# Now solaris installations use pxelinux to chainload pxegrub. This
# way we can keep generation of pxelinux files controlled through
# "rocks add host pxeaction" and thus keep the content of
# pxelinux files consistent and managed.
#

import os
import sys
import string
import rocks.sql

class Plugin(rocks.sql.InsertEthersPlugin):
	"Controls the DHCP server when nodes are added and removed."

	def added(self, nodename, id):
		sql_q  = "select os from nodes where " +\
			"name='%s'" % (nodename)
		self.app.execute(sql_q)
		osname = self.app.fetchone()[0].strip()
		if osname == 'sunos':
			for action in [
				'install',
				'install headless',
				'rescue',
				]:
				cmd = "/opt/rocks/bin/rocks add host pxeaction " +\
					"%s action='%s' " % (nodename, action) +\
					"command='kernel pxegrub.0' args=''"
				os.system(cmd)

		os.system("/opt/rocks/bin/rocks set host pxeboot " +\
			"%s action=%s" % (nodename, "install"))

	def removed(self, nodename, id):
		pass

	def update(self):
		pass

	def done(self):
		pass

	def restart(self):
		pass
