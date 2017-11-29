# $Id: googleotp_411.py,v 1.2 2012/11/27 00:48:38 phil Exp $

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

# $Log: googleotp_411.py,v $
# Revision 1.2  2012/11/27 00:48:38  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.1  2012/10/18 17:55:21  phil
# 411 plugin for google authenticator.  creates a tar file of all keys (except
# root) and transfers to login appliances
#
#

import os
import sys
import rocks
import rocks.service411
import string
import subprocess

class Plugin(rocks.service411.Plugin):

	# THIS IS AN ABSOLUTE MUST FOR ALL PLUGINS. WITHOUT THIS,
	# PLUGINS WONT WORK
	def get_filename(self):
		return "/export/google-authenticator/keys.tar"

	def pre_send(self, content):
		# keys.tar is an empty file/contents ignored
		# this creates a tar file output stream of the directory 
		# which is then transmitted.
                # Never send root's key
		cmd = "cd /export/google-authenticator;"
		cmd += "/bin/tar cf - --exclude=root --exclude=keys.tar --no-recursion *"
		newcontent = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
		return newcontent.read() 


	# Function to extract the keys 
	def post(self):

		# first delete all existing keys, to clean out any 
                # that were deleted on the fronted.  
		# never delete root's key, it is considered local

		cmd1 = "find /export/google-authenticator -type f -not -name keys.tar -not -name root -exec /bin/rm {} \;"
		subprocess.call(cmd1, shell=True)

		# now extract the new keys
		cmd = "cd /export/google-authenticator;"
		cmd += "/bin/tar xfp /export/google-authenticator/keys.tar"

		subprocess.call(cmd, shell=True)
		
