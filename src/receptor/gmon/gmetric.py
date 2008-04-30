#!/opt/rocks/bin/python
#
# A Wrapper around the C-based Gmetric Ganglia module.
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
# $Log: gmetric.py,v $
# Revision 1.2  2008/03/06 23:41:45  mjk
# copyright storm on
#
# Revision 1.1  2008/01/04 23:04:44  bruno
# moved ganglia-pylib and receptor from hpc to base roll
#
# Revision 1.8  2007/06/23 04:03:40  mjk
# mars hill copyright
#
# Revision 1.7  2006/09/11 22:48:54  mjk
# monkey face copyright
#
# Revision 1.6  2006/08/10 00:10:58  mjk
# 4.2 copyright
#
# Revision 1.5  2006/06/30 12:26:32  bruno
# moved all ganglia python code in hpc roll to point to the rocks foundation
# python
#
# Revision 1.4  2005/10/12 18:09:50  mjk
# final copyright for 4.1
#
# Revision 1.3  2005/09/16 01:03:27  mjk
# updated copyright
#
# Revision 1.2  2005/05/24 21:22:51  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/12 00:50:27  fds
# Greceptor. Moved from monolithic source tree.
#
# Revision 1.2  2004/11/04 00:00:40  fds
# Greceptor needs to listen on the gmond channel too.
#
# Revision 1.1  2004/11/02 00:57:03  fds
# Same channel/port as gmond. For bug 68.
#
#

import socket
# Our gmetric python extension in C.
from gmon.Gmetric import publish

class Tx:
	"""Wrapper class around Ganglia publish function. Can match
	to gmond's multicast channel."""

	def __init__(self):
		self.chan = "239.2.11.71"
		self.port = 8649
		# Read channel from gmond config
		try:
			g=open('/etc/gmond.conf','r')
			for line in g.readlines():
				tokens = line.split()
				if tokens[0] == "mcast_channel":
					self.chan=tokens[1]
					if self.chan[0] == '"':
						self.chan = self.chan[1:-1]
				elif tokens[0] == "mcast_port":
					self.port=int(tokens[1])
			g.close()
		except:
			pass


	def setChannel(self, channel):
		self.chan = socket.gethostbyname(channel)

	def getChannel(self):
		return self.chan

	def setPort(self, port):
		self.port = port

	def getPort(self):
		return self.port

	def publish(self, name, value, units="", slope="", tmax=1800,
			dmax=3600, port=0, channel="", type=""):

		if not channel:
			channel=self.chan
		if not port:
			port=self.port

		publish(name, value, units, slope, tmax,
			dmax, port, channel, type)

	
