#! /opt/rocks/bin/python
#
# Generates restore XML nodes for frontend restore.
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		           version 5.1  (VI)
# 
# Copyright (c) 2000 - 2008 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log: restore.py,v $
# Revision 1.16  2008/10/18 00:55:59  mjk
# copyright 5.1
#
# Revision 1.15  2008/03/06 23:41:41  mjk
# copyright storm on
#
# Revision 1.14  2007/06/23 04:03:21  mjk
# mars hill copyright
#
# Revision 1.13  2006/09/15 02:35:10  mjk
# removed ROCK_ROOT variable, bug 80 (trac.rocksclusters.org)
#
# Revision 1.12  2006/09/11 22:47:08  mjk
# monkey face copyright
#
# Revision 1.11  2006/08/10 00:09:30  mjk
# 4.2 copyright
#
# Revision 1.10  2006/01/16 06:48:57  mjk
# fix python path for source built foundation python
#
# Revision 1.9  2005/10/12 18:08:37  mjk
# final copyright for 4.1
#
# Revision 1.8  2005/09/16 01:02:16  mjk
# updated copyright
#
# Revision 1.7  2005/09/15 22:45:09  mjk
# - copyright updated, but not the final notice for 4.1 (ignore this change)
# - resolv.conf now uses "search" domains for private, then public
# - resolv.conf no longer uses "domain" (replaced by "search")
# - named.conf is now created from dbreport (includes rocks.zone)
# - dns.py requires an argument ("zone", or "reverse")
# - dns config removed (now in named)
# - general dns.py cleanup (simpler logic, tossed dead code)
# - removed domain name related functions from base.py
# - added getGlobalVar to base.py (don't have to go through self.sql anymore)
# - did a diff of the reports vs existing files on rocks-153, looks good
#
# Revision 1.6  2005/07/11 23:51:34  mjk
# use rocks version of python
#
# Revision 1.5  2005/05/26 01:23:14  fds
# run insert-ethers --update earlier
#
# Revision 1.4  2005/05/26 00:20:22  fds
# Restore insert-ethers --update run on first boot.
#
# Revision 1.3  2005/05/24 21:30:10  fds
# Tweaks
#
# Revision 1.2  2005/05/24 21:21:52  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/05/23 23:59:22  fds
# Frontend Restore
#
#

import os
import string
import xml.sax.saxutils
import rocks.reports.base
import getopt


class Report(rocks.reports.base.ReportBase):
	"""Generates a kickstart XML file for non-interactive
	frontend restore"""
	
	site = 0
	client = ''

	def getVars(self, prefix, container):
		"Pulls data for the site from app_globals"

		self.execute('select component, value from app_globals '
			'where service = "%s" and site = %d' % (prefix, self.site))

		for key, value in self.fetchall():
			print '		%s.%s = "%s" ' % (container, key,
				xml.sax.saxutils.escape(value))


	def makeRestoreScreen(self):
		"""Outputs python. An anaconda install window that
		sets all the app_global variables."""

		print 'class RocksRestoreWindow:'
		print '	"Generated." '
		print '	def __call__(self, screen, rocksinfo):'

		self.getVars('Info', 'rocksinfo')

		print '		rocksinfo.restoreKickstart = RocksGlobalData()'

		self.getVars('Kickstart', 'rocksinfo.restoreKickstart')

		print '		rocksinfo.restorePrivate = RocksGlobalData()'

		self.getVars('Private', 'rocksinfo.restorePrivate')
		
		#
		# Special command to read the root password from the command line
		#
		print
		print '		rootpasswd, crypted = rocksGetRootPassword()'
		print '		rocksinfo.restoreKickstart.PrivateRootPassword = crypted'
		print '		rocksinfo.restoreKickstart.PublicRootPassword = crypted'
		print '		rocksinfo.restorePrivate.PureRootPassword = rootpasswd'
		print
		print '		return INSTALL_OK'

	
	def doNode(self):
		"Output a kickstart node file"

		tz = self.sql.getGlobalVar('Kickstart','Timezone', self.site)
		passwd = self.sql.getGlobalVar('Kickstart','PublicRootPassword', self.site)

		print '<?xml version="1.0" standalone="no"?>'
		print '<kickstart roll="rocks">'
		print
		print ' <description>'
		print ' Generated. Restore node for %s cluster' % (self.name),
		print '(%s)' % (self.client)
		print ' </description>'
		print
		print '<main>'
		print ' <timezone>%s</timezone>' % tz
		print ' <rootpw>--iscrypted <var name="Kickstart_PrivateRootPassword"/></rootpw>'
		print '</main>'
		print
		print ' <installclass>'

		#
		# We put the screen and kickstart variables here rather
		# than in <var> tags because we are assured they will always
		# be defined when we need them, they will always be first.
		#
		self.makeRestoreScreen()

		print ' </installclass>'
		print
		
		# This needs to run after the database is up, at the TAIL

		print ' <post>'
		print

		# I am going to need to point insert-ethers to a specific SITE.

		path = '/opt/rocks/sbin'
		cmd = '%s/insert-ethers --dump --site=%s' % (path, self.client)
		for line in os.popen(cmd).readlines():
			print '%s/%s' % (path, line),

		print
		cmd = '%s/add-extra-nic --dump --site=%s' % (path, self.client)
		for line in os.popen(cmd).readlines():
			print '%s/%s' % (path, line),
		print

		# We need to run insert-ethers --update during 
		# first boot.

		print '/opt/rocks/sbin/insert-ethers --update'
		print
		print ' </post>'
		print
		print '</kickstart>'


	def doGraph(self):
		"Output a kickstart graph file"

		print '<?xml version="1.0" standalone="no"?>'
		print '<graph roll="rocks">'
		print
		print ' <description>'
		print ' Generated. Restore graph.'
		print ' </description>'
		print
		print '<order head="TAIL" tail="restore"/>'
		print
		print '<edge from="server" to="restore"/>'
		print
		print '</graph>'


	def run(self):

		usage = "dbreport restore [--kind=node (default) | graph "
		usage += "| installclass] [--site=Addr]"

		kind = "node"
		if len(self.args):
			try:
				(opts, args) = getopt.getopt(self.args, '',
					['kind=','site='])
			except Exception, msg:
				print msg
				print usage
				return

			for key, val in opts:
				if key=='--site':
					self.client = val
					self.site = self.sql.getSiteId(val)
				elif key=='--kind':
					kind = val

		self.name = xml.sax.saxutils.escape(
			self.sql.getGlobalVar('Info','ClusterName', self.site))
		
		if kind=="node":
			self.doNode()
		elif kind=="graph":
			self.doGraph()
		elif kind=="installclass":
			self.makeRestoreScreen()
		else:
			print usage
			return



