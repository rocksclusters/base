# $Id: __init__.py,v 1.27 2008/12/19 21:08:54 mjk Exp $
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

	def checkConditional(self, attrs, cond):
		if not cond:
			return True
		for (k,v) in attrs.items():
			exec('%s="%s"' % (k,v))
		return eval(cond)
	
	def run(self, params, args):

		if len(args) != 1:
			self.abort('must supply an XML node name')
		root = args[0]

		if params.has_key('os'):
			self.os = params['os']
		if self.db:
			hostname = self.db.getHostname()
		else:
			hostname = 'None'
		if params.has_key('host'):
			hostname = params['host']
			
		if hostname == 'None':
			address = '127.0.0.1'
		else:
			self.db.execute('select ip from networks where name="%s"' % hostname)
			address, = self.db.fetchone()
		

		(arch, host, addr, graph, dist, roll, eval, missing, 
			generator, basedir) = self.fillParams(
			[('arch', self.arch),
			('host', hostname),
			('addr', address),
			('graph', 'default'),
			('dist', 'rocks-dist'),
			('roll', ),
			('eval', 'yes'),
			('missing-check', 'no'),
			('gen', 'kgen'),
			('basedir', )])

		doEval = self.str2bool(eval)
		allowMissing = self.str2bool(missing)


		if self.os == 'sunos':
			starter_tag = "jumpstart"
		else:
			starter_tag = "kickstart"
		# If we are connected to the database, generate the siteXML
		# using 'rocks list sitexml', otherwise use the file in
		# /tmp/site.xml.  The later case should only be run while
		# inside the installation environment (no database).
		# 
		# Once the siteXML has been populated feed it to the
		# SiteXMLHandler for parsing.  The result is the var
		# dictionary get populated from the siteXML
		
		if self.db:
			siteXML = self.command('list.host.sitexml', 
					[
				 	 host,
					 'os=%s' % self.os,
					])
		else:
			try:
				sitefile = 'site.xml'
				fin = open(os.path.join(os.sep, 
					'tmp', sitefile), 'r')
			except IOError:
				pass
			siteXML = fin.read()
			fin.close()

		var	= {}
		attrs   = {}
		parser	= make_parser()
		handler	= SiteXMLHandler(var)
		parser.setContentHandler(handler)
		parser.feed(siteXML)

		# Add more variable based on who this command was
		# called.

		if not self.db: # if we are inside the installer
			host = var['Kickstart_PrivateHostname']
			addr = var['Kickstart_PrivateAddress']
			membership = 'Frontend' # bad hardcoding here
			attrs['arch']		= arch    # no db
			attrs['os']		= self.os # min stuff only
		else:
			self.db.execute('select memberships.name from '
				'nodes,memberships where '
				'nodes.name="%s" and '
				'nodes.membership=memberships.id' % host)
			membership, = self.db.fetchone()
			
			# read the attributes into a dictionary to handle
			# the conditional edges (cond tag)
			
			self.db.execute("""select a.attr, a.value from
				attributes a, nodes n where
				n.name='%s' and n.id=a.node""" % host)
			for (a, v) in self.db.fetchall():
				attrs[a] = v

		var['Node_Root']	 = root
		var['Node_Hostname']     = host
		var['Node_Address']      = addr
		var['Node_Membership']   = membership
		var['Node_Distribution'] = os.path.join(dist, arch)
		var['Node_DistName']     = dist
		var['Node_Architecture'] = attrs['arch']
		var['Node_OS']		 = attrs['os']
		var['Info_RocksVersion'] = rocks.version
		var['Info_RocksRelease'] = rocks.release
	
		var['ROCKS_VARS_HOSTNAME'] = host
		os.putenv('ROCKS_VARS_HOSTNAME', host)

		# If environment variable exist of the form
		# Kickstart_<component> = <value> then override
		# the above and place into the var dictionary.

		for env in os.environ.keys():
			list = string.split(env, '_', 1)
			if len(list) == 2 and list[0] == 'Kickstart':
				var[env] = os.environ[env]
		if not self.db:
			kickstart_dir = 'install'
		else:
			kickstart_dir = self.command('report.distro').strip()

		if not basedir:
			os.chdir(os.path.join(os.sep, 'home', 
				kickstart_dir, dist, arch, 'build'))
		else:
			os.chdir(basedir)

		# Parse the XML graph files in the chosen directory

		parser  = make_parser()
		handler = rocks.profile.GraphHandler(var, self.os)

		graphDir = os.path.join('graphs', graph)
		if not os.path.exists(graphDir):
			print 'error - not such graph', graphDir
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
			if not self.checkConditional(attrs, cond):
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
			if not nodesHash.has_key(dep.name):
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
		self.addText('<%s attrs="%s">\n' % (starter_tag, attrs))
		if self.os != 'sunos':
			self.addText('<loader>\n')
			self.addText('%s\n' % saxutils.escape(kstext))
			self.addText('%kgen\n')
			self.addText('</loader>\n')

		for node in parsed:

			# If we are only expanding a roll subgraph
			# then do not ouput the XML for other nodes
				
			if roll and node.getRoll() != roll:
				continue
				
			try:
				self.addText('%s\n' % node.getXML())
			except Exception, msg:
				raise rocks.util.KickstartNodeError, \
				      "in %s node: %s" \
				      % (node, msg)
		self.addText('</%s>\n' % starter_tag)
		
		

class SiteXMLHandler(handler.ContentHandler,
	handler.DTDHandler,
	handler.EntityResolver,
	handler.ErrorHandler):

	def __init__(self, vars):
		handler.ContentHandler.__init__(self)
		self.vars = vars
	
	def startElement(self, name, attrs):
		if not name == 'var':
			return
			
		varName = attrs.get('name')
		varRef  = attrs.get('ref')
		varVal  = attrs.get('val')

		# Undo quoting from writeSiteVar() - dead code?
		varName = varName.replace("\\'","'")

		if varVal:
			varVal = varVal.replace("\\'","'")
			self.vars[varName] = varVal
		elif varRef:
			if self.vars.has_key(varRef):
				self.vars[varName] = self.vars[varRef]
			else:
				self.vars[varName] = ''

