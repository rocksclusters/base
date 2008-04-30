#! /opt/rocks/bin/python
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
# $Log: getrpms.py,v $
# Revision 1.5  2008/03/06 23:41:43  mjk
# copyright storm on
#
# Revision 1.4  2007/06/23 04:03:23  mjk
# mars hill copyright
#
# Revision 1.3  2006/09/11 22:47:15  mjk
# monkey face copyright
#
# Revision 1.2  2006/08/10 00:09:37  mjk
# 4.2 copyright
#
# Revision 1.1  2006/01/19 19:58:01  mjk
# *** empty log message ***
#
# Revision 1.7  2006/01/16 06:48:58  mjk
# fix python path for source built foundation python
#
# Revision 1.6  2005/10/12 18:08:39  mjk
# final copyright for 4.1
#
# Revision 1.5  2005/09/16 01:02:18  mjk
# updated copyright
#
# Revision 1.4  2005/09/02 00:05:49  bruno
# pushing toward 4.1 beta
#
# Revision 1.3  2005/07/20 23:40:58  mjk
# foundation doesn't need docs
#
# Revision 1.2  2005/07/13 01:22:00  mjk
# more foundation changes
#
# Revision 1.1  2005/07/11 21:54:59  mjk
# foundation builds
#

import sys
import os
import rocks.app
import rocks.roll

class App(rocks.app.Application):

	def __init__(self, argv):
		rocks.app.Application.__init__(self, argv)

	def run(self):
		root = self.args[0]
		rpms = self.args[1:]
		dist = rocks.roll.Distribution(self.getArch())
		dist.generate('--notorrent')
		
		for name in rpms:
			for rpm in dist.getRPM(name):
				rpm.installPackage(root, '--excludedocs')
			

app = App(sys.argv)
app.parseArgs()
app.run()
