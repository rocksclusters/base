# $Id: __init__.py,v 1.14 2009/03/21 22:22:55 bruno Exp $
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
# Revision 1.14  2009/03/21 22:22:55  bruno
#  - lights-out install of VM frontends with new node_rolls table
#  - nuked 'site' columns and tables from database
#  - worked through some bugs regarding entities
#
# Revision 1.13  2009/01/08 23:36:01  mjk
# - rsh edge is conditional (no more uncomment crap)
# - add global_attribute commands (list, set, remove, dump)
# - attributes are XML entities for kpp pass (both pass1 and pass2)
# - attributes are XML entities for kgen pass (not used right now - may go away)
# - some node are now interface=public
#
# Revision 1.12  2008/11/19 17:42:25  bruno
# fix (from long beach airport!)
#
# Revision 1.11  2008/10/18 00:55:50  mjk
# copyright 5.1
#
# Revision 1.10  2008/07/22 00:34:40  bruno
# first whack at vlan support
#
# Revision 1.9  2008/07/10 17:26:09  anoop
# Bug fix to support new distribution directory
#
# Revision 1.8  2008/03/06 23:41:37  mjk
# copyright storm on
#
# Revision 1.7  2007/07/05 17:46:45  bruno
# fixes
#
# Revision 1.6  2007/07/04 01:47:38  mjk
# embrace the anger
#
# Revision 1.5  2007/06/28 19:45:44  bruno
# all the 'rocks list host' commands now have help
#
# Revision 1.4  2007/06/19 16:42:41  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.3  2007/05/31 19:35:42  bruno
# first pass at getting all the 'help' consistent on all the rocks commands
#
# Revision 1.2  2007/05/30 20:15:41  anoop
# Modified to be able to get the graph of any roll individually,
# and not just the whole system
#
# Revision 1.1  2007/05/10 20:37:01  mjk
# - massive rocks-command changes
# -- list host is standardized
# -- usage simpler
# -- help is the docstring
# -- host groups and select statements
# - added viz commands
#
# Revision 1.5  2007/04/27 23:48:46  anoop
# Small changes to the rocks list graph command. 
# Now can support multiple graphs
# rather than just the default graph
#
# Revision 1.4  2007/04/24 17:58:09  bruno
# consist look and feel for all 'list' commands
#
# put partition commands under 'host'
#
# Revision 1.3  2007/01/17 02:11:40  anoop
# createEntitiesFromDB now replaced by getEntities()
# Minor correction for code that uses the database
#
# Revision 1.2  2007/01/12 22:54:54  anoop
# Some more cleanup. Now the commands that work properly are
#
# rocks list graph - lists the digraph from the root of the roll. 
#	more modifications
# 	coming, primarily argument parsing, for type of graph, orientation
# 	and size
#
# rocks list node xml - lists the xml tree rooted at the <root_node>
#
# All these use the self.addText command, rather than print.
#
# Removed the rocks list profile commands
#
# Revision 1.1  2007/01/12 20:20:06  anoop
# Added the command line:
# rocks list graph
#
# Revision 1.1  2007/01/11 23:25:37  anoop
# Baby steps to try and port kpp to the rocks command line.
# At the moment, a rather hacky way of doing things. A heck of a lot
# of cleanup is going to be necessary. (Apologies, if I hurt anyone's
# programming sensibilities)
#


import os
import sys
import string
import rocks.util
import rocks.profile
import rocks.graph
import rocks.file
import rocks.commands

from xml.sax import make_parser

class Command(rocks.commands.list.host.command):
	"""
	For each host, output a graphviz script to produce a diagram of the
	XML configuration graph. If no hosts are specified, a graph for every
	known host is listed.

	<arg optional='1' type='string' name='host' repeat='1'>
	Zero, one or more host names. If no host names are supplied, info about
	all the known hosts is listed.
	</arg>

	<param type='string' name='arch'>
	Optional. If specified, generate a graph for the specified CPU type.
	If not specified, then 'arch' defaults to this host's architecture.
	</param>

	<param type='string' name='basedir'>
	Optional. If specified, the location of the XML node files.
	</param>
	
	<example cmd='list host graph compute-0-0'>
	Generates a graph for compute-0-0
	</example>
	"""

	def run(self, params, args):
	
		# In the future we should store the ARCH in the database
		# and allow the cgi/url to override the default setting.
		# When this happens we can do a db lookup instead of using
		# a flag and defaulting to the host architecture.

		(arch, basedir) = self.fillParams(
			[('arch', self.arch),
			('basedir', )])

		self.beginOutput()
		
		self.drawOrder		= 0
		self.drawKey		= 1
		self.drawLandscape	= 0
		self.drawSize		= '10,10'
		
		for host in self.getHostnames(args):
			self.db.execute("""select d.name, a.graph from
				nodes n, memberships m, 
				distributions d, appliances a where
				n.membership=m.id and m.appliance=a.id and
				m.distribution=d.id and n.name='%s'""" % host)
			(dist, graph) = self.db.fetchone()

			distrodir = self.command('report.distro')
			
			self.basedir  = os.path.join(distrodir.strip(), dist,
				arch, 'build')
			if basedir:
				if not os.path.exists(basedir):
					self.abort('cannot read directory "%s"'
						% basedir)
				self.basedir = basedir

			graphdir = os.path.join(self.basedir, 'graphs', graph)
			if not os.path.exists(graphdir):
				self.abort('cannot read directory "%s"' %
					graphdir)

			parser  = make_parser()
			attrs = self.db.getHostAttrs(host)
			handler = rocks.profile.GraphHandler(attrs)

			for file in os.listdir(graphdir):
				root, ext = os.path.splitext(file)
				if ext == '.xml':
					path = os.path.join(graphdir, file)
					if not os.path.isfile(path):
						continue
					fin = open(path, 'r')
					parser.setContentHandler(handler)
					parser.parse(fin)
					fin.close()
			
			cwd = os.getcwd()
			os.chdir(self.basedir)
			dot = self.createDotGraph(handler,
				self.readDotGraphStyles())
			os.chdir(cwd)
			for line in dot:
				self.addOutput(host, line)

		self.endOutput(padChar='')
	
	
	def createDotGraph(self, handler, styleMap):
		dot = []
		dot.append('digraph rocks {')
		dot.append('\tsize="%s";' % self.drawSize)
		dot.append('\trankdir=LR;')

		# Key
		
		dot.append('\tsubgraph clusterkey {')
		dot.append('\t\tlabel="Rolls";')
		dot.append('\t\tfontsize=32;')
		dot.append('\t\tcolor=black;')
		for key in styleMap:
			a = 'style=filled '
			a += 'shape=%s '    % styleMap[key].nodeShape
			a += 'label="%s" ' % key
			a += 'fillcolor=%s' % styleMap[key].nodeColor
			dot.append('\t\t"roll-%s" [%s];' % (key, a))
		dot.append('\t}')

		# Ordering Graph
		
		dot.append('\tsubgraph clusterorder {')
		dot.append('\t\tlabel="Ordering Contraints";')
		dot.append('\t\tfontsize=32;')
		dot.append('\t\tcolor=black;')
		dict = {}
		for node in handler.getOrderGraph().getNodes():
			try:
				handler.parseNode(node, 0) # Skip <eval>
			except rocks.util.KickstartNodeError:
				pass
			try:
				color = styleMap[node.getRoll()].nodeColor
			except:
				color = 'white'
			node.setFillColor(color)
			dot.append(node.getDot('\t\t', 'order'))

		iter = rocks.profile.OrderIterator(handler.getOrderGraph())
		iter.run()

		for e in handler.getOrderGraph().getEdges():
			try:
				color = styleMap[e.getRoll()].edgeColor
				style = 'bold'
			except:
				color = 'black'
				style = 'invis'
			e.setColor(color)
			e.setStyle(style)
			dot.append(e.getDot('\t\t', 'order'))
		dot.append('\t}')

		# Main Graph

		dot.append('\tsubgraph clustermain {')
		dot.append('\t\tlabel="Profile Graph";')
		dot.append('\t\tfontsize=32;')
		dot.append('\t\tcolor=black;')
		for node in handler.getMainGraph().getNodes():
			try:
				handler.parseNode(node, 0) # Skip <eval>
			except rocks.util.KickstartNodeError:
				pass
			try:
				color = styleMap[node.getRoll()].nodeColor
			except:
				color = 'white'
			node.setFillColor(color)
			dot.append(node.getDot('\t\t'))
		for e in handler.getMainGraph().getEdges():
			try:
				color = styleMap[e.getRoll()].edgeColor
			except:
				color = 'black'
			e.setColor(color)
			e.setStyle('bold')
			dot.append(e.getDot('\t\t'))
		dot.append('\t}')

#		for mainNode in handler.getMainGraph().getNodes():
#			dot.append('"%s" -> "order-%s" [ style="invis"];' %
#				(mainNode.name,
#				 handler.getOrderGraph().getNode('HEAD')))


		dot.append('}')
		return dot


	def readDotGraphStyles(self):
		p   = make_parser()
		h   = rocks.profile.RollHandler()
		map = {}
		
		for file in os.listdir('.'):
			tokens = os.path.splitext(file)
			if len(tokens) != 2:
				continue
			name = tokens[0]
			ext  = tokens[1]
			tokens = string.split(name, '-')
			if len(tokens) < 2:
				continue
			prefix = tokens[0]
			if prefix == 'roll' and \
			   ext == '.xml' and \
			   os.path.isfile(file):
				fin = open(file, 'r')
				p.setContentHandler(h)
				p.parse(fin)
				fin.close()
				r = h.getRollName()
				map[r] = rocks.util.Struct()
				map[r].edgeColor = h.getEdgeColor()
				map[r].nodeColor = h.getNodeColor()
				map[r].nodeShape = h.getNodeShape()

		return map

