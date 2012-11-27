#! @PYTHON@
#
# $Id: iso-backup.cgi.py,v 1.16 2012/11/27 00:48:08 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.6 (Emerald Boa)
# 		         version 6.1 (Emerald Boa)
# 
# Copyright (c) 2000 - 2013 The Regents of the University of California.
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
# $Log: iso-backup.cgi.py,v $
# Revision 1.16  2012/11/27 00:48:08  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.15  2012/05/06 05:48:18  phil
# Copyright Storm for Mamba
#
# Revision 1.14  2011/07/23 02:30:23  phil
# Viper Copyright
#
# Revision 1.13  2010/09/07 23:52:48  bruno
# star power for gb
#
# Revision 1.12  2009/05/01 19:06:50  mjk
# chimi con queso
#
# Revision 1.11  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.10  2008/03/06 23:41:33  mjk
# copyright storm on
#
# Revision 1.9  2007/06/23 04:03:20  mjk
# mars hill copyright
#
# Revision 1.8  2006/09/11 22:47:03  mjk
# monkey face copyright
#
# Revision 1.7  2006/08/10 00:09:26  mjk
# 4.2 copyright
#
# Revision 1.6  2006/01/16 06:48:55  mjk
# fix python path for source built foundation python
#
# Revision 1.5  2005/10/12 18:08:32  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:02:12  mjk
# updated copyright
#
# Revision 1.3  2005/07/11 23:51:33  mjk
# use rocks version of python
#
# Revision 1.2  2005/05/24 21:21:48  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/01 02:02:42  mjk
# moved from core to base
#
# Revision 1.7  2004/04/12 17:48:54  mjk
# start splitting the iso
#
# Revision 1.6  2004/03/25 03:15:15  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.5  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.4  2003/05/22 16:39:27  mjk
# copyright
#
# Revision 1.3  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.2  2003/01/17 21:22:51  mjk
# fix dvdrecord command line
#
# Revision 1.2  2002/02/21 21:33:27  bruno
# added new copyright
#
# Revision 1.1  2002/01/11 19:41:42  mjk
# Add rocks-backup package
#


import os
import sys
import cgi
import string
import popen2
import rocks.app


class App(rocks.app.Application):

	def __init__(self, argv):
		rocks.app.Application.__init__(self, argv)
		self.usage_name		= 'ISO Backup'
		self.usage_version	= '@VERSION@'
		self.bs			= '650MB'
		self.chunk		= 0
		self.path		= '/home/cvs/CVSROOT'
		self.form		= cgi.FieldStorage()

		if self.form.has_key('chunk'):
			self.chunk = self.form['chunk'].value

		# Add application flags to inherited flags
                
		self.getopt.s.extend([('d:', 'path')])
		self.getopt.l.extend([('directory=', 'path'),
				      ('chunk=', 'number')])

		
	def parseArg(self, c):
		if rocks.app.Application.parseArg(self, c):
			return 1
		elif c[0] in ('-d', '--directory'):
			self.path = c[1]
			return 0
		elif c[0] == '--chunk':
			self.chunk = c[1]
			return 0
		return 1


	def run(self):
		print 'Content-type: application/octet-stream'
		print			# blank line required


		cmd = 'mkisofs -r -quiet  %s | dd bs=%s skip=%s' % (self.path,
								    self.bs,
								    self.chunk)
		job = popen2.Popen3(cmd)
		while 1:
			data = job.fromchild.read(1024)
			if not data:
				break
			sys.stdout.write(data)
		job.fromchild.close()
		job.tochild.close()
		job.wait()



app = App(sys.argv)
app.parseArgs()
app.run()

