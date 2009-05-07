# $Id: __init__.py,v 1.44 2009/05/07 01:06:41 mjk Exp $
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
# $Log: __init__.py,v $
# Revision 1.44  2009/05/07 01:06:41  mjk
# Bug Fix
#
# A failed edge conditional with a passed ordering included the node.
# Fix was to make sure the nodeHash is either missing the node in the first
# place (previous code) OR the value is None, meaning it failed the
# conditional test.  We've had this bug for years!
#
# Anoop found the bug but I still have CVS access
#
# Revision 1.43  2009/05/01 19:06:59  mjk
# chimi con queso
#
# Revision 1.42  2009/03/21 22:22:55  bruno
#  - lights-out install of VM frontends with new node_rolls table
#  - nuked 'site' columns and tables from database
#  - worked through some bugs regarding entities
#
# Revision 1.41  2009/03/19 21:37:02  mjk
# attrs can also be the pathname of the site.attrs file
#
# Revision 1.40  2009/03/06 22:34:16  mjk
# - added roll argument to list.host.xml and list.node.xml
# - kroll is dead, added run.roll
#
# Revision 1.39  2009/03/04 01:32:13  bruno
# attributes work for frontend installs
#
# Revision 1.38  2009/03/04 00:18:00  mjk
# default to localhost os and arch
#
# Revision 1.37  2009/03/03 20:45:28  bruno
# gooder english
#
# Revision 1.36  2009/02/10 20:11:20  mjk
# os attr stuff for anoop
#
# Revision 1.35  2009/01/24 00:44:22  mjk
# fix hostname
#
# Revision 1.34  2009/01/23 23:46:51  mjk
# - continue to kill off the var tag
# - can build xml and kickstart files for compute nodes (might even work)
#
# Revision 1.33  2009/01/08 23:36:01  mjk
# - rsh edge is conditional (no more uncomment crap)
# - add global_attribute commands (list, set, remove, dump)
# - attributes are XML entities for kpp pass (both pass1 and pass2)
# - attributes are XML entities for kgen pass (not used right now - may go away)
# - some node are now interface=public
#
# Revision 1.32  2009/01/08 01:20:57  bruno
# for anoop
#
# Revision 1.31  2009/01/06 21:07:57  mjk
# *** empty log message ***
#
# Revision 1.30  2008/12/23 00:14:05  mjk
# - moved build and eval of cond strings into cond.py
# - added dump appliance,host attrs (and plugins)
# - cond values are typed (bool, int, float, string)
# - everything works for client nodes
# - random 80 col fixes in code (and CVS logs)
#
# Revision 1.29  2008/12/22 23:50:24  bruno
# change 4 quotes to 3.
#
# Revision 1.28  2008/12/20 01:06:15  mjk
# - added appliance_attributes
# - attributes => node_attributes
# - rocks set,list,remove appliance attr
# - eval shell for conds has a special local dictionary that allows
#   unresolved variables (attributes) to evaluate to None
# - need to add this to solaris
# - need to move UserDict stuff into pylib and remove cut/paste code
# - need a drink
#
# Revision 1.27  2008/12/19 21:08:54  mjk
# - solaris jgen code looks more like linux kgen code now
# - removed solaris <part> tag (outside of <main> section)
# - everything using cond now (arch,os are converted)
# - cond now works inside node files also
# - conditional edges work on linux, needs testing on solaris
#
# Revision 1.26  2008/10/18 00:55:54  mjk
# copyright 5.1
#
# Revision 1.25  2008/05/22 21:02:06  bruno
# rocks-dist is dead!
#
# moved default location of distro from /export/home/install to
# /export/rocks/install
#
# Revision 1.24  2008/03/06 23:41:38  mjk
# copyright storm on
#
# Revision 1.23  2007/12/20 21:39:12  anoop
# Added support for automatically choosing the correct node xml file depending
# on the platform on which we're running. On linux, the normal files are
# chosen, and on Solaris sol_<nodename>.xml file is chosen if it exists.
#
# This should eventually go away once the rocks graph is merged.
#
# Revision 1.22  2007/11/27 01:27:50  anoop
# Added support for os attribute to graph and node XML files.
#
# Revision 1.21  2007/11/09 00:04:54  anoop
# Made hostname and host ip address variables more sane. Now retrieves
# these values from database or site.xml, and won't just blindly default
# to 127.0.0.1 and 'None'
#
# Revision 1.20  2007/09/28 19:41:56  anoop
# More bug fixes. The "rocks list node xml" is the only command that needs to
# be run with data from either the database or /tmp/site.xml. The "rocks list
# host profile" command that produces the actual kickstart file can be run
# with the output of "rocks list node xml" command. It does not require the
# presence of a database.
#
# Revision 1.19  2007/09/28 18:51:46  anoop
# Adapting command line utils to run when no database is present. The only
# identifiable one at the moment is to be able to run "list node xml" command
# without the database
#
# Revision 1.18  2007/09/08 06:42:39  anoop
# Added ability for commands to accept the os=something option
#
# Revision 1.17  2007/08/14 20:14:23  anoop
# Fitting pylib and the command line with solaris
# mechs
#
# Revision 1.16  2007/07/05 17:46:45  bruno
# fixes
#
# Revision 1.15  2007/07/04 01:47:38  mjk
# embrace the anger
#
# Revision 1.14  2007/06/28 20:24:02  bruno
# cleanup a big 'um
#
# Revision 1.13  2007/06/19 16:42:42  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.12  2007/06/07 21:23:05  mjk
# - command derive from verb.command class
# - default is MustBeRoot
# - list.command / dump.command set MustBeRoot = 0
# - removed plugin non-bugfix
#
# Revision 1.11  2007/05/31 19:35:43  bruno
# first pass at getting all the 'help' consistent on all the rocks commands
#
# Revision 1.10  2007/05/10 20:37:01  mjk
# - massive rocks-command changes
# -- list host is standardized
# -- usage simpler
# -- help is the docstring
# -- host groups and select statements
# - added viz commands
#
# Revision 1.9  2007/04/27 23:50:37  anoop
# Basedir can be set dynamically
#
# Revision 1.8  2007/03/28 22:33:50  mjk
# - add getHostname() method to base command class
# - fix bad try block for default args in list.node.xml
# - list.node.xml works as standalone
#
# Revision 1.7  2007/03/02 01:14:38  mjk
# fix node specific app_globals
#
# Revision 1.6  2007/02/28 03:06:28  mjk
# - "rocks list host xml" replaces kpp
# - kickstart.cgi uses "rocks list host xml"
# - indirects in node xml now works
#
# Revision 1.5  2007/02/27 21:23:53  mjk
# checkpoint
#
# Revision 1.4  2007/02/27 01:53:58  mjk
# - run(self, args) => run(self, flags, args)
# - replaced rocks list host xml with more complete code
# - replaced rocks lust node xml with kpp shell (not a command now)
#
#
# 	Reset code to snapshot of kpp.py (minus non-app objects)


import os
import sys
import string
import socket
import rocks
import rocks.profile
import rocks.commands
from xml.sax import saxutils
from xml.sax import handler
from xml.sax import make_parser

class Command(rocks.commands.list.command):
	"""
	Lists the XML configuration information for a host. The graph
	traversal for the XML output is rooted at the XML node file
	specified by the 'node' argument. This command executes the first
	pre-processor pass on the configuration graph, performs all
	variable substitutions, and runs all eval sections.

	<arg type='string' name='node'>
	The XML node file that the graph traversal will begin. This should be
	the basename of the XML file (e.g., 'compute' and not 'compute.xml').
	</arg>

	<param type='string' name='arch'>
	Traverse the graph with the 'arch' parameter set to 
	the supplied value. If not specified, then 'arch' defaults to this
	host's architecture.
	</param>

	<param type='string' name='attrs'>
	A list of attributes. This list must be in python dictionary form,
	e.g., attrs="{ 'os': 'linux', 'arch' : 'x86_64' }"
	</param>

	<param type='string' name='host'>
	Primary name of host. If not supplied, then the name of
	this host is used.
	</param>

	<param type='string' name='addr'>
	Primary address of host. If not supplied, then the loopback
	IP address is used.
	</param>

	<param type='string' name='graph'>
	Name of the graph to traverse. If not supplied, then the
	graph named 'default' is traversed.
	</param>

	<param type='string' name='dist'>
	Name of the distribution. If not supplied, then the
	distribution named 'rocks-dist' is used.
	</param>

	<param type='string' name='roll'>
	If set, only expand nodes from the named roll. If not
	supplied, then the all rolls are used.
	</param>

	<param type='bool' name='eval'>
	If set to 'no', then don't execute eval sections. If not
	supplied, then execute all eval sections.
	</param>

	<param type='bool' name='missing-check'>
	If set to 'no', then disable errors regarding missing nodes.
	If not supplied, then print messages about missing nodes.
	</param>

	<param type='string' name='gen'>
	If set, the use the supplied argument as the program for the
	2nd pass generator. If not supplied, then use 'kgen'.
	</param>

	<param type='string' name='basedir'>
	If specified, the location of the XML node files.
	</param>
	
	<example cmd='list node xml compute'>
	Generate the XML graph starting at the XML node named 'compute.xml'.
	</example>
	"""

	def run(self, params, args):

		(attributes, rolls, evalp, missing, 
			generator, basedir) = self.fillParams(
			[('attrs', ),
			('roll', ),
			('eval', 'yes'),
			('missing-check', 'no'),
			('gen', 'kgen'),
			('basedir', )
			])
			
		if rolls:
			rolls = rolls.split(',')

		if attributes:
			try:
				attrs = eval(attributes)
			except:
				attrs = {}
				if os.path.exists(attributes):
					file = open(attributes, 'r')
					for line in file.readlines():
						l = line.split(':', 1)
						if len(l) == 2:
							#
							# key/value pairs
							#
							attrs[l[0].strip()] = \
								l[1].strip()
				file.close()
		else:
			attrs = {}

		if 'os' not in attrs:
			attrs['os'] = self.os

		if 'arch' not in attrs:
			attrs['arch'] = self.arch
			
		if 'hostname' not in attrs:
			attrs['hostname'] = self.db.getHostname()

		if 'graph' not in attrs:
			attrs['graph'] = 'default'
			
		if 'distribution' not in attrs:
			attrs['distribution'] = 'rocks-dist'
			
		if 'membership' not in attrs:
			attrs['membership'] = 'Frontend'
	
		if len(args) != 1:
			self.abort('must supply an XML node name')
		root = args[0]

		doEval = self.str2bool(evalp)
		allowMissing = self.str2bool(missing)

		if attrs['os'] == 'sunos':
			starter_tag = "jumpstart"
		else:
			starter_tag = "kickstart"


		# Add more values to the attributes
		attrs['version'] = rocks.version
		attrs['release'] = rocks.release
		attrs['root']	 = root
		
		kickstart_dir = self.command('report.distro').strip()

		if not basedir:
			os.chdir(os.path.join(os.sep, kickstart_dir,
				attrs['distribution'], attrs['arch'],
				'build'))
		else:
			os.chdir(basedir)

		# Parse the XML graph files in the chosen directory

		parser  = make_parser()
		handler = rocks.profile.GraphHandler(attrs)

		graphDir = os.path.join('graphs', attrs['graph'])
		if not os.path.exists(graphDir):
			print 'error - no such graph', graphDir
			sys.exit(-1)

		for file in os.listdir(graphDir):
			base, ext = os.path.splitext(file)
			if ext == '.xml':
				path = os.path.join(graphDir, file)
				fin = open(path, 'r')
				parser.setContentHandler(handler)
				parser.parse(fin)
				fin.close()

		graph = handler.getMainGraph()
		if graph.hasNode(root):
			root = graph.getNode(root)
		else:
			print 'error - node %s in not in graph' % root
			sys.exit(-1)
				
		nodes = rocks.profile.FrameworkIterator(graph).run(root)
		deps  = rocks.profile.OrderIterator\
			(handler.getOrderGraph()).run()

		# Initialize the hash table for the framework
		# nodes, and filter out everyone not for our
		# architecture and release.
		#
		# Now test for arbitrary conditionals (cond tag),
		# old arch,os test are part of this now are still supported
		
		nodesHash = {}
		for node,cond in nodes:
			nodesHash[node.name] = node
			if not rocks.cond.EvalCondExpr(cond, attrs):
				nodesHash[node.name] = None
			

		# Initialize the hash table for the dependency
		# nodes, and filter out everyone not for our
		# generator type (e.g. 'kgen').

		depsHash = {}
		for node,gen in deps:
			depsHash[node.name] = node
			if gen not in [ None, generator ]:
				depsHash[node.name] = None

		for dep,gen in deps:
			if not nodesHash.get(dep.name):
				depsHash[dep.name] = None

		for node,cond in nodes:
			if depsHash.has_key(node.name):
				nodesHash[node.name] = None

		list = []
		for dep,gen in deps:
			if dep.name == 'TAIL':
				for node,cond in nodes:
					list.append(nodesHash[node.
							      name])
			else:
				list.append(depsHash[dep.name])

		# if there was not a 'TAIL' tag, then add the
		# the nodes to the list here

		for node,cond in nodes:
			if nodesHash[node.name] not in list:
				list.append(nodesHash[node.name])

		# Iterate over the nodes and parse everyone we need
		# to parse.
		
		parsed = []
		kstext = ''
		for node in list:
			if not node:
				continue

			# When building rolls allowMissing=1 and
			# doEval=0.  This is setup by rollRPMS.py

			if allowMissing:
				try:
					handler.parseNode(node, doEval)
				except rocks.util.KickstartNodeError:
					pass
			else:
				handler.parseNode(node, doEval)
				parsed.append(node)
				kstext += node.getKSText()

		# Now print everyone out with the header kstext from
		# the previously parsed nodes

		self.addText('<?xml version="1.0" standalone="no"?>\n')
		self.addText('<!DOCTYPE rocks-graph [\n')
		for (k, v) in attrs.items():
			self.addText('\t<!ENTITY %s "%s">\n' % (k, v))
		self.addText(']>\n')
		d = {}
		for key in attrs.keys():
			d[key] = '&%s;' % key
		self.addText('<%s attrs="%s">\n' % (starter_tag, d))
		if attrs['os'] == 'linux':
			self.addText('<loader>\n')
			self.addText('%s\n' % saxutils.escape(kstext))
			self.addText('%kgen\n')
			self.addText('</loader>\n')

		for node in parsed:

			# If we are only expanding a roll subgraph
			# then do not ouput the XML for other nodes
				
			if rolls and node.getRoll() not in rolls:
				continue
				
			try:
				self.addText('%s\n' % node.getXML())
			except Exception, msg:
				raise rocks.util.KickstartNodeError, \
				      "in %s node: %s" \
				      % (node, msg)
		self.addText('</%s>\n' % starter_tag)
		
		

