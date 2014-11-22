#!/opt/rocks/bin/python
#
# Encrypts and prepares a file for publishing
# in the 411 information service. Can handle regular
# files and directories.
#
# Requires Python 2.1 or better
#
# $Id: 411put.py,v 1.18 2012/11/27 00:48:02 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
# 
# Copyright (c) 2000 - 2014 The Regents of the University of California.
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
# $Log: 411put.py,v $
# Revision 1.18  2012/11/27 00:48:02  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.17  2012/05/06 05:48:16  phil
# Copyright Storm for Mamba
#
# Revision 1.16  2011/07/23 02:30:22  phil
# Viper Copyright
#
# Revision 1.15  2011/06/21 06:05:05  anoop
# Obtain IP address and 411 port information from the database
# as opposed to divining it from archaic gmon interfaces
#
# Revision 1.14  2011/05/13 21:56:08  anoop
# If plugin doesn't match reset plugin instance to None
#
# Revision 1.13  2011/04/26 23:23:26  anoop
# Minor modification to 411put. Use a get_filename function instead of
# a filename constant.
#
# Revision 1.12  2011/04/26 03:30:27  anoop
# Support for pre-send filtering of content,
# and post receive actions.
# Minor cleanup in the way temp files are created.
#
# Revision 1.11  2010/11/20 20:57:49  bruno
# on a 'rocks sync config', we need to update /opt/rocks/etc/four11putrc
# with the private address and CIDR netmask to tell 411put where the local
# network is. without this assistance, 411put assumes eth0 is the private
# network and if the frontend has a bonded interface for the private network,
# then 411put will not know where to send its alerts.
#
# Revision 1.10  2010/10/20 21:26:08  mjk
# Call out to 411-alert to send RPC, no more ganglia protocol
#
# Revision 1.9  2010/10/18 23:53:03  bruno
# 411put no longer sends out 411 alerts
#
# Revision 1.8  2010/09/07 23:52:48  bruno
# star power for gb
#
# Revision 1.7  2009/05/01 19:06:49  mjk
# chimi con queso
#
# Revision 1.6  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.5  2008/08/12 23:20:13  anoop
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
# Revision 1.4  2008/07/17 01:29:40  anoop
# Changed 411put to use XML as transport rather than http style headers. This
# makes it significantly more flexible, to use and abuse. Adds python code
# that will filter the content of the file.
#
# Revision 1.3  2008/03/06 23:41:32  mjk
# copyright storm on
#
# Revision 1.2  2008/02/15 00:06:48  mjk
# - Apply the HG Changeset from Takahiro Hirofuchi (AIST)
# - Modified changeset to ignore services and rpc files
#
# # HG changeset patch
# # User root@vizzy.rocksclusters.org
# # Date 1203022614 28800
# # Node ID fc6e0b98fef1a65932eef3e5e5ad2bedf5b634b4
# # Parent  2716de75af4304c3e3d261fb9cf19a1c8d988f56
# Fix too slow booting bug caused by overrunning of vol_id.
# Remove comment headers from /etc/{passwd,group,shadow} because udev's
# vol_id cannot parse it correctly.
#
# Revision 1.1  2007/12/10 21:28:33  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.9  2007/06/23 04:03:38  mjk
# mars hill copyright
#
# Revision 1.8  2006/09/11 22:48:49  mjk
# monkey face copyright
#
# Revision 1.7  2006/08/10 00:10:53  mjk
# 4.2 copyright
#
# Revision 1.6  2006/01/16 06:49:10  mjk
# fix python path for source built foundation python
#
# Revision 1.5  2005/10/12 18:09:42  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:03:19  mjk
# updated copyright
#
# Revision 1.3  2005/08/08 21:25:00  mjk
# foundation
#
# Revision 1.2  2005/05/24 21:22:45  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/01 02:02:40  mjk
# moved from core to base
#
# Revision 1.7  2005/02/12 02:27:54  fds
# 411 second generation: safer, thanks to master-only RSA keypair; all files
# are now signed for integrity. Faster for master, since we run the random
# number generator less (only once per cluster lifetime rather than once per
# encryption).  Keys are kept in /etc/411-security. Amen.
#
# Revision 1.6  2005/01/18 16:41:09  fds
# Use broadcast alert signaling rather than multicast. Now --name option respects
# group and chroot state.
#
# Revision 1.5  2004/11/29 20:57:23  fds
# Fix for bug 84. Simplify! Only use the dot-paths to prevent naming collisions
# in 411.d. Use native pathnames to actually write files. Specifically: the 411
# header contains the real path name, not the dot-path translation.
#
# This version of 411 is not compatible with past versions.
#
# Revision 1.4  2004/11/02 00:57:04  fds
# Same channel/port as gmond. For bug 68.
#
# Revision 1.3  2004/07/21 17:46:47  fds
# Alerts handle group names with spaces. Important
# for Rocks Membership names
#
# Revision 1.2  2004/07/20 19:47:19  fds
# 411 group support. Also cleaned out some depricated options.
#
# Revision 1.1  2004/05/25 02:31:05  fds
# Since becoming a 411-master is a job that should not be taken on lightly, we
# are moving the tools necessary for it into a separate package. These files are
# essentially unchanged from those in 'rocks-411', except the initscript, which
# is slightly simpler.
#
# Revision 1.32  2004/03/25 03:15:09  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.31  2004/01/13 18:55:21  fds
# Be quieter when generating makefile. Bug pointed out by Cooper Berthea.
#
# Revision 1.30  2003/10/20 19:31:38  fds
# Respect to master scores, better doc formatting.
# Turned off debug mode for all modules.
#
# Revision 1.29  2003/09/24 23:23:36  fds
# Moved privateIP logic to net app class
#
# Revision 1.28  2003/09/24 19:44:43  fds
# More sophisticated about choosing our master ip address.
#
# Revision 1.27  2003/09/14 17:23:01  fds
# Using our new Networks module
#
# Revision 1.26  2003/09/12 21:43:43  fds
# Cleaning up a bit
#
# Revision 1.25  2003/09/08 05:09:05  fds
# Parsing character data in conf file. Not Used, ugly code, slow.
#
# Revision 1.24  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.23  2003/08/13 21:48:27  fds
# Saved case where child does not exit cleanly on failure.
#
# Revision 1.21  2003/08/12 00:17:30  fds
# Using hostname -i now, more robust.
#
# Revision 1.20  2003/07/28 19:06:49  fds
# Warning about a serious security hole.
#
# Revision 1.19  2003/07/25 22:02:16  fds
# Added Log
#
#

import os
import os.path
import sys
import stat
import time
import base64
import rocks.sql
import rocks.service411
from rocks.service411 import Error411
import socket
from rocks.util import mkdir
from urllib import quote

# Multiple inheritance with a bias towards rocks.Application.
class App(rocks.sql.Application, rocks.service411.Service411):
	"Can encrypt and publish a 411 file."

	def __init__(self, argv):
		rocks.sql.Application.__init__(self, argv)
		rocks.service411.Service411.__init__(self)
		self.usage_name = "411 Publisher"
		self.usage_version = '@VERSION@'
		# Where we store encrypted 411 files.
		self.dir411 = "/etc/411.d"
		self.comment = ""
		self.nocomment = 0
		self.doSee = 0
		self.doAlert = 1
		self.doName = 0
		# Ganglia defaults for alert channel.
		self.group = ''
		self.chroot = ''

		self.getopt.l.extend([
			('pub=', 'RSA public key file'),
			('priv=', 'RSA private key file'),
			('411dir=', 'for message storage'),
			('urldir=', '411 URL path'),
			('comment=', 'Comment character for file'),
			('nocomment', 'Dont add comment header for file'),
			('see', 'Show encryped 411 message'),
			('noalert', 'Dont send multicast 411 alert'),
			('alert=', 'Address (default Ganglia mcast)'),
			('411name', 'Show 411 filename with path'),
			('chroot=', 'root of group file tree'),
			('chroot-here'),
			('group=', 'name (a path like x/y/z...)'),
			('make-shared-key')
			])


	def usageTail(self):
		return """ file
Publishes a file or directory in the 411 information system. The file
absolute path (after any chroots) will be maintained on clients."""


	def parseArgs(self):
		"""Point ourselves at the rocksrc config file, so 
		we dont need our own."""
		rocks.sql.Application.parseArgs(self, rcbase='four11put')
		self.port411 = None
		# This is more complicated than I originally thought.
		# Always use the private cluster address for 411 HTTP alerts.
		try:
			self.connect()
			self.execute('select nodename, ip from '	+\
				'vnet where appliance="frontend" and '	+\
				'subnet="private"')
			(nodename, self.ip,) = self.fetchone()
			self.port411 = int(self.db.getHostAttr(nodename, 'port411'))
		except Exception, msg:
			self.doAlert = 0
			if not self.doName:
				print "Warning:", msg
				print "Alert message will not be sent."


	def parseArg(self, c):
		rocks.app.Application.parseArg(self, c)
		if c[0] == "--pub":
			self.pub_filename = c[1]
		elif c[0] == "--priv":
			self.priv_filename = c[1]
		elif c[0] == "--411dir":
			self.dir411 = os.path.normpath(c[1])
		elif c[0] == "--urldir":
			self.urldir = c[1]
		elif c[0] == "--comment":
			self.comment = c[1]
		elif c[0] == "--nocomment":
			self.nocomment = 1
		elif c[0] == "--see":
			self.doSee = 1
		elif c[0] == "--noalert":
			self.doAlert = 0
		elif c[0] == "--411name":
			self.doName = 1
		elif c[0] == "--group":
			self.group = os.path.normpath(c[1])
			if os.path.isabs(self.group):
				self.group = self.group[1:]
		elif c[0] == "--chroot":
			self.chroot = os.path.normpath(c[1])
		elif c[0] == "--chroot-here":
			self.chroot = os.getcwd()
		elif c[0] == "--make-shared-key":
			print self.makeSharedKey(),
			sys.exit(0)


	def run(self, filename):
		"""Prepare a 411 file for publishing. Uses a hybrid
		RSA-Blowfish encryption method."""

		if not filename:
			raise Error411, "Please specify a file."
		if self.chroot:
			filename = os.path.join(self.chroot, filename)

		if self.doName:
			# Used by 411 makefile.
			fullpath = os.path.abspath(filename)
			if self.chroot:
				fullpath = fullpath.replace(self.chroot, '')
			print os.path.join(self.dir411, self.group,
				self.path411(fullpath))
			return

		if not os.access(filename, os.R_OK):
			raise Error411, "I cannot find or see '%s'" % filename
		if not os.access(self.dir411, os.W_OK):
			raise Error411, "I do not have permission to write to '%s'" % self.dir411

		# What kind of file is this?
		s = os.stat(filename)
		# File type and permissions in a decimal int.
		mode = s[stat.ST_MODE]
		# File type and permission bits in an octal string.
		mode_oct = oct(mode)
		# Owner and group id as numeric ints (dont want to rely on
		# etc/group file).
		owner = "%d.%d" % (s[stat.ST_UID], s[stat.ST_GID])

		# Get the normalized, absolute path name of the file.
		fullpath = os.path.abspath(filename)
		if self.chroot:
			fullpath = fullpath.replace(self.chroot, '')
		filename411 = self.path411(fullpath)


		#####MODIFICATIONS TO SUPPORT FILTERING######
		# Look for filters in /opt/rocks/var/plugins/411
		plugin411_path = '/opt/rocks/var/plugins/411/'
		sys.path.append(plugin411_path)
		mod_file = None
		# Iterate through all the plugins to find the one
		# that will filter the file.
		for plugin_file in os.listdir(plugin411_path):
			if not plugin_file.endswith('.py'):
				continue
			mod_name = plugin_file.split('.py')[0]
			# Import the plugin
			mod = __import__(mod_name)
			# Get the filename that the plugin will
			# process
			plugin = mod.Plugin()
			if plugin.get_filename() == fullpath:
				mod_file = plugin_file
				break
			else:
				plugin = None
		if mod_file == None:
			filter = None
		else:
			f = open(os.path.join(plugin411_path,mod_file), 'r')
			filter = f.read()
			f.close()
		#####END MODIFICATIONS TO SUPPORT FILTERING######


		# 411 file meta data encoded in file. HTTP header style.
		header = "<?xml version='1.0' standalone='yes'?>\n"
		header = "<service411>\n"
		header += "<name>%s</name>\n" 	% fullpath
		header += "<mode>%s</mode>\n" 	% mode_oct
		header += "<owner>%s</owner>\n"	% owner

		plaintext = header

		if stat.S_ISREG(mode):
			file = open(filename, 'r')
			plaintext += "<content>\n<![CDATA[\n"

			content = file.read()
			# Support for pre-send function
			try:
				# if the pre_send function exists in the plugin
				# filter the content through it, before sending
				# it over
				f = getattr(plugin, 'pre_send')
				content = f(content)
			except AttributeError:
				pass
			plaintext += base64.b64encode(content)
			plaintext += "]]>\n</content>\n"
			file.close()

		elif stat.S_ISDIR(mode):
			plaintext += "<directory>%s</directory>\n" % filename411

		else:
			raise Error411, "I can only publish a regular file or a directory."

		if filter is not None:
			plaintext += "<filter>\n<![CDATA[\n"
			plaintext += base64.b64encode(filter)
			plaintext += "]]>\n</filter>\n"
		plaintext += "</service411>"

		# Call the cryptography engine.
		msg = self.encrypt(plaintext)

		# Write the file with the correct name
		dir411 = self.dir411
		if self.group:
			dir411 = os.path.join(self.dir411, self.group)
			mkdir(dir411)

		file = open(os.path.join(dir411, filename411), 'w')
		file.write(msg)
		file.close()

		print "411 Wrote: %s/%s" % (dir411, filename411)
		print "Size: %s/%s bytes (encrypted/plain)" % \
			(len(msg), len(plaintext))
		if self.doAlert:
			self.sendAlert(filename411)


	def sendAlert(self, filename411):
		"""Send an RPC Broadcast packet alerting clients to an updated
		411 file. Message was in Ganglia 2.5.x format but now uses RPC.
		Cryptographic signature covers message in format: "filename seqnum".
		"""

		urldir = self.urldir
		if self.group:
			urldir = quote("%s/%s" % (self.urldir, self.group))

		if self.port411 is None:
			alert = "http://%s/%s/%s" % (self.ip, urldir, filename411)
		else:
			alert = "http://%s:%d/%s/%s" % (self.ip, self.port411,
				urldir, filename411)
		sig   = self.sign(alert)

		# replace ganglia channel with the rocks rpc channel

		os.spawnl(os.P_NOWAIT, '/opt/rocks/sbin/411-alert',
			 '411-alert', alert, sig)

		

#
# My Main
#
app = App(sys.argv)
app.parseArgs()
files = app.getArgs()
try:
	if not files:
		raise Error411, "Please specify a file."
	# Connect to the Rocks database
	app.connect()
	for f in files:
		app.run(f)
except Error411, msg:
	print >> sys.stderr, "**" + str(msg)
	sys.exit(1)
