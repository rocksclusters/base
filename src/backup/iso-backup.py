#! @PYTHON@
#
# $Id: iso-backup.py,v 1.12 2009/05/01 19:06:50 mjk Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
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
# $Log: iso-backup.py,v $
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
# Revision 1.8  2004/03/25 03:15:15  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.7  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.6  2003/05/22 16:39:27  mjk
# copyright
#
# Revision 1.5  2003/02/28 20:47:21  bruno
# not dead-on-arrival -- use the dao
#
# Revision 1.4  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.3  2003/01/17 21:22:51  mjk
# fix dvdrecord command line
#
# Revision 1.2  2003/01/16 23:02:22  mjk
# *** empty log message ***
#
# Revision 1.1  2002/10/28 20:16:20  mjk
# Create the site-nodes directory from rocks-dist
# Kill off mpi-launch
# Added rocks-backup
#
# Revision 1.2  2002/02/21 21:33:27  bruno
# added new copyright
#
# Revision 1.1  2002/01/11 19:41:42  mjk
# Add rocks-backup package
#


import os
import sys
import time
import string
import popen2
import rocks.app


class App(rocks.app.Application):

	def __init__(self, argv):
		rocks.app.Application.__init__(self, argv)
		self.usage_name		= 'ISO Backup'
		self.usage_version	= '@VERSION@'
                self.server		= 'cvs.rocksclusters.org'
                self.cgi		= 'cgi-bin/iso-backup.cgi'
                self.path		= '/home/backup'
		self.cdr		= '0,0,0'
		self.verbose		= 0

		# Add application flags to inherited flags
                
		self.getopt.s.extend([('d:', 'path'), ('v')])
		self.getopt.l.extend([('directory=', 'path'),
				      ('host=', 'host'),
				      ('dev=', 'cdr-device'),
				      ('verbose')])

		
	def parseArg(self, c):
		if rocks.app.Application.parseArg(self, c):
			return 1
		elif c[0] in ('-d', '--directory'):
			self.path = c[1]
		elif c[0] == 'host':
			self.server = c[1]
		elif c[0] == 'dev':
			self.cdr = c[1]
		elif c[0] in ( '-v', '--verbose'):
			self.verbose = self.verbose + 1
		else:
			return 0
		return 1


	def burnISO(self, file):
		if self.verbose:
			print 'burning media'
		os.system('dvdrecord dev=%s -dao %s' % (self.cdr, file))
		os.system('dvdrecord dev=%s -eject' % self.cdr)


	def fetchISO(self):
		isoFile = os.path.join(self.path, 'iso-backup.iso')
		if os.path.isfile(isoFile):
			os.remove(isoFile)

		if self.verbose:
			print 'fetching: http://%s/%s' % (self.server, self.cgi)

		if self.verbose > 1:
			qflag = ''
		else:
			qflag = '--quiet'

		cmd = 'wget %s -O %s http://%s/%s' % (qflag, isoFile,
						      self.server, self.cgi)

		if not os.system(cmd):
			return isoFile
		else:
			return None


	def run(self):
		iso = self.fetchISO()
		self.burnISO(iso)



app = App(sys.argv)
app.parseArgs()
app.run()

