# $Id: plugin_googleotp.py,v 1.3 2012/11/27 00:48:38 phil Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWindwer)
# 		         version 7.0 (Manzanita)
# 
# Copyright (c) 2000 - 2017 The Regents of the University of California.
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

import os
import string
import subprocess
import rocks.commands
import re

class Plugin(rocks.commands.Plugin):
	"""Adds users to the google-otp group, if specified in attribute"""

	def provides(self):
		return 'googleotp'

	def str2bool(self, s):
		"""Converts an on/off, yes/no, true/false string to 1/0."""
		if s and s.upper() in [ 'ON', 'YES', 'Y', 'TRUE', '1' ]:
			return 1
		else:
			return 0

	def run(self, args):

		f = open("/etc/login.defs","r")
		l = f.readlines()
		try:
			self.UIDMIN = int(filter(lambda x : re.match('^UID_MIN',x), l)[0].strip().split()[1])
			self.UIDMAX = int(filter(lambda x : re.match('^UID_MAX',x), l)[0].strip().split()[1])
		except:
			self.UIDMIN = 1000
			self.UIDMAX = 60000
		# scan the password for users >= 1000
		# this is the default entry as setup by useradd
		otp_users = []
		userOTP = self.db.getHostAttr('localhost', 'Info_GoogleOTPUsers')
		if self.str2bool(userOTP):
			file = open('/etc/passwd', 'r')

			for line in file.readlines():
				l = string.split(line[:-1], ':')			
				if len(l) < 6:
					continue

				username = l[0]
				uid = int(l[2])

				# only users in Range (UID_MIN and UID_MAX from /etc/login.defs)
				if uid >= self.UIDMIN and uid < self.UIDMAX:
					otp_users.append(username)
				file.close()

		rootOTP = self.db.getHostAttr('localhost', 'Info_GoogleOTPRoot')
		if self.str2bool(rootOTP):
			otp_users.append('root')
			
		for user in otp_users:
			# for each otp user,  add them to the google-otp group
			cmd = '/usr/sbin/usermod -a -G google-otp %s' % user
			subprocess.call(cmd, shell=True)

		# touch /export/google-authenticator/keys.tar
		# so that 411 will process any new key files
		cmd = '/bin/touch /export/google-authenticator/keys.tar' 
		subprocess.call(cmd, shell=True)



