#!/opt/rocks/bin/python
#
# A metric for Gschedule that pulls all 411 files at 
# a low polling interval. In this way all clients can
# maintain weak consistancy with the master.
#
# The 411 file names indicate where on the local filesytem
# they should be placed:
#
#	etc.group -> /etc/group
# etc.auto..home -> /etc/auto.home
#
# 411 naming convention is similar to the python/java import
# engine.
#
# This module does not actually use any Ganglia-specific
# features - Gschedule simply schedules it to run at a
# uniformly random frequency.
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		            version 5.0 (V)
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
# $Log: event411.py,v $
# Revision 1.2  2008/03/06 23:41:32  mjk
# copyright storm on
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
# Revision 1.8  2006/09/11 22:48:48  mjk
# monkey face copyright
#
# Revision 1.7  2006/08/10 00:10:53  mjk
# 4.2 copyright
#
# Revision 1.6  2006/01/16 06:49:10  mjk
# fix python path for source built foundation python
#
# Revision 1.5  2005/10/12 18:09:41  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:03:19  mjk
# updated copyright
#
# Revision 1.3  2005/08/08 21:24:59  mjk
# foundation
#
# Revision 1.2  2005/05/24 21:22:44  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/01 02:02:40  mjk
# moved from core to base
#
# Revision 1.25  2005/01/24 23:37:45  fds
# Using my simplehttp library for transfers in 411. No memory leaks, no more
# forking from threads. TCP retries now greatly simplified in the listener.
#
# Revision 1.24  2005/01/04 22:09:02  fds
# Retry multiple times if necessary, dont rely on TCP.
#
# Revision 1.23  2004/07/21 00:50:25  fds
# 411get listing now respects groups. Moved group processing into
# base class.
#
# Revision 1.22  2004/07/20 19:47:18  fds
# 411 group support. Also cleaned out some depricated options.
#
# Revision 1.21  2004/06/03 18:11:34  fds
# Slightly more stable.
#
# Revision 1.20  2004/04/13 20:09:31  fds
# Can set polling interval in config file.
#
# Revision 1.19  2004/04/05 19:47:01  mjk
# case matters
#
# Revision 1.18  2004/03/29 20:15:08  mjk
# - Changed frequency to 15 minutes (down from 24 hours)
# - 80 col the code (have to move some blocks around to minimize indents
# - Only create lock file if ALL files have been created
#
# Revision 1.17  2004/03/25 03:15:12  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.16  2003/11/17 18:56:19  fds
# Fixes from rockstar testing.
#
# Revision 1.15  2003/11/05 23:25:06  fds
# Added lock file and new initscript to wait for login files.
#
# Revision 1.14  2003/10/20 19:31:39  fds
# Respect to master scores, better doc formatting.
# Turned off debug mode for all modules.
#
# Revision 1.13  2003/09/09 01:44:42  fds
# Using Master helper class. Started
# structure for complex 411 service.
#
# Revision 1.12  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.11  2003/07/25 18:01:34  fds
# Added /etc/411.d and removed debug mode.
#
# Revision 1.10  2003/07/23 18:47:55  fds
# Added 'disable' option to the config file.
#
# Revision 1.9  2003/07/22 22:19:45  fds
# Getting ready for packaging.
#
# Revision 1.8  2003/07/21 23:48:04  fds
# Can handle bad conf files, and does more CVS-like keyword expansion.
#
# Revision 1.7  2003/07/16 21:28:56  fds
# Sign, verify deal with base64 signatures now, header format improved.
#
# Revision 1.6  2003/07/15 23:48:57  fds
# New 411 alert design.
#
# Revision 1.4  2003/07/13 23:32:24  fds
# Less suceptible to a man-in-the-middle-attack. File name,
# owner, and mode are now encrypted along with the contents in HTTP-style headers.
# Naming them only in the HTTP filename was unsafe.
#
# Revision 1.3  2003/07/11 19:04:41  fds
# Handles directories, and transmits file meta data.
#
# Revision 1.1  2003/07/02 23:26:09  fds
# A low frequency 411 pull engine (Ganglia independant).
#
#

import os
import os.path
import sys
import shutil
import string
import gmon.events
import rocks.service411
from rocks.service411 import Error411
import stat


# Multiple inheritance with a bias towards Metric.

class Event411(gmon.events.Metric, rocks.service411.Service411):
	"""Pulls every 411 file from the first available master server,
	and names them correctly on the local machine."""

	def __init__(self, app):
		gmon.events.Metric.__init__(self, app)
		rocks.service411.Service411.__init__(self)
		self.conf_mtime = 0
		self.debug = 0

		# Poll every 5 hours by default.  Even when multicast code
		# fails the core system will still work. Can override this
		# in conf file.

		self.interval = 18000
		self.setConfHandler(ConfHandler)

		self.setFrequency(self.interval)

		if self.debug:
			print "Interval frequency is", self.interval
			self.setFrequency(10)
			self.rootdir = "/tmp"


	def name(self):
		return "411-poller"
		
		
	def schedule(self, sched):
		"""Chooses whether or not to schedule ourself."""
		if self.disable:
			return
		else:
			gmon.events.Metric.schedule(self, sched, now=1)


	def getAlarm(self):
		return 30


	def run(self):
		"""Pulls each 411 file from master and writes it to disk."""

		self.checkConf()

		try:
			files = self.find()
		except ValueError:
			# There were no master servers in config file.
			pass
		except Error411, msg:
			self.warning(msg)
		else:
			for file in files.keys():
				try:
					contents, meta = self.get(file)
					self.write(contents, meta, files[file])
				except Error411, msg:
					self.warning("getting file: %s: %s" 
						% (file, msg))

			self.disconnect()


	def checkConf(self):
		"""Checks for the existance of the configuration file. If it
		exists, and has changed since last time (by 411 listener), we
		reparse it."""

		conf = self.config.getFile()
		if not os.path.exists(conf):
			return

		s = os.stat(conf)
		mtime = s[stat.ST_MTIME]
		if mtime != self.conf_mtime:
			self.config.parse()

		self.conf_mtime = mtime



class ConfHandler(rocks.service411.ConfHandler):
	
	def startElement_interval(self, name, attrs):
		self.app.interval = int(attrs.get('sec', self.app.interval))


def initEvents():
	return Event411
