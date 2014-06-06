#
# $Id: __init__.py,v 1.6 2012/11/27 00:48:25 phil Exp $
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
# $Log: __init__.py,v $
# Revision 1.6  2012/11/27 00:48:25  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.5  2012/05/06 05:48:33  phil
# Copyright Storm for Mamba
#
# Revision 1.4  2012/05/06 05:20:16  phil
# Now support eval tags.
#
# Revision 1.3  2012/02/13 23:05:17  phil
# Closer to proper post extraction. Need to handle eval sections
#
# Revision 1.2  2012/02/13 21:05:40  phil
# Improvement in Entity handling
#
# Revision 1.1  2011/11/02 05:08:56  phil
# First take on bootstrap0. Packages, command line and processing to
# bring up the rocks database on a non-Rocks installed host.
# Also reworked generation of post sections to work more like Solaris:
# Each post section now creates a shell script with the desired interpreter.
# Report post command creates a shell script from the post section of a
# (set of) node xml files.
#
#

import sys
import tempfile
import os.path
import re
import rocks.commands
import rocks.gen
import rocks.profile
from xml.sax import saxutils
from xml.sax import handler
from xml.sax import make_parser


class Command(rocks.commands.report.command):
	"""
	Take STDIN Rocks Graph node file(s) and create shell scripts 
	that execute the post section.

	<param optional='1' type='string' name='os'>
	The OS type.
	</param>

	<param optional='1' type='string' name='arch'>
	The architecture type.
	</param>

	<param optional='1' type='string' name='attrs'>
	Attributes to be used while building the output shell script.
	</param>

	<example cmd="cat database.xml | rocks report post attrs=&quot;{'os':'linux'}&quot;">
	Take database.xml file in the base roll and create a script from the
	post section. Adding attrs="{'os':'linux'}'" to the command will
	also expand os=linux tags.
	</example>

	<example cmd="cat database.xml | rocks report post attrs=&quot;`rocks report host attr localhost pydict=true`&quot;">
	Take database.xml file in the base roll and create a script from the
	post section. Take all attributes from the database 
	</example>
	"""

	
	def prescrub(self, xml, attrs):
		# This handles eval tags
		parser = make_parser()
		graphnode = rocks.profile.Node("temppost")
		handler=rocks.profile.Pass1NodeHandler(graphnode,"report-post",{},attrs, eval=1)
		parser.setContentHandler(handler)
		for line in xml:
			parser.feed(line)
		newxml = handler.getXML()
		return newxml

		
	def scrub(self, xml):
		filename = tempfile.mktemp()

		file = open(filename, 'w')
		file.write(xml)
		file.close()

		scrubbed = ''
		cmd = 'xmllint --nocdata %s' % (filename)
		for line in os.popen(cmd).readlines():
			scrubbed += line
		
		# os.remove(filename)

		return scrubbed
		

	
	def runXML(self, xml):
		list = []

		self.generator.attrs = self.attrs
		self.generator.parse(xml)
		section_name = 'post'
		if self.os == 'sunos':
			section_name = 'finish'

		list += self.generator.generate(section_name)
			
		for line in list:
			if line.startswith("%post") or line.startswith("%end"):
				continue

			self.addOutput('', line.rstrip())


	def run(self, params, args):
		self.os, self.arch, attributes = self.fillParams([
			('os', self.os),
			('arch', self.arch),
			('attrs', )
			])

		c_gen = getattr(rocks.gen,'Generator_%s' % self.os)
		self.generator = c_gen()
		self.generator.setArch(self.arch)
		self.generator.setOS(self.os)

		starter_tag = 'kickstart'
		if self.os == 'sunos':
			starter_tag = 'jumpstart'

		# Either all attributes are explictly specified
		if attributes:
			self.attrs = eval(attributes)
		else:
			# OR implicit from os and arch (common case)
			self.attrs = {}
			self.attrs['os'] = self.os
			self.attrs['arch'] = self.arch

		self.beginOutput()

		xmlheader = '<?xml version="1.0" standalone="no"?>\n'
		xmlentities = ''
		needEntityHeader = True 
		xml = ''

		if attributes:
			for (k, v) in self.attrs.items():
				xmlentities += '\t<!ENTITY %s "%s">\n' % (k, v)

		xmlhdr =re.compile('<\?xml')
		kstag = re.compile('</?kickstart')
		entity = re.compile('<!ENTITY')

		for line in sys.stdin.readlines():
			if xmlhdr.match(line.lower().strip()) is None and  \
				kstag.match(line.lower().strip()) is None:
				# Add Command-line Entities before XML entities
				if entity.match(line.upper().strip()):
					if needEntityHeader:
						xml += xmlentities
						needEntityHeader = False
				xml += line

		xml += '</%s>\n' % starter_tag

		if ( len(xmlentities) > 0  and needEntityHeader ):  
			xmlheader += '<!DOCTYPE rocks-graph [\n'
			xmlheader += xmlentities
			xmlheader += ']>\n'
			xmlheader += '<%s>\n' % starter_tag

		# if the input had ENTITYs, then we need to find the split
                # and add the starter tag
		if ( not needEntityHeader ):
			(entities, body) = xml.split(']>')
			xmlheader += entities
			xmlheader += ']>\n'
			xmlheader += '<%s>\n' % starter_tag
			xml = body

		self.runXML(self.scrub(self.prescrub(xmlheader + xml, self.attrs)))

		self.endOutput(padChar='')

