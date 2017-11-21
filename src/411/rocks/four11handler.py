#! /opt/rocks/bin/python
# Given a url, fetch and write the 411 file 
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
#
#
import os
import sys
import random
import syslog
import urllib
import pickle
import rocks.service411

class Handle411(rocks.service411.Service411):

	def __init__(self):
		rocks.service411.Service411.__init__(self)

	def apply(self, url, sig):

		syslog.openlog('411-msg-handler', syslog.LOG_PID, syslog.LOG_LOCAL0)
		# This will fetch and apply a 411 message from the supplied url
		# If a signature is supplied, the message will be verified 
		# Otherwise allow to be called manually to update
		# a file.  This might become the new 411get method.
		
		if sig and not self.verify(url, sig):
			syslog.syslog(syslog.LOG_ERR, 'bad signature')
			return

		url = urllib.unquote(url)

		# If this file is not registered in one of our groups it belongs
		# to other nodes (we just saw it because the alert is broadcasted).
		# In the case just ignore it.
		
		groupPaths = []
		for g in self.groups:
			if not g:
				continue
			groupPaths.append('/'.join(g))

		master = rocks.service411.Master(url)
		path  = master.getDir()
		group = path.replace(self.urldir, '')
		group = group[2:-1]

		found = False
		for g in groupPaths:
			if g.find(group) == 0:
				found = True
		if not found:
			return

		# This msg was for us, so fetch the file using a random retry if
		# the server is busy.
		
		retry = 3
		while retry:
			try:
				contents, meta = self.get(url)
				self.write(contents, meta)
				syslog.syslog(syslog.LOG_INFO, 'wrote (file="%s")' % url)
				try:
					f = getattr(self.plugin, 'post')
					f()
				except:
					pass
				retry = 0
			except Exception, e:
				retry -= 1
				if retry:
					import time
					time.sleep(random.uniform(0, 30))
				else:
					syslog.syslog(syslog.LOG_ERR, 'Error: %s updating %s' % (url, str(e)))



