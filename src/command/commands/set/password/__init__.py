# $Id: __init__.py,v 1.6 2012/05/06 05:48:36 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.5 (Mamba)
# 		         version 6.0 (Mamba)
# 
# Copyright (c) 2000 - 2012 The Regents of the University of California.
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
# $Log: __init__.py,v $
# Revision 1.6  2012/05/06 05:48:36  phil
# Copyright Storm for Mamba
#
# Revision 1.5  2011/07/23 02:30:39  phil
# Viper Copyright
#
# Revision 1.4  2010/09/07 23:53:02  bruno
# star power for gb
#
# Revision 1.3  2010/07/08 23:45:18  bruno
# password setting fixes
#
# Revision 1.2  2009/05/01 19:07:04  mjk
# chimi con queso
#
# Revision 1.1  2009/02/10 20:41:46  bruno
# change the root password for various cluster services
#
#


import os
import pwd
import getpass
import crypt
import rocks.commands


class Command(rocks.commands.Command):
	"""
	Change the root password for relevant cluster services.
	"""

	def readpassword(self):
		#
		# read the old password
		#
		p = pwd.getpwuid(os.geteuid())

		if p[0] != 'root':
			self.abort('must be root to change the password')

		if p[1] in [ 'x', '*' ]:
			#
			# need to read /etc/shadow (python v2.6 has the
			# 'spwd' which does that for you).
			#
			file = open('/etc/shadow', 'r')
	
			for line in file.readlines():
				l = line.split(':')
				if len(l) > 1 and l[0] == 'root':
					oldpw = l[1]
					break

			file.close()
		else:
			oldpw = p[1]
			
		return oldpw

	
	def run(self, params, args):
		if len(args):
			self.abort('command does not take arguments')

		old_password = getpass.getpass('current UNIX password: ')

		#
		# check if the old password matches
		#
		oldpw = self.readpassword()

		if crypt.crypt(old_password, oldpw) != oldpw:
			self.abort('The current password you entered ' +
				'does not match the stored password')

		while 1:
			new_password = getpass.getpass('new UNIX password: ')
			confirm_new_password = getpass.getpass(
				'retype new UNIX password: ')

			if new_password == confirm_new_password:
				break
			else:
				print 'Sorry, the passwords do not match'
		
		self.runPlugins( [ old_password, new_password ] )

