#! /opt/rocks/bin/python
#
# $Id: profile.py,v 1.26 2009/03/03 00:30:29 mjk Exp $
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
# $Log: profile.py,v $
# Revision 1.26  2009/03/03 00:30:29  mjk
# more attr stuff
#
# Revision 1.25  2009/02/03 20:55:32  bruno
# some more ROCKSDEBUG fixes
#
# Revision 1.24  2009/01/24 02:04:29  mjk
# - more ROCKDEBUG stuff (now to stderr)
# - os attr commands (still incomplete)
# - fix ssl code
#
# Revision 1.22  2009/01/23 23:46:51  mjk
# - continue to kill off the var tag
# - can build xml and kickstart files for compute nodes (might even work)
#
# Revision 1.21  2009/01/08 23:36:01  mjk
# - rsh edge is conditional (no more uncomment crap)
# - add global_attribute commands (list, set, remove, dump)
# - attributes are XML entities for kpp pass (both pass1 and pass2)
# - attributes are XML entities for kgen pass (not used right now - may go away)
# - some node are now interface=public
#
# Revision 1.20  2008/12/23 02:03:31  mjk
# - fix conditional edges for new style
# - conds are no longer labels but nodes, this make dot look better
#
# Revision 1.19  2008/12/23 01:01:19  mjk
# fix rocks list host graph to handle cond instead of arch/os.  The
# label is the created cond python expression.  good for testing.
#
# Revision 1.18  2008/12/23 00:14:05  mjk
# - moved build and eval of cond strings into cond.py
# - added dump appliance,host attrs (and plugins)
# - cond values are typed (bool, int, float, string)
# - everything works for client nodes
# - random 80 col fixes in code (and CVS logs)
#
# Revision 1.17  2008/12/19 21:08:54  mjk
# - solaris jgen code looks more like linux kgen code now
# - removed solaris <part> tag (outside of <main> section)
# - everything using cond now (arch,os are converted)
# - cond now works inside node files also
# - conditional edges work on linux, needs testing on solaris
#
# Revision 1.16  2008/10/18 00:56:02  mjk
# copyright 5.1
#
# Revision 1.15  2008/07/17 01:22:39  anoop
# Small modifications to add the OS parameter correctly when generating
# graphs
#
# Revision 1.14  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.13  2008/02/13 20:18:51  anoop
# Added default value to os argument
#
# Revision 1.12  2007/12/20 21:39:12  anoop
# Added support for automatically choosing the correct node xml file depending
# on the platform on which we're running. On linux, the normal files are
# chosen, and on Solaris sol_<nodename>.xml file is chosen if it exists.
#
# This should eventually go away once the rocks graph is merged.
#
# Revision 1.11  2007/11/27 01:27:50  anoop
# Added support for os attribute to graph and node XML files.
#
# Revision 1.10  2007/09/09 01:11:17  anoop
# - Rolled back previous changes.
#
# - RCS tags are now included again. Will make changes later to make
#   this optional
#
# - Logs are now written to /var/log/rocks-install.log rather than
#   /root/install.log. Solaris does not have /root directory, so perhaps
#   this can be made standard?
#
# - Minor solaris related bug fixes.
#
# Revision 1.9  2007/09/04 19:00:16  anoop
# Makefile now dynamically changes the MySQL socket path during building the
# package on Solaris. On linux, it does not change the path.
#
# NOTE: rcs tags generation commented out for now. Must be re-enabled before
# release
# NOTE: Writing to /root/install.log commented out for now. Must be re-enabled
# before release
#
# Revision 1.8  2007/08/14 20:14:23  anoop
# Fitting pylib and the command line with solaris
# mechs
#
# Revision 1.7  2007/06/23 04:03:24  mjk
# mars hill copyright
#
# Revision 1.6  2007/05/10 20:37:02  mjk
# - massive rocks-command changes
# -- list host is standardized
# -- usage simpler
# -- help is the docstring
# -- host groups and select statements
# - added viz commands
#
# Revision 1.5  2007/02/28 03:06:29  mjk
# - "rocks list host xml" replaces kpp
# - kickstart.cgi uses "rocks list host xml"
# - indirects in node xml now works
#
# Revision 1.4  2007/02/27 21:23:35  mjk
# moved SiteNodeHandler out
#
# Revision 1.3  2007/02/26 22:53:37  mjk
# - Refreshed profile.py (kpp.py library code)
#
#
#	History Lost
#	File is kpp.py w/o the App class

import os
import sys
import string
import xml
import popen2
import socket
import base64
import rocks.sql
import rocks.util
import rocks.graph
import rocks.cond
from xml.sax import saxutils
from xml.sax import handler
from xml.sax import make_parser

class RollHandler(handler.ContentHandler,
		  handler.DTDHandler,
		  handler.EntityResolver,
		  handler.ErrorHandler):

	def __init__(self):
		handler.ContentHandler.__init__(self)
		self.rollName  = ''
		self.edgeColor = None
		self.nodeColor = None
		self.nodeShape = 'ellipse'

	def getRollName(self):
		return self.rollName
	
	def getEdgeColor(self):
		return self.edgeColor

	def getNodeColor(self):
		return self.nodeColor

	def getNodeShape(self):
		return self.nodeShape
	
	# <roll>
	
	def startElement_roll(self, name, attrs):
		self.rollName = attrs.get('name')
		
	
	# <color>
	
	def startElement_color(self, name, attrs):
		if attrs.get('edge'):
			self.edgeColor = attrs.get('edge')
		if attrs.get('node'):
			self.nodeColor = attrs.get('node')


	def startElement(self, name, attrs):
		try:
			eval('self.startElement_%s(name, attrs)' % name)
		except AttributeError:
			pass

	def endElement(self, name):
		try:
			eval('self.endElement_%s(name)' % name)
		except AttributeError:
			pass


class AttributeHandler:

	def setAttributes(self, attrs):
		list = []
		list.append('<?xml version="1.0" standalone="no"?>\n')
		list.append('<!DOCTYPE rocks-graph [\n')
		for (k, v) in attrs.items():
			list.append('\t<!ENTITY %s "%s">\n' % (k, v))
		list.append(']>\n')
		self.header = string.join(list, '')

	def getXMLHeader(self):
		return self.header

	
class GraphHandler(handler.ContentHandler,
		   handler.DTDHandler,
		   handler.EntityResolver,
		   handler.ErrorHandler,
		   AttributeHandler):

	def __init__(self, attrs):
		handler.ContentHandler.__init__(self)
		self.setAttributes(attrs)
		self.graph			= rocks.util.Struct()
		self.graph.main			= rocks.graph.Graph()
		self.graph.order		= rocks.graph.Graph()
		self.attrs			= rocks.util.Struct()
		self.attrs.main			= rocks.util.Struct()
		self.attrs.main.default		= rocks.util.Struct()
		self.attrs.order		= rocks.util.Struct()
		self.attrs.order.default	= rocks.util.Struct()
		self.attributes			= attrs
		self.entities			= {}
		self.roll			= ''
		self.text			= ''
		self.os				= attrs['os']
		

	def getMainGraph(self):
		return self.graph.main

	def getOrderGraph(self):
		return self.graph.order

	def parseNode(self, node, eval=1):
		if node.name in [ 'HEAD', 'TAIL' ]:
			return
		
		nodesPath = [ os.path.join('.',  'nodes'),
			      os.path.join('..', 'nodes'),
			      os.path.join('.',  'site-nodes'),
			      os.path.join('..', 'site-nodes')
			      ]

		# Find the xml file for each node in the graph.  If we
		# can't find one just complain and abort.

		xml = [ None, None, None ] # rocks, extend, replace
		for dir in nodesPath:
			if self.os == 'sunos':
				file = os.path.join(dir, 'sol_%s.xml'\
						% node.name)
				if os.path.isfile(file):
					node.name = 'sol_%s' % node.name
			if not xml[0]:
				file = os.path.join(dir, '%s.xml' % node.name)
				if os.path.isfile(file):
					xml[0] = file
			if not xml[1]:
				file = os.path.join(dir, 'extend-%s.xml'\
						    % node.name)
				if os.path.isfile(file):
					xml[1] = file
			if not xml[2]:
				file = os.path.join(dir, 'replace-%s.xml'\
						    % node.name)
				if os.path.isfile(file):
					xml[2] = file

		if not (xml[0] or xml[2]):
			raise rocks.util.KickstartNodeError, \
			      'cannot find node "%s"' % node.name

		xmlFiles = [ xml[0] ]
		if xml[1]:
			xmlFiles.append(xml[1])
		if xml[2]:
			xmlFiles = [ xml[2] ]

		for xmlFile in xmlFiles:
		
			# 1st Pass
			#	- Expand XML Entities
			#	- Expand VAR tags (going away)
			#	- Expand EVAL tags
			#	- Expand INCLUDE/SINCLUDE tag
			#	- Logging for post sections

			fin = open(xmlFile, 'r')
			parser = make_parser()
			handler = Pass1NodeHandler(node, xmlFile, 
				self.entities, self.attributes, eval)
			parser.setContentHandler(handler)
			parser.feed(handler.getXMLHeader())

			for line in fin.readlines():
			
				# Some of the node files might have the <?xml
				# document header.  Since we are replacing
				# the XML header with our own (which includes
				# the entities) we need to skip it.
				
				if line.find('<?xml') != -1:
					continue
					
				# Send the XML to stderr for debugging before
				# we parse it.
				
				if os.environ.has_key('ROCKSDEBUG'):
					sys.stderr.write('[parse1]%s' % line)
				parser.feed(line)
				
			fin.close()
			
			# 2nd Pass
			#	- Annotate all tags with ROLL attribute
			#	- Annotate all tags with FILE attribute
			#	- Strip off KICKSTART tags
			#
			# The second pass is required since EVAL tags can
			# create their own XML, instead of requiring the
			# user to annotate we do it for them.
			
			parser = make_parser()
			xml = handler.getXML()
			handler = Pass2NodeHandler(node, self.attributes)
			parser.setContentHandler(handler)
			if os.environ.has_key('ROCKSDEBUG'):
				sys.stderr.write('[parse2]%s' % xml)
			parser.feed(xml)

			# Attach the final XML to the node object so we can
			# find it again.
			
			node.addXML(handler.getXML())
			node.addKSText(handler.getKSText())


	def addOrder(self):
		if self.graph.order.hasNode(self.attrs.order.head):
			head = self.graph.order.getNode(self.attrs.order.head)
		else:
			head = Node(self.attrs.order.head)

		if self.graph.order.hasNode(self.attrs.order.tail):
			tail = self.graph.order.getNode(self.attrs.order.tail)
		else:
			tail = Node(self.attrs.order.tail)

		e = OrderEdge(head, tail, self.attrs.order.gen)
		e.setRoll(self.roll)
		self.graph.order.addEdge(e)


	def addEdge(self):
		if self.graph.main.hasNode(self.attrs.main.parent):
			head = self.graph.main.getNode(self.attrs.main.parent)
		else:
			head = Node(self.attrs.main.parent)

		if self.graph.main.hasNode(self.attrs.main.child):
			tail = self.graph.main.getNode(self.attrs.main.child)
		else:
			tail = Node(self.attrs.main.child)

		e = FrameworkEdge(tail, head)

		e.setConditional(rocks.cond.CreateCondExpr(
			self.attrs.main.arch,
			self.attrs.main.os,
			self.attrs.main.release,
			self.attrs.main.cond))
				
		e.setRoll(self.roll)
		self.graph.main.addEdge(e)


	# <graph>

	def startElement_graph(self, name, attrs):
		if attrs.get('roll'):
			self.roll = attrs.get('roll')
		else:
			self.roll = 'base'

	# <head>

	def startElement_head(self, name, attrs):
		self.text		= ''
		self.attrs.order.gen	= self.attrs.order.default.gen
		
		if attrs.has_key('gen'):
			self.attrs.order.gen = attrs['gen']


	def endElement_head(self, name):
		self.attrs.order.head = self.text
		self.addOrder()
		self.attrs.order.head = None


	# <tail>

	def startElement_tail(self, name, attrs):
		self.text		= ''
		self.attrs.order.gen	= self.attrs.order.default.gen

		if attrs.has_key('gen'):
			self.attrs.order.gen = attrs['gen']

	def endElement_tail(self, name):
		self.attrs.order.tail = self.text
		self.addOrder()
		self.attrs.order.tail = None


	# <to>

	def startElement_to(self, name, attrs):	
		self.text		= ''
		self.attrs.main.arch	= self.attrs.main.default.arch
		self.attrs.main.os	= self.attrs.main.default.os
		self.attrs.main.release	= self.attrs.main.default.release
		self.attrs.main.cond	= self.attrs.main.default.cond

		if attrs.has_key('arch'):
			self.attrs.main.arch = attrs['arch']
		if attrs.has_key('os'):
			self.attrs.main.os = attrs['os']
		if attrs.has_key('cond'):
			self.attrs.main.cond = attrs['cond']
		if attrs.has_key('release'):
			self.attrs.main.release = attrs['release']

	def endElement_to(self, name):
		self.attrs.main.parent = self.text
		self.addEdge()	
		self.attrs.main.parent = None
	

	# <from>

	def startElement_from(self, name, attrs):
		self.text		= ''
		self.attrs.main.arch	= self.attrs.main.default.arch
		self.attrs.main.os	= self.attrs.main.default.os
		self.attrs.main.release	= self.attrs.main.default.release
		self.attrs.main.cond	= self.attrs.main.default.cond
		
		if attrs.has_key('arch'):
			self.attrs.main.arch = attrs['arch']
		if attrs.has_key('os'):
			self.attrs.main.os   = attrs['os']
		if attrs.has_key('cond'):
			self.attrs.main.cond   = attrs['cond']
		if attrs.has_key('release'):
			self.attrs.main.release = attrs['release']


	def endElement_from(self, name):
		self.attrs.main.child = self.text
		self.addEdge()
		self.attrs.main.child = None
		
	# <order>

	def startElement_order(self, name, attrs):
		if attrs.has_key('head'):
			self.attrs.order.head = attrs['head']
		else:
			self.attrs.order.head = None
		if attrs.has_key('tail'):
			self.attrs.order.tail = attrs['tail']
		else:
			self.attrs.order.tail = None
		if attrs.has_key('gen'):
			self.attrs.order.default.gen = attrs['gen']
		else:
			self.attrs.order.default.gen = None
		self.attrs.order.gen = self.attrs.order.default.gen
			
	def endElement_order(self, name):
		if self.attrs.order.head and self.attrs.order.tail:
			self.addOrder()



	# <edge>
	
	def startElement_edge(self, name, attrs):
		if attrs.has_key('arch'):
			self.attrs.main.default.arch = attrs['arch']
		else:
			self.attrs.main.default.arch = None
		if attrs.has_key('os'):
			self.attrs.main.default.os = attrs['os']
		else:
			self.attrs.main.default.os = None
		if attrs.has_key('cond'):
			self.attrs.main.default.cond = attrs['cond']
		else:
			self.attrs.main.default.cond = None
		if attrs.has_key('release'):
			self.attrs.main.default.release = attrs['release']
		else:
			self.attrs.main.default.release	= None
		if attrs.has_key('to'):
			self.attrs.main.parent = attrs['to']
		else:
			self.attrs.main.parent = None
		if attrs.has_key('from'):
			self.attrs.main.child = attrs['from']
		else:
			self.attrs.main.child = None

		self.attrs.main.arch	= self.attrs.main.default.arch
		self.attrs.main.os	= self.attrs.main.default.os
		self.attrs.main.cond	= self.attrs.main.default.cond
		self.attrs.main.release	= self.attrs.main.default.release


	def endElement_edge(self, name):
		if self.attrs.main.parent and self.attrs.main.child:
			self.addEdge()



	def startElement(self, name, attrs):
		try:
			func = getattr(self, "startElement_%s" % name)
		except AttributeError:
			return
		func(name, attrs)


	def endElement(self, name):
		try:
			func = getattr(self, "endElement_%s" % name)
		except AttributeError:
			return
		func(name)

		
	def endDocument(self):
		pass


	def characters(self, s):
		self.text = self.text + s
		


class Pass1NodeHandler(handler.ContentHandler,
	handler.DTDHandler,
	handler.EntityResolver,
	handler.ErrorHandler,
	AttributeHandler):

	"""Sax Parser for the Kickstart Node files"""

	def __init__(self, node, filename, entities, attrs, eval=0):
		handler.ContentHandler.__init__(self)
		self.setAttributes(attrs)
		self.node	= node
		self.entities	= entities
		self.evalShell	= None
		self.evalText	= []
		self.copyData	= None
		self.doEval	= eval
		self.doCopy	= eval
		self.xml	= []
		self.filename	= filename
		self.stripText  = 0

	def startElement_description(self, name, attrs):
		self.stripText = 1

	def endElement_description(self, name):
		pass

	def startElement_changelog(self, name, attrs):
		self.stripText = 1

	def endElement_changelog(self, name):
		pass

	def startElement_copyright(self, name, attrs):
		self.stripText = 1

	def endElement_copyright(self, name):
		pass
	
	# <kickstart>
	
	def startElement_kickstart(self, name, attrs):
	
		# Setup the Node object to know what roll and what filename 
		# this XML came from.  We use this on the second pass to
		# annotated every XML tag with this information
		
		if attrs.get('roll'):
			self.node.setRoll(attrs.get('roll'))
		else:
			self.node.setRoll('unknown')
			

		# Rolls can define individual nodes to be "interface=public".
		# All this does is change the shape of the node on the
		# kickstart graph.  This helps define well know grafting
		# points inside the graph (for example, in the base roll).
 
		if attrs.get('interface'):
			self.node.setShape('box')
		else:
			self.node.setShape('ellipse')
 
			
		self.node.setFilename(self.filename)
		self.startElementDefault(name, attrs)
			

	def startElement_jumpstart(self, name, attrs):
		if attrs.get('roll'):
			self.node.setRoll(attrs.get('roll'))
		else:
			self.node.setRoll('unknown')
			
		if attrs.get('interface'):
			self.node.setShape('box')
		else:
			self.node.setShape('ellipse')
 
			
		self.node.setFilename(self.filename)
		self.startElementDefault(name, attrs)
	
	# <include>

	def startElement_include(self, name, attrs):
		filename = attrs.get('file')
		if attrs.get('mode'):
			mode = attrs.get('mode')
		else:
			mode = 'quote'

		file = open(os.path.join('include', filename), 'r')
		for line in file.readlines():
			if mode == 'quote':
				if os.environ.has_key('ROCKSDEBUG'):
					sys.stderr.write('[include]%s' %
						saxutils.escape(line))
				self.xml.append(saxutils.escape(line))
			else:
				if os.environ.has_key('ROCKSDEBUG'):
					sys.stderr.write('[include]%s' % line)
				self.xml.append(line)
		file.close()

	def endElement_include(self, name):
		pass
	
	# <sinclude> - same as include but allows for missing files

	def startElement_sinclude(self, name, attrs):
		try:
			self.startElement_include(name, attrs)
		except IOError:
			return

	def endElement_sinclude(self, name):
		pass

	# <var>

	def startElement_var(self, name, attrs):
		varName = attrs.get('name')
		varRef  = attrs.get('ref')
		varVal  = attrs.get('val')

		if varVal:
			self.entities[varName] = varVal
		elif varRef:
			if self.entities.has_key(varRef):
				self.entities[varName] = self.entities[varRef]
			else:
				self.entities[varName] = ''
		elif varName:
			#
			# if the entity value is 'None', then we must set
			# it to the empty string. this is because the
			# 'escape' method throws an exception when it
			# tries to XML escape a None type.
			#
			x = self.entities.get(varName)
			if not x:
				x = ''
			
			self.xml.append(saxutils.escape(x))

	def endElement_var(self, name):
		pass

	# <copy>

	def startElement_copy(self, name, attrs):
		if not self.doCopy:
			return
		if attrs.get('src'):
			src = attrs.get('src')
		if attrs.get('dst'):
			dst = attrs.get('dst')
		else:
			dst = src
		tmpfile = '/tmp/kpp.base64'
		self.xml.append('<file name="%s"/>\n' % dst)
		self.xml.append('<file name="%s">\n' % tmpfile)
		try:
			file = open(src, 'r')
			data = base64.encodestring(file.read())
			file.close()
		except IOError:
			data = ''
		self.xml.append(data)
		self.xml.append('</file>\n')
		self.xml.append("cat %s | /opt/rocks/bin/python -c '" % tmpfile)
		self.xml.append('\nimport base64\n')
		self.xml.append('import sys\n')
		self.xml.append("base64.decode(sys.stdin, sys.stdout)' > %s\n"
			 % (dst))
		self.xml.append('rm -rf /tmp/kpp.base64\n')
		self.xml.append('rm -rf /tmp/RCS/kpp.base64,v\n')

	def endElement_copy(self, name):
		pass

	# <eval>
	
	def startElement_eval(self, name, attrs):
		if not self.doEval:
			return
		if attrs.get('shell'):
			self.evalShell = attrs.get('shell')
		else:
			self.evalShell = 'sh'
		if attrs.get('mode'):
			self.evalMode = attrs.get('mode')
		else:
			self.evalMode = 'quote'

		# Special case for python: add the applets directory
		# to the python path.

		if self.evalShell == 'python':
			self.evalShell = os.path.join(os.sep,
				'opt', 'rocks', 'bin', 'python')
			self.evalText = ['import sys\nimport os\nsys.path.append(os.path.join("include", "applets"))\n']
			
		
	def endElement_eval(self, name):
		if not self.doEval:
			return
		for key in self.entities.keys():
			os.environ[key] = self.entities[key]
		r, w = popen2.popen2(self.evalShell)

		if os.environ.has_key('ROCKSDEBUG'):
			for line in string.join(self.evalText, '').split('\n'):
				sys.stderr.write('[eval]%s\n' % line)
		
		for line in self.evalText:
			w.write(line)
		w.close()

		for line in r.readlines():
			if self.evalMode == 'quote':
				self.xml.append(saxutils.escape(line))
			else:
				self.xml.append(line)
		self.evalText  = []
		self.evalShell = None


	# <post>

	def startElement_post(self, name, attrs):
		self.xml.append('\n'
			'<post>\n'
			'<file name="/var/log/rocks-install.log" mode="append">\n'
			'%s: begin post section\n'
			'</file>\n'
			'</post>\n'
			'\n' %
			self.node.getFilename())
		self.startElementDefault(name, attrs)

	def endElement_post(self, name):
		self.endElementDefault(name)
		self.xml.append('\n'
			'<post>\n'
			'<file name="/var/log/rocks-install.log" mode="append">\n'
			'%s: end post section\n'
			'</file>\n'
			'</post>\n'
			'\n' %
			self.node.getFilename())

	# <*>

	def startElementDefault(self, name, attrs):
		s = ''
		for attrName in attrs.getNames():
			if attrName not in [ 'roll', 'file' ]:
				attrValue = attrs.get(attrName)
				s += ' %s="%s"' % (attrName, attrValue)
		if not s:
			self.xml.append('<%s>' % name)
		else:
			self.xml.append('<%s %s>' % (name, s))
		
	def endElementDefault(self, name):
		self.xml.append('</%s>' % name)


		
	def startElement(self, name, attrs):
		try:
			func = getattr(self, "startElement_%s" % name)
		except AttributeError:
			self.startElementDefault(name, attrs)
			return
		func(name, attrs)


	def endElement(self, name):
		try:
			func = getattr(self, "endElement_%s" % name)
		except AttributeError:
			self.endElementDefault(name)
			return
		func(name)
		self.stripText = 0

	def characters(self, s):
		if self.stripText:
			return

		if self.evalShell:
			self.evalText.append(s)
		else:
			self.xml.append(saxutils.escape(s))
			
	def getXML(self):
		return self.getXMLHeader() + string.join(self.xml, '')


class Pass2NodeHandler(handler.ContentHandler,
	handler.DTDHandler,
	handler.EntityResolver,
	handler.ErrorHandler,
	AttributeHandler):

	"""Sax Parser for XML before it is written to stdout.
	All generated XML is filtered through this to append the file and
	roll attributes to all tags.  The includes tags generated from eval
	and include sections."""
		

	def __init__(self, node, attrs):
		handler.ContentHandler.__init__(self)
		self.setAttributes(attrs)
		self.node = node
		self.xml = []
		self.kstags  = {}
		self.kskey = None
		self.kstext = []

	def startElement(self, name, attrs):
		self.kstext = []
		
		if name == 'kickstart' or name == 'jumpstart':
			return
		
		if name in [ 'url', 'lang', 'keyboard', 'text', 'reboot' ]:
			self.kskey = name
		else:
			self.kskey = None
						
		s = ''
		for attrName in attrs.getNames():
			attrValue = attrs.get(attrName)
			s += ' %s="%s"' % (attrName, attrValue)
		if 'roll' not in attrs.getNames():
			s += ' roll="%s"' % self.node.getRoll()
		if 'file' not in attrs.getNames():
			s += ' file="%s"' % self.node.getFilename()
		self.xml.append('<%s%s>' % (name, s))
		
	def endElement(self, name):
		if name == 'kickstart' or name == 'jumpstart':
			return

		if self.kskey:
			self.kstags[self.kskey] = string.join(self.kstext, '')
			
		self.xml.append('</%s>' % name)

	def characters(self, s):
		self.kstext.append(s)
		self.xml.append(saxutils.escape(s))
		
	def getKSText(self):
		text = ''
		for key, val in self.kstags.items():
			text += '%s %s\n' % (key, val)
		return text
		
	def getXML(self):
		return string.join(self.xml, '')

	
				
				
class Node(rocks.graph.Node):

	def __init__(self, name):
		rocks.graph.Node.__init__(self, name)
		self.color	= 'black'
		self.fillColor	= 'white'
		self.shape	= 'ellipse'
		self.roll	= ''
		self.filename	= ''
		self.xml	= []
		self.kstext	= []

	def setColor(self, color):
		self.color = color

	def setFilename(self, filename):
		self.filename = filename
	
	def setFillColor(self, color):
		self.fillColor = color
		
	def setShape(self, shape):
		self.shape = shape

	def setRoll(self, name):
		self.roll = name
	
	def addKSText(self, text):
		self.kstext.append(text)
			
	def addXML(self, xml):
		self.xml.append(xml)
		
	def getFilename(self):
		return self.filename
		
	def getRoll(self):
		return self.roll

	def getXML(self):
		return string.join(self.xml, '')

	def getKSText(self):
		return string.join(self.kstext, '')

	def getDot(self, prefix='', namespace=''):
		attrs = 'style=filled '
		attrs = attrs + 'shape=%s '     % self.shape
		attrs = attrs + 'label="%s" '   % self.name
		attrs = attrs + 'fillcolor=%s ' % self.fillColor
		attrs = attrs + 'color=%s'      % self.color
		if namespace:
			name = '%s-%s' % (namespace, self.name)
		else:
			name = self.name
		return '%s"%s" [%s];' % (prefix, name, attrs)
		
	def drawDot(self, prefix=''):
		print self.getDot(prefix)
		

class Edge(rocks.graph.Edge):
	def __init__(self, a, b):
		rocks.graph.Edge.__init__(self, a, b)
		self.roll	= ''
		self.color	= 'black'
		self.style	= ''

	def setStyle(self, style):
		self.style = style
		
	def setColor(self, color):
		self.color = color

	def setRoll(self, name):
		self.roll = name
		
	def getRoll(self):
		return self.roll

		

class FrameworkEdge(Edge):
	def __init__(self, a, b):
		Edge.__init__(self, a, b)
		self.cond	= None

	def setConditional(self, cond):
		self.cond = cond
		
	def getConditional(self):
		return self.cond

	def getDot(self, prefix=''):
		attrs = ''
		attrs += 'style=%s ' % self.style
		attrs += 'color=%s ' % self.color

		if not self.cond:
			return '%s"%s" -> "%s" ' \
				'[%s arrowsize=1.5];' % (prefix,
				self.parent.name, self.child.name, attrs)

		list = [] 
		label = self.cond.replace('"', '\\"')
		list.append('%s"%s_%s_%s" '
			'[ shape=none label="%s" ];' %
			(prefix, self.parent.name, self.child.name,
			label, label))
		list.append('%s"%s" -> "%s_%s_%s" [%s arrowsize=0];' %
			(prefix, self.parent.name,
			self.parent.name, self.child.name, label,
			attrs))
		list.append('%s"%s_%s_%s" -> "%s" [%s arrowsize=1.5];' %
			(prefix,
			self.parent.name, self.child.name, label,
			self.child.name, attrs))
		return string.join(list, '\n')
					
	
	def drawDot(self, prefix=''):
		print self.getDot(prefix)
		


class OrderEdge(Edge):
	def __init__(self, head, tail, gen=None):
		Edge.__init__(self, head, tail)
		self.gen = gen

	def getGenerator(self):
		return self.gen

	def getDot(self, prefix='', namespace=''):
		attrs = ''
		attrs = attrs + 'style=%s ' % self.style
		attrs = attrs + 'color=%s ' % self.color
		attrs = attrs + 'arrowsize=1.5'
		if namespace:
			child  = '%s-%s' % (namespace, self.child.name)
			parent = '%s-%s' % (namespace, self.parent.name)
		else:
			child  = self.child.name
			parent = self.parent.name
		return '%s"%s" -> "%s" [%s];' % (prefix, parent, child, attrs)

	def drawDot(self, prefix=''):
		print self.getDot(prefix)
		


class FrameworkIterator(rocks.graph.GraphIterator):
	def __init__(self, graph):
		rocks.graph.GraphIterator.__init__(self, graph)
		self.nodes = {}

	def run(self, node):
		rocks.graph.GraphIterator.run(self, node)
		keys = self.nodes.keys()
		keys.sort()
		list = []
		for key in keys:
			list.append(self.nodes[key])
		return list
	
	def visitHandler(self, node, edge):
		rocks.graph.GraphIterator.visitHandler(self, node, edge)
		if edge:
			cond	= edge.getConditional()
		else:
			cond	= None
		self.nodes[node.name] = (node, cond)


class OrderIterator(rocks.graph.GraphIterator):
	def __init__(self, graph):
		rocks.graph.GraphIterator.__init__(self, graph)
		self.nodes = []
		self.mark  = {}

	def run(self):

		# First pass: Mark all nodes that have a path to HEAD.
		# We do this by reversing all edges in the graph, and
		# marking all nodes in HEAD's subtree.  Then for all
		# the unmarked nodes create an edge from HEAD to the
		# node.  This will force the HEAD node to be as close
		# as possible to the front of the topological order.

		self.nodes = []		# We don't really use these but we
		self.time  = 0		# might as well intialize them
		for node in self.graph.getNodes():
			self.mark[node] = 0
		self.graph.reverse()
		head = self.graph.getNode('HEAD')
		rocks.graph.GraphIterator.run(self, head)
		self.graph.reverse()	# restore edge order

		for node in self.graph.getNodes():
			if not self.mark[node] and node.getInDegree() == 0:
				self.graph.addEdge(OrderEdge(head, node))

		
		# Second pass: Mask all nodes reachable from TAIL.
		# Then for all the unmarked nodes create an edge from
		# TAIL to the node.  This will force TAIL to be as
		# close as possible to the end of the topological
		# order.

		self.nodes = []		# We don't really use these but we
		self.time  = 0		# might as well intialize them
		for node in self.graph.getNodes():
			self.mark[node] = 0
		tail = self.graph.getNode('TAIL')
		rocks.graph.GraphIterator.run(self, tail)

		for node in self.graph.getNodes():
			if not self.mark[node] and node.getOutDegree() == 0:
				self.graph.addEdge(OrderEdge(node, tail))
		

		# Third pass: Traverse the entire graph and compute
		# the finishing times for each node.  The reverse sort
		# of the finishing times produces the topological
		# ordering of the graph.  This ordered list of nodes
		# satisifies all of the dependency edges.
		
		self.nodes = []
		self.time  = 0
		rocks.graph.GraphIterator.run(self)

		list = []
		self.nodes.sort()
		for rank, node, gen in self.nodes:
			list.append((node, gen))
		list.reverse()

		return list


	def visitHandler(self, node, edge):
		rocks.graph.GraphIterator.visitHandler(self, node, edge)
		self.mark[node] = 1
		self.time = self.time + 1

	def finishHandler(self, node, edge):
		rocks.graph.GraphIterator.finishHandler(self, node, edge)
		self.time = self.time + 1
		if edge:
			gen = edge.getGenerator()
		else:
			gen = None
		self.nodes.append((self.time, node, gen))

