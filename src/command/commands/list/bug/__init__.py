# $Id: __init__.py,v 1.1 2008/11/21 01:03:46 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		           version 5.1  (VI)
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
# $Log: __init__.py,v $
# Revision 1.1  2008/11/21 01:03:46  bruno
# moved 'dbreport bug' to 'rocks list bug'
#
#

import popen2
from xml.sax import saxutils
import rocks.commands

class Command(rocks.commands.RollArgumentProcessor,
	rocks.commands.list.command):
	"""
	List info about the system to help debug issues.
	
	<example cmd='list bug'>		
	List system info.
	</example>
	"""		

	def networkconfig(self):
		cmd = '/sbin/ifconfig -a'

		r, w, e = popen2.popen3(cmd)

		interface = ''

		self.addText('\t<networkconfig>\n')
		for line in r.readlines():
			l = line.split()
			if len(l) > 1 and l[1] == "Link":
				if interface != '':
					self.addText('\t\t</interface>\n')

				interface = l[0]
				self.addText('\t\t<interface>\n')
				self.addText('\t\t\t<name>')
				self.addText(interface + '</name>\n')

			if len(l) > 2 and l[2][:6] == "encap:":
				encap = l[2][6:]
				self.addText('\t\t\t<encap>')
				self.addText(encap + '</encap>\n')

			if len(l) > 4 and l[3] == "HWaddr":
				self.addText('\t\t\t<hwaddr>')
				self.addText(l[4] + '</hwaddr>\n')

			if len(l) > 1 and l[0] == 'inet' \
					and l[1][:5] == "addr:":
				self.addText('\t\t\t<ipaddr>')
				self.addText(l[1][5:] + '</ipaddr>\n')

			if len(l) > 2 and l[2][:6] == "Bcast:":
				self.addText('\t\t\t<bcast>')
				self.addText(l[2][6:] + '</bcast>\n')

			if len(l) > 3 and l[3][:5] == "Mask:":
				self.addText('\t\t\t<netmask>')
				self.addText(l[3][5:] + '</netmask>\n')

		if interface != '':
			self.addText('\t\t</interface>\n')

		self.addText('\t</networkconfig>\n')

		return


	def globals(self):
		self.db.execute('select membership,service,component,value '
			'from app_globals where site=0 and '
			'component!="PublicRootPassword" and '
			'component!="PrivateRootPassword" and '
			'component!="PrivateMD5RootPassword" and '
			'component!="PrivatePortableRootPassword" and '
			'component!="PrivateSHARootPassword"')
		for col in self.db.fetchall():
			self.addText('\t<appglobal ')
			self.addText('membership="%d" ' % int(col[0]))
			self.addText('service="%s" ' % col[1])
			self.addText('component="%s" ' % col[2])
			self.addText('value="%s"/>\n' % saxutils.escape(col[3]))
			
	def graph(self):
		self.addText('\t<graph>\n')

		graph = self.command('list.host.graph', [ 'localhost' ])

		for line in graph.split('\n'):
			self.addText('\t\t<line>%s</line>\n' %
				saxutils.escape(line))

		self.addText('\t</graph>\n')
		
		
	def rolls(self):
		self.db.execute('select name,version,arch,enabled from rolls '
			'where site=0')
		for col in self.db.fetchall():
			self.addText('\t<roll ')
			self.addText('name="%s" '	% col[0])
			self.addText('version="%s" '	% col[1])
			self.addText('arch="%s" '	% col[2])
			self.addText('enabled="%s"/>\n'	% col[3])


	def run(self, params, args):

		self.beginOutput()

		self.addText('<rocks-bug>\n')
		self.networkconfig()
		self.globals()
		self.rolls()
		self.graph()
		self.addText('</rocks-bug>\n')

		self.endOutput(padChar='')
		
