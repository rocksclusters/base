#! /opt/rocks/bin/python
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
# $Log: gen.py,v $
# Revision 1.71  2012/11/27 00:48:40  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.70  2012/05/06 05:48:47  phil
# Copyright Storm for Mamba
#
# Revision 1.69  2012/04/12 05:36:21  phil
# mv the chmod when creating a file
#
# Revision 1.68  2011/11/02 05:08:56  phil
# First take on bootstrap0. Packages, command line and processing to
# bring up the rocks database on a non-Rocks installed host.
# Also reworked generation of post sections to work more like Solaris:
# Each post section now creates a shell script with the desired interpreter.
# Report post command creates a shell script from the post section of a
# (set of) node xml files.
#
# Revision 1.67  2011/07/23 02:30:49  phil
# Viper Copyright
#
# Revision 1.66  2010/11/28 00:32:44  anoop
# Add the auto_reg keyword to jumpstart sysidcfg
#
# Revision 1.65  2010/09/07 23:53:08  bruno
# star power for gb
#
# Revision 1.64  2010/08/19 17:15:58  bruno
# f'ed by the katz!
#
# Revision 1.63  2010/08/09 22:58:13  mjk
# BUG:
#
# In the following code snippet, the file permissions set in the first "<file>" tag will not be preserved (the second <file> tag clears the permissions):
#
# <file name="/tmp/a" perms="0755">
# first line
# </file>
#
# <file name="/tmp/a" mode="append">
# second line
# </file>
#
# FIX: Revert to the previous perms and owner settings for all file tags
# that do not specify these optional attributes.
#
# Revision 1.62  2010/07/27 20:22:21  anoop
# Bug fixes
# - Jumpstart generation needs to recognize new tags to parse networking
#   information
# - Syntax error fixes
#
# Revision 1.61  2010/07/07 02:02:13  anoop
# file tag needs to support "os" conditionals. Since file tag
# is not subject to node filter attribute check, "os" conditional
# needs to be checked explicitly for the file tag
#
# Revision 1.60  2010/06/10 19:59:25  mjk
# <pre> handles interpreter attribute same as <post>
#
# Revision 1.59  2009/08/25 21:45:51  anoop
# More patching support for Solaris.
#   - support for including patches during creation of Rolls
#   - support for parsing <patch> tags
#   - support for contrib patches
#
# Revision 1.58  2009/06/02 17:22:25  anoop
# use unix-generic options and not linux specific ones
#
# Revision 1.57  2009/05/21 21:15:59  bruno
# make sure only root can checkout files from RCS repositories created with
# the 'file' tag
#
# Revision 1.56  2009/05/19 21:57:17  anoop
# Use the "interpreter" attribute instead of arg="--interpreter"
#
# Revision 1.55  2009/05/09 23:00:55  mjk
# - added <boot> to list of processed tags (linux)
# - tested and works on viz roll
#
# Revision 1.54  2009/05/08 22:15:39  anoop
# Use the isMeta() function to determine meta packages in solaris
#
# Revision 1.53  2009/05/05 21:01:36  bruno
# better logging from post scripts
#
# Revision 1.52  2009/05/04 21:52:58  bruno
# nuke rocks-security
#
# Revision 1.51  2009/05/02 22:40:42  bruno
# fix
#
# Revision 1.50  2009/05/01 23:18:28  bruno
# change log file
#
# Revision 1.49  2009/05/01 23:07:37  bruno
# log output of pre and post scripts
#
# Revision 1.48  2009/05/01 19:07:08  mjk
# chimi con queso
#
# Revision 1.47  2009/04/28 19:48:54  mjk
# - better exception handling for generate_ lookups, don't catch f() throws
# - rocks-post ci/co stuff is being written again
#
# Revision 1.46  2009/04/28 18:49:37  mjk
# fix syntax errors
#
# Revision 1.45  2009/04/28 17:58:10  mjk
# - UNTESTED BEWARE
# - rcsFiles now tracks (owner, perms)
# - last ci/co (rcsEnd) lays down the correct ower and perms
# - list co is a "co -l"
#
# Revision 1.44  2009/04/27 18:03:34  bruno
# remove dead setRCS* and getRCS* functions
#
# Revision 1.43  2009/04/22 22:15:31  mjk
# - rcs co/ci is complete
# - first modification triggers a ci of the file
# - top of the boot-pre section ci/co all modified files
# - no ci/co nonsense in between the above events
# - boot pre/post files generated in /etc/sysconfig
# - still needs rc.d scripts to trigger everything
# - solaris?
#
# Revision 1.42  2009/04/22 21:30:54  mjk
# - new take on the rcs ci/co stuff
# - added <boot> section
# - not tested yet
#
# Revision 1.41  2009/04/20 21:57:51  bruno
# fix syntax error and stop all the ci/co stuff.
#
# Revision 1.40  2009/03/26 23:57:35  anoop
# Cleaned up finish script generation for Solaris
# Modified RCS support for Linux and Solaris by using
# gawk instead of awk, and full paths for "co" and "ci"
# commands
#
# Revision 1.39  2009/01/29 01:28:13  anoop
# Better support for package clusters in solaris
#
# Revision 1.38  2008/12/23 00:14:05  mjk
# - moved build and eval of cond strings into cond.py
# - added dump appliance,host attrs (and plugins)
# - cond values are typed (bool, int, float, string)
# - everything works for client nodes
# - random 80 col fixes in code (and CVS logs)
#
# Revision 1.37  2008/12/20 01:06:15  mjk
# - added appliance_attributes
# - attributes => node_attributes
# - rocks set,list,remove appliance attr
# - eval shell for conds has a special local dictionary that allows
#   unresolved variables (attributes) to evaluate to None
# - need to add this to solaris
# - need to move UserDict stuff into pylib and remove cut/paste code
# - need a drink
#
# Revision 1.36  2008/12/19 21:08:54  mjk
# - solaris jgen code looks more like linux kgen code now
# - removed solaris <part> tag (outside of <main> section)
# - everything using cond now (arch,os are converted)
# - cond now works inside node files also
# - conditional edges work on linux, needs testing on solaris
#
# Revision 1.35  2008/10/18 00:56:02  mjk
# copyright 5.1
#
# Revision 1.34  2008/08/07 19:35:28  bruno
# need to checkout the file and lock it, not just lock it
#
# Revision 1.33  2008/08/07 18:53:49  bruno
# simplified the RCS code for the file tag.
#
# Revision 1.32  2008/07/21 17:46:38  anoop
# Stupid bug fixed. Now sunos actually honor's the os attribute in
# the package and post tags
#
# Revision 1.31  2008/05/20 21:08:07  anoop
# Added '' to heredoc so that shell special chars don't get expanded
# before their time
#
# Revision 1.30  2008/05/20 01:08:38  anoop
# Modified gen.py to output service instance lines correctly. Now we can specify
# multiple instances of the same service. Affects Solaris only
#
# Revision 1.29  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.28  2008/02/21 19:48:51  bruno
# nuke dead flag
#
# Revision 1.27  2008/02/19 23:20:24  bruno
# katz made me do it.
#
# Revision 1.26  2007/12/10 21:28:35  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.25  2007/11/27 01:27:50  anoop
# Added support for os attribute to graph and node XML files.
#
# Revision 1.24  2007/10/31 00:07:46  anoop
# Added a handler for the service tag on Solaris.
#
# Revision 1.22  2007/09/28 05:02:30  anoop
# Reverting back to using the cluster keyword. For the time being decomposing
# packages to be able to use HTTP for installation does not work and is
# completely usesless. Will use this when the Solaris installer code is
# advanced
#
# Revision 1.21  2007/09/25 21:56:03  anoop
# Made the jumpstart config generator a bit more http aware. Still an ugly
# kludge that the Sun engineers should work on, to get native http support
# into pfinstall
#
# Revision 1.20  2007/09/24 23:22:36  anoop
# Minor modifications to the Solaris part when generating sysidcfg files
#
# Revision 1.19  2007/09/19 01:50:09  anoop
# Fixed minor bug
#
# Revision 1.18  2007/09/10 04:26:26  anoop
# SOLARIS: For pretty much everything that goes into sysidcfg strip out the
# whitespaces/newline/tab characters at the very beginning and end of the
# string.
#
# Revision 1.17  2007/09/09 01:11:17  anoop
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
# Revision 1.16  2007/09/04 19:00:16  anoop
# Makefile now dynamically changes the MySQL socket path during building the
# package on Solaris. On linux, it does not change the path.
#
# NOTE: rcs tags generation commented out for now. Must be re-enabled before
# release
# NOTE: Writing to /root/install.log commented out for now. Must be re-enabled
# before release
#
# Revision 1.15  2007/09/02 06:45:31  anoop
# The command line to generate the profile XML made a little more flexible.
# The all new Pylib - Now with more XML tags support!!!
#
# Revision 1.14  2007/08/15 18:36:20  anoop
# Minor bug fix
#
# Revision 1.13  2007/08/14 20:14:23  anoop
# Fitting pylib and the command line with solaris
# mechs
#
# Revision 1.12  2007/06/23 04:03:24  mjk
# mars hill copyright
#
# Revision 1.11  2006/09/11 22:47:23  mjk
# monkey face copyright
#
# Revision 1.10  2006/08/10 00:09:41  mjk
# 4.2 copyright
#
# Revision 1.9  2006/01/16 06:48:59  mjk
# fix python path for source built foundation python
#
# Revision 1.8  2005/10/12 18:08:42  mjk
# final copyright for 4.1
#
# Revision 1.7  2005/10/04 22:03:37  mjk
# force cvs co
#
# Revision 1.6  2005/09/16 01:02:21  mjk
# updated copyright
#
# Revision 1.5  2005/07/11 23:51:35  mjk
# use rocks version of python
#
# Revision 1.4  2005/05/24 21:21:57  mjk
# update copyright, release is not any closer
#
# Revision 1.3  2005/04/25 23:17:57  mjk
# lost file perms, put them back
#
# Revision 1.2  2005/04/22 23:43:51  mjk
# ntp fix
#
# Revision 1.1  2005/03/01 00:22:08  mjk
# moved to base roll
#
# Revision 1.13  2005/02/11 23:38:18  mjk
# - blow up the bridge
# - kgen and kroll do actually work (but kroll is not complete)
# - file,roll attrs added to all tags by kpp
# - gen has generator,nodefilter base classes
# - replaced rcs ci/co code with new stuff
# - very close to adding rolls on the fly
#
# Revision 1.12  2004/03/25 03:15:48  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.11  2003/08/20 22:07:04  mjk
# OO changes
#
# Revision 1.10  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.9  2003/08/15 18:31:59  mjk
# - Gave into FDS and put some formatting into ci/co "compiler output"
# - Some more arch fixes for rocks-dist
#
# Revision 1.8  2003/08/01 23:40:04  phil
# Changed my mind
#
# Revision 1.7  2003/08/01 23:27:23  phil
# Small change to rocksCheckin Function
#
# Revision 1.6  2003/07/28 19:36:07  phil
# typo.
#
# Revision 1.5  2003/07/28 19:35:14  phil
# changed matching logic for grep so that rocks checkin can
# be re-applied.
#
# Revision 1.4  2003/07/28 18:41:23  phil
# Essentially ... rewrote it.
#
# Revision 1.3  2003/07/23 00:42:14  phil
# make checkin_checkout return a string
#
# Revision 1.2  2003/07/23 00:25:22  phil
# Fixed up the revision tag naming scheme
#
# Revision 1.1  2003/07/22 23:41:34  phil
# Print out inline shell script that will checkin/checkout a
# config file into a local cvs repository
#
#
# Some basic utility functions that allows us to generate
# kickstart, cfengine, and tripwire files
#
 


import string
import types
import sys
import os
import tempfile
import time
import xml.dom.NodeFilter
import xml.dom.ext.reader.Sax2
import rocks.js
import rocks.cond
	
		

class NodeFilter(xml.dom.NodeFilter.NodeFilter):

	def __init__(self, attrs):
		self.attrs = attrs
                self.phases = set(['pre','post'])

	def set_phases(self, values):
		""" if reconfigure is set to true we are reconfiguring 
		if it is set to false we are installing""" 
		self.phases = set(values)

	def isCorrectCond(self, node):

		attr = node.attributes.getNamedItem((None, 'arch'))
		if attr:
			arch = attr.value
		else:
			arch = None

		attr = node.attributes.getNamedItem((None, 'os'))
		if attr:
			os = attr.value
		else:
			os = None

		attr = node.attributes.getNamedItem((None, 'release'))
		if attr:
			release = attr.value
		else:
			release = None

		attr = node.attributes.getNamedItem((None, 'cond'))
		if attr:
			cond = attr.value
		else:
			cond = None

		attr = node.attributes.getNamedItem((None, 'phase'))
		if attr :
			phaseVal = set(attr.value.split(','))
		else :
			# by default post section are install only
			phaseVal = set(["pre", "post"])

		if not phaseVal.intersection(self.phases):
			return False

		expr = rocks.cond.CreateCondExpr(arch, os, release, cond)
		return rocks.cond.EvalCondExpr(expr, self.attrs)

		
class Generator:
	"""Base class for various DOM based kickstart graph generators.
	The input to all Generators is assumed to be the XML output of KPP."""
	
	def __init__(self):
		self.attrs	= {}
		self.arch	= None
		self.rcsFiles	= {}

	def setArch(self, arch):
		self.arch = arch
		
	def getArch(self):
		return self.arch
	
	def setOS(self, osname):
		self.os = osname
		
	def getOS(self):
		return self.os

	def isDisabled(self, node):
		return node.attributes.getNamedItem((None, 'disable'))

	def isMeta(self, node):
		attr  = node.attributes
		type  = attr.getNamedItem((None, 'type'))
		if type:
			type = type.value
		else:
			type = 'rpm'
		if type  == 'meta':
			return 1
		return 0
	
	def rcsBegin(self, file, owner, perms):
		"""
		If the is the first time we've seen a file ci/co it.  Otherwise
		just track the ownership and perms from the <file> tag .
		"""
		
		rcsdir	= os.path.join(os.path.dirname(file), 'RCS')
		rcsfile = '%s,v' % os.path.join(rcsdir, os.path.basename(file))
		l	= []

		l.append('')

		if file not in self.rcsFiles:
			l.append('if [ ! -f %s ]; then' % rcsfile)
			l.append('\tif [ ! -f %s ]; then' % file)
			l.append('\t\ttouch %s;' % file)
			l.append('\tfi')
			l.append('\tif [ ! -d %s ]; then' % rcsdir)
			l.append('\t\tmkdir -m 700 %s' % rcsdir)
			l.append('\t\tchown 0:0 %s' % rcsdir)
		 	l.append('\tfi;')
			l.append('\techo "original" | /opt/rocks/bin/ci %s;' %
			 	file)
			l.append('\t/opt/rocks/bin/co -f -l %s;' % file)
			l.append('fi')

		# If this is a subsequent file tag and the optional PERMS
		# or OWNER attributes are missing, use the previous value(s).
		
		if self.rcsFiles.has_key(file):
			(orig_owner, orig_perms) = self.rcsFiles[file]
			if not perms:
				perms = orig_perms
			if not owner:
				owner = orig_owner

		self.rcsFiles[file] = (owner, perms)
		
		if owner:
			l.append('chown %s %s' % (owner, file))
			l.append('chown %s %s' % (owner, rcsfile))

		l.append('')

		return string.join(l, '\n')

	def rcsEnd(self, file, owner, perms):
		"""
		Run the final ci/co of a <file>.  The ownership of both the
		file and rcs file are changed to match the last requested
		owner in the file tag.  The perms of the file (not the file
		file) are also modified.

		The file is checked out locked, which is why we don't modify
		the perms of the RCS file itself.
		"""
		rcsdir	= os.path.join(os.path.dirname(file), 'RCS')
		rcsfile = '%s,v' % os.path.join(rcsdir, os.path.basename(file))
		l	= []

		l.append('')
		l.append('if [ -f %s ]; then' % file)
		l.append('\techo "rocks" | /opt/rocks/bin/ci %s;' % file)
		l.append('\t/opt/rocks/bin/co -f -l %s;' % file)
		l.append('fi')		

		if owner:
			l.append('chown %s %s' % (owner, file))
			l.append('chown %s %s' % (owner, rcsfile))

		if perms:
			l.append('chmod %s %s' % (perms, file))

		return string.join(l, '\n')

	
	def order(self, node):
		"""
		Stores the order of traversal of the nodes
		Useful for debugging.
		"""
		attr = node.attributes
		
		if attr.getNamedItem((None, 'file')):
			file = attr.getNamedItem((None, 'file')).value
		else:
			file = ''
		if attr.getNamedItem((None, 'roll')):
			roll = attr.getNamedItem((None, 'roll')).value
		else:
			roll = ''
			
		if (file,roll) not in self.ks['order']:
			self.ks['order'].append((file,roll))
		
	def handle_mainChild(self, node):
		try:
			eval('self.handle_main_%s(node)' % node.nodeName)
		except AttributeError:
			self.ks['main'].append('%s %s' % (node.nodeName,
				self.getChildText(node)))

		
	def parseFile(self, node):
		attr = node.attributes

		if attr.getNamedItem((None, 'os')):
			os = attr.getNamedItem((None, 'os')).value
			if os != self.getOS():
				return ''

		if attr.getNamedItem((None, 'name')):
			fileName = attr.getNamedItem((None, 'name')).value
		else:
			fileName = ''

		if attr.getNamedItem((None, 'mode')):
			fileMode = attr.getNamedItem((None, 'mode')).value
		else:
			fileMode = 'create'

		if attr.getNamedItem((None, 'owner')):
			fileOwner = attr.getNamedItem((None, 'owner')).value
		else:
			fileOwner = ''

		if attr.getNamedItem((None, 'perms')):
			filePerms = attr.getNamedItem((None, 'perms')).value
		else:
			filePerms = ''

		if attr.getNamedItem((None, 'vars')):
			fileQuoting = attr.getNamedItem((None, 'vars')).value
		else:
			fileQuoting = 'literal'

		if attr.getNamedItem((None, 'expr')):
			fileCommand = attr.getNamedItem((None, 'expr')).value
		else:
			fileCommand = None

		fileText = self.getChildText(node)

		if fileName:
		
			s = self.rcsBegin(fileName, fileOwner, filePerms)

			if fileMode == 'append':
				gt = '>>'
			else:
				gt = '>'

			if fileCommand:
				s += '%s %s %s\n' % (fileCommand, gt, fileName)
			if not fileText:
				s += 'touch %s\n' % fileName
			else:
				if fileQuoting == 'expanded':
					eof = "EOF"
				else:
					eof = "'EOF'"

				s += "cat %s %s << %s" % (gt, fileName, eof)
				if fileText[0] != '\n':
					s += '\n'
				s += fileText
				if fileText[-1] != '\n':
					s += '\n'
				s += 'EOF\n'

			if filePerms:
				s += 'chmod %s %s' % (filePerms, fileName)

		return s
	
	# <*>
	#	<*> - tags that can go inside any other tags
	# </*>

	def getChildText(self, node):
		text = ''
		for child in node.childNodes:
			if child.nodeType == child.TEXT_NODE:
				text += child.nodeValue
			elif child.nodeType == child.ELEMENT_NODE:
				text += eval('self.handle_child_%s(child)' \
					% (child.nodeName))
		return text

	
	# <*>
	#	<file>
	# </*>
	
	def handle_child_file(self, node):
		return self.parseFile(node)

	##
	## Generator Section
	##
			
	def generate(self, section):
		"""Dump the requested section of the kickstart file.  If none 
		exists do nothing."""
		list = []
		try:
			f = getattr(self, "generate_%s" % section)
		except AttributeError:
			f = None
		if f:
			list += f()
		return list
		
	def generate_order(self):
		list = []
		list.append('#')
		list.append('# Node Traversal Order')
		list.append('#')
		for (line,roll) in self.ks['order']:
			if roll:
				list.append('# %s (%s)' % (line, roll))
			else:
				list.append('# %s' % (line))
		list.append('#')
		return list

	def generate_debug(self):
		list = []
		list.append('#')
		list.append('# Debugging Information')
		list.append('#')
		for text in self.ks['debug']:
			for line in string.split(text, '\n'):
				list.append('# %s' % line)
		list.append('#')
		return list
			


class MainNodeFilter_linux(NodeFilter):

	def acceptNode(self, node):
	
		if node.nodeName == 'kickstart':
			return self.FILTER_ACCEPT
				
		if node.nodeName not in [
			'include',
			'main',
			'auth',
			'clearpart',
			'device',
			'driverdisk',
			'install',
			'nfs',
			'cdrom',
			'interactive',
			'harddrive',
			'url',
			'keyboard',
			'lang',
			'langsupport',
			'lilo',
			'lilocheck',
			'bootloader',
			'mouse',
			'network',
			'part',
			'volgroup',
			'logvol',
			'raid',
			'reboot',
			'rootpw',
			'skipx',
			'text',
			'timezone',
			'upgrade',
			'xconfig',
			'zerombr'
			]:
			return self.FILTER_SKIP

		if not self.isCorrectCond(node):
			return self.FILTER_SKIP

		return self.FILTER_ACCEPT


class OtherNodeFilter_linux(NodeFilter):
	def acceptNode(self, node):

		if node.nodeName == 'kickstart':
			return self.FILTER_ACCEPT
			
		if node.nodeName not in [
			'attributes', 
			'debug',
			'description',
			'package',
			'pre', 
			'post',
			'boot',
			'configure'
			]:
			return self.FILTER_SKIP
			
		if not self.isCorrectCond(node):
			return self.FILTER_SKIP

		return self.FILTER_ACCEPT


class Generator_linux(Generator):

	def __init__(self):
		Generator.__init__(self)	
		self.ks                 = {}
		self.ks['order']	= []
		self.ks['debug']	= []
		self.ks['main']         = []
		self.ks['rpms-on']	= []
		self.ks['rpms-off']	= []
		self.ks['pre' ]         = []
		self.ks['post']         = []
		self.ks['boot-pre']	= []
		self.ks['boot-post']	= []

		self.phases		= ['post', 'pre']

		self.log = '/mnt/sysimage/var/log/rocks-install.log'


	def set_phases(self, values):
		""" this is a list of string containing the phases that will be generated by the 
		generator. Default is 'post' and 'pre' aka the kickstart """
		self.phases = values
	
	##
	## Parsing Section
	##
	
	def parse(self, xml_string):
		import cStringIO
		xml_buf = cStringIO.StringIO(xml_string)
		doc = xml.dom.ext.reader.Sax2.FromXmlStream(xml_buf)
		filter = MainNodeFilter_linux(self.attrs)
		iter = doc.createTreeWalker(doc, filter.SHOW_ELEMENT,
			filter, 0)
		node = iter.nextNode()
		
		while node:
			if node.nodeName == 'kickstart':
				self.handle_kickstart(node)
			elif node.nodeName == 'main':
				child = iter.firstChild()
				while child:
					self.handle_mainChild(child)
					child = iter.nextSibling()

			node = iter.nextNode()
			
		filter = OtherNodeFilter_linux(self.attrs)
		filter.set_phases(self.phases)
		iter = doc.createTreeWalker(doc, filter.SHOW_ELEMENT,
			filter, 0)
		node = iter.nextNode()
		while node:
			if node.nodeName != 'kickstart':
				self.order(node)
				eval('self.handle_%s(node)' % (node.nodeName))
			node = iter.nextNode()


	# <kickstart>
	
	def handle_kickstart(self, node):
		# pull out the attr to handle generic conditionals
		# this replaces the old arch/os logic but still
		# supports the old syntax

		if node.attributes:
			attrs = node.attributes.getNamedItem((None, 'attrs'))
			if attrs:
				dict = eval(attrs.value)
				for (k,v) in dict.items():
					self.attrs[k] = v
		
	# <main>
	#	<clearpart>
	# </main>
	
	def handle_main_clearpart(self, node):
		attr = node.attributes
		if attr.getNamedItem((None, 'partition')):
			arg = attr.getNamedItem((None, 'partition')).value
		else:
			arg = ''

		#
		# the web form sets the environment variable 'partition'
		# (although, we may find that it makes sense for other
		# sources to set it too).
		#
		try:
			os_arg = os.environ['partition']
		except:
			os_arg = ''

		clearpart = self.getChildText(node)

		if (arg == '') or (os_arg == '') or (arg == os_arg):
			self.ks['main'].append('clearpart %s' % clearpart)

	
	# <main>
	#	<lilo>
	# </main>
	
	def handle_main_lilo(self, node):
		self.ks['main'].append('bootloader %s' %
			self.getChildText(node))
		return


	# <main>
	#	<bootloader>
	# </main>

	def handle_main_bootloader(self, node):
		self.ks['main'].append('bootloader %s' % 
			self.getChildText(node))
		return

	# <main>
	#	<lang>
	# </main>

	def handle_main_lang(self, node):
		self.ks['main'].append('lang %s' % 
			self.getChildText(node))
		return

	# <main>
	#	<langsupport>
	# </main>

	def handle_main_langsupport(self, node):
		self.ks['main'].append('langsupport --default=%s' %
			self.getChildText(node).strip())

		return

	# <main>
	#	<volgroup>
	# </main>

	def handle_main_volgroup(self, node):
		self.ks['main'].append('volgroup %s' % 
			self.getChildText(node))
		return

	# <main>
	#	<logvol>
	# </main>

	def handle_main_logvol(self, node):
		self.ks['main'].append('logvol %s' % 
			self.getChildText(node))
		return

	# <debug>
	
	def handle_debug(self, node):
		self.ks['debug'].append(self.getChildText(node))
	
	# <description>
	
	def handle_description(self, node):
	 	dummy=self.getChildText(node)

	
	# <package>
		
	def handle_package(self, node):
		rpm = self.getChildText(node).strip()

		if self.isDisabled(node):
			key = 'rpms-off'
		else:
			key = 'rpms-on'

		if self.isMeta(node):
			rpm = '@' + rpm	


		# if the RPM is to be turned off, only add if it is not 
		# in the on list.

		if key == 'rpms-off':
			if rpm not in self.ks['rpms-on']:
				self.ks[key].append(rpm)

		# if RPM is turned on, make sure it is not in the off list

		if key == 'rpms-on':
			self.ks[key].append(rpm)

			if rpm in self.ks['rpms-off']:
				self.ks['rpms-off'].remove(rpm)
						

	# <pre>
	
	def handle_pre(self, node):
		attr = node.attributes
		# Parse the interpreter attribute
		if attr.getNamedItem((None, 'interpreter')):
			interpreter = '--interpreter ' + \
				attr.getNamedItem((None, 'interpreter')).value
		else:
			interpreter = ''
		# Parse any additional arguments to the interpreter
		# or to the post section
		if attr.getNamedItem((None, 'arg')):
			arg = attr.getNamedItem((None, 'arg')).value
		else:
			arg = ''
		list = []
		list.append(string.strip(string.join([interpreter, arg])))
		list.append(self.getChildText(node))
		self.ks['pre'].append(list)

	# <post>
	
	def handle_post(self, node):
		attr = node.attributes
		# Parse the interpreter attribute
		if attr.getNamedItem((None, 'interpreter')):
			interpreter = \
				attr.getNamedItem((None, 'interpreter')).value
		else:
			interpreter = '/bin/bash'
		# Parse any additional arguments to the interpreter
		# or to the post section
		if attr.getNamedItem((None, 'arg')):
			arg = attr.getNamedItem((None, 'arg')).value
		else:
			arg = ''
		list = []
		# Add the args to the %post line
		list.append(string.strip(arg))
		# Add the interpreter to use for this post section
		list.append(string.strip('#!%s' % interpreter))
		list.append(self.getChildText(node))
		self.ks['post'].append(list)


	# <config>

	def handle_configure(self, node):
		""" for now we put everything in post"""
		self.handle_post(node)

		
	# <boot>
	
	def handle_boot(self, node):
		attr = node.attributes
		if attr.getNamedItem((None, 'order')):
			order = attr.getNamedItem((None, 'order')).value
		else:
			order = 'pre'

		self.ks['boot-%s' % order].append(self.getChildText(node))


	def generate_main(self):
		list = []
		list.append('')
		list += self.ks['main']
		return list

	def generate_packages(self):
		list = []
		list.append('%packages --ignoremissing')
		self.ks['rpms-on'].sort()
		for e in self.ks['rpms-on']:
			list.append(e)
		self.ks['rpms-off'].sort()
		for e in self.ks['rpms-off']:
			list.append('-' + e)
		return list

	def generate_pre(self):
		pre_list = []
		pre_list.append('')

		for list in self.ks['pre']:
			pre_list.append('%%pre --log=/tmp/ks-pre.log %s' %
				list[0])
			pre_list.append(string.join(list[1:], '\n'))
			
		return pre_list

	def generate_post(self):
		""" for backward compatibility"""
		return self.generate_config_kickstart()


	def generate_config_kickstart(self):
		""" generate a kickstart configure script """
		post_list = []
		post_list.append('')

		for list in self.ks['post']:
			post_list.append('%%post --log=%s %s\n' % \
				(self.log, list[0]))
			post_list += self._generate_config_script(list)

		return post_list


	def generate_config_script(self):
		""" generate a generic configure scritp """

		post_list = []
		post_list.append('')

		for list in self.ks['post']:
			if list[0] == "--nochroot":
				# there is not such a thing
				continue
			post_list += self._generate_config_script(list)

		return post_list


	def _generate_config_script(self, list):
		""" generate a generic script which can be enbeded in kickstart of
		run roll """
		temp_list = []
		tmpfile=tempfile.mktemp()
		# Create a 'HERE' document that is executed
		temp_list.append("cat > %s << 'ROCKS-KS-POST'\n" % tmpfile)
		# Shell interpreter (python, bash, etc)
		temp_list.append('%s\n' % list[1])
		temp_list.append(string.join(list[2:], '\n'))
		temp_list.append('ROCKS-KS-POST\n')
		# Chmod and execute the shell script just created
		temp_list.append('/bin/chmod +x %s\n' % tmpfile)
		temp_list.append('%s \n' % tmpfile)
		# clean up
		temp_list.append('/bin/rm %s \n' % tmpfile)
		return temp_list

	def generate_boot(self):
		list = []
		list.append('')
		list.append('%%post --log=%s' % self.log)
		
		# Boot PRE
		#	- check in/out all modified files
		#	- write the <boot order="pre"> text
		
		list.append('')
		list.append('cat >> /etc/sysconfig/rocks-pre << EOF')

		for (file, (owner, perms)) in self.rcsFiles.items():
			s = self.rcsEnd(file, owner, perms)
			list.append(s)

		for l in self.ks['boot-pre']:
			list.append(l)

		list.append('EOF')

		# Boot POST
		#	- write the <boot order="post"> text
		
		list.append('')
		list.append('cat >> /etc/sysconfig/rocks-post << EOF')

		for l in self.ks['boot-post']:
			list.append(l)

		list.append('EOF')
		list.append('')
		
		return list

		
class MainNodeFilter_sunos(NodeFilter):
	"""
	This class either accepts or reject tags
	from the node XML files. All tags are under
	the <main>*</main> tags.
	Each and every one of these tags needs to
	have a handler for them in the Generator
	class.
	"""
	def acceptNode(self, node):
		if node.nodeName == 'jumpstart':
			return self.FILTER_ACCEPT

		if node.nodeName not in [
			'main', 	# <main><*></main>
			'clearpart', 	# Clears the disk partitions
			'url', 		# URL to download all the packages from
			'part', 	# Partition information
			'size',
			'filesys',
			'slice',
			'locale',
			'timezone',
			'timeserver',
			'terminal',
			'name_service',
			'domain_name',
			'name_server',
			'nfs4_domain',
			'search',
			'rootpw', 	# root password
			'network',	# specify network configuration
			'interface',	# network interface
			'hostname',	# hostname
			'ip_address',	# IP Address
			'netmask',	# Netmask information
			'default_route',# Default Gateway
			'dhcp',		# to DHCP or not to DHCP
			'protocol_ipv6',# to IPv6 or not to IPv6
			'display',	# Display config
			'monitor',	# Monitor config
			'keyboard',	# Keyboard Config
			'pointer',	# Mouse config
			'security_policy', # Security config
			'auto_reg',	# Auto Registration
			'type',	# Auto Registration
			]:
			return self.FILTER_SKIP
			
		if not self.isCorrectCond(node):
			return self.FILTER_SKIP
	
		return self.FILTER_ACCEPT



class OtherNodeFilter_sunos(NodeFilter):
	"""
	This class accepts tags that define the
	pre section, post section and the packages
	section in the node XML files. The handlers
	for these are present in the Generator class.
	"""
	def acceptNode(self, node):
		if node.nodeName == 'jumpstart':
			return self.FILTER_ACCEPT

		if node.nodeName not in [
			'cluster',
			'package',
			'patch',
			'pre',
			'post',
			]:
			return self.FILTER_SKIP

		if not self.isCorrectCond(node):
			return self.FILTER_SKIP
			
		return self.FILTER_ACCEPT
		
		
class Generator_sunos(Generator):
	"""
	Handles all the XML tags that are acceptable
	and generates a jumpstart compatible output
	"""
	def __init__(self):
		Generator.__init__(self)
		self.ks = {}
		self.ks['main']		= []
		self.ks['url']		= ''
		self.ks['order']	= [] # Order of traversal
		self.ks['sysidcfg']	= [] # The Main section
		self.ks['part']		= [] # Partitioning
		self.ks['profile']	= [] # Misc. Profile Information
		self.ks['pkg_on']	= [] # Selected Packages
		self.ks['pkg_off']	= [] # Deselected Packages
		self.ks['pkgcl_on']	= [] # Selected Package Clusters
		self.ks['pkgcl_off']	= [] # Deselected Package Clusters
		self.ks['patch']	= [] # List of patches
		self.ks['begin']	= [] # Begin Section
		self.ks['finish']	= [] # Finish Section
		self.ks['service_on']	= [] # Enabled Services section
		self.ks['service_off']	= [] # Disabled Services section
		self.finish_section	= 0  # Iterator. This counts up for
					     # every post section that's
					     # encountered
					     
		self.service_instances	= {}
						

	def parse(self, xml_string):
		"""
		Creates an XML tree representation of the XML string,
		decompiles it, and parses the string.
		"""
		import cStringIO
		xml_buf = cStringIO.StringIO(xml_string)
		doc = xml.dom.ext.reader.Sax2.FromXmlStream(xml_buf)
		filter = MainNodeFilter_sunos(self.attrs)
		iter = doc.createTreeWalker(doc, filter.SHOW_ELEMENT,
			filter, 0)
		node = iter.nextNode()
		
		while node:
			if node.nodeName == 'jumpstart':
				self.handle_jumpstart(node)
			elif node.nodeName == 'main':
				child = iter.firstChild()
				while child:
					self.handle_mainChild(child)
					child = iter.nextSibling()
					
			elif node.nodeName in [
				'name_service',
				'network',
				'auto_reg',
				]:
				f = getattr(self, "handle_%s" % node.nodeName)
				f(node, iter)

			node = iter.nextNode()

		filter = OtherNodeFilter_sunos(self.attrs)
		iter = doc.createTreeWalker(doc, filter.SHOW_ELEMENT,
			filter, 0)
		node = iter.nextNode()
		while node:
			if node.nodeName != 'jumpstart':
				self.order(node)
				eval('self.handle_%s(node)' % (node.nodeName))
			node = iter.nextNode()

	# <jumpstart>
	
	def handle_jumpstart(self, node):
		# pull out the attr to handle generic conditionals
		# this replaces the old arch/os logic but still
		# supports the old syntax

		if node.attributes:
			attrs = node.attributes.getNamedItem((None, 'attrs'))
			if attrs:
				dict = eval(attrs.value)
				for (k,v) in dict.items():
					self.attrs[k] = v

	# <main>
	#	<clearpart>
	# </main>
	
	def handle_main_clearpart(self, node):
		self.ks['part'][0:0] = ['fdisk\trootdisk\tsolaris\tall']

	# <main>
	#	<url>
	# </main>
	
	def handle_main_url(self, node):
		self.ks['url'] = self.getChildText(node).strip()
	
	# <main>
	#	<rootpw>
	# </main>
	
	def handle_main_rootpw(self, node):
		self.ks['sysidcfg'].append("root_password=%s" %
			self.getChildText(node).strip())

	# <main>
	#	<locale>
	# </main>
	
	def handle_main_locale(self, node):
		self.ks['sysidcfg'].append("system_locale=%s" %
			self.getChildText(node).strip())

	# <main>
	#	<timezone>
	# </main>

	def handle_main_timezone(self, node):
		self.ks['sysidcfg'].append("timezone=%s" %
			self.getChildText(node).strip())

	# <main>
	#	<timeserver>
	# </main>

	def handle_main_timeserver(self, node):
		self.ks['sysidcfg'].append("timeserver=%s" %
			self.getChildText(node).strip())

	# <main>
	#	<nfs4_domain>
	# </main>

	def handle_main_nfs4_domain(self, node):
		self.ks['sysidcfg'].append("nfs4_domain=%s" %
			self.getChildText(node).strip())


	# <name_service>
	
	def handle_name_service(self, node, iter):
		dns = {}
		child = iter.firstChild()
		while child:
			dns[child.nodeName] = self.getChildText(child).strip()
			child = iter.nextSibling()
		self.ks['sysidcfg'].append("name_service=DNS {")
		for i in dns:
			self.ks['sysidcfg'].append('\t%s=%s' % (i, dns[i]))
		self.ks['sysidcfg'].append('}')
			
	
	# <auto_registration>
	def handle_auto_reg(self, node, iter):
		auto_reg = {}
		child = iter.firstChild()
		while child:
			auto_reg[child.nodeName] = self.getChildText(child).strip()
			child = iter.nextSibling()
		if not auto_reg.has_key('type'):
			self.ks['sysidcfg'].append('auto_reg=disable')
			return
		auto_reg_type = auto_reg.pop('type')
		if auto_reg_type in ['disable', 'none']:
			self.ks['sysidcfg'].append("auto_reg=%s" % auto_reg_type)
			return
		self.ks['sysidcfg'].append('auto_reg=%s {')
		for i in auto_reg:
			self.ks['sysidcfg'].append('\t%s=%s' % (i,auto_reg[i]))
		self.ks['sysidcfg'].append('}')
		
	# <main>
	#	<security_policy>
	# </main>
	
	def handle_main_security_policy(self, node):
		self.ks['sysidcfg'].append("security_policy=%s" %
			self.getChildText(node).strip())
	
	# <main>
	#	<display>
	# </main>
	
	def handle_main_display(self, node):
		self.ks['sysidcfg'].append("display=%s" %
			self.getChildText(node).strip())

	# <main>
	#	<monitor>
	# </main>
	
	def handle_main_monitor(self, node):
		self.ks['sysidcfg'].append("monitor=%s" %
			self.getChildText(node).strip())

	# <main>
	#	<keyboard>
	# </main>
	
	def handle_main_keyboard(self, node):
		self.ks['sysidcfg'].append("keyboard=%s" %
			self.getChildText(node).strip())

	# <main>
	#	<pointer>
	# </main>
	
	def handle_main_pointer(self, node):
		self.ks['sysidcfg'].append("pointer=%s" %
			self.getChildText(node).strip())
		

	# <*>
	#	<service>
	# </*>
	
	def handle_child_service(self, node):
		# Handle the <service> tags that enable
		# or disable services in Solaris
		
		# Get name and enabled flags
		attr = node.attributes
		name = None
		enabled = 'true'
		instance = 'default'
		if attr.getNamedItem((None, 'name')):
			name = attr.getNamedItem((None, 'name')).value
		# If there's no name return
		if not name:
			return ''

		if attr.getNamedItem((None, 'instance')):
			instance = attr.getNamedItem((None, 'instance')).value

		# populate the correct list, depending on
		# whether the service is enabled or disabled.
		if attr.getNamedItem((None, 'enabled')):
			enabled = attr.getNamedItem((None, 'enabled')).value
		if enabled == 'no' or enabled == 'false':
			enabled = 'false'
		else:
			enabled='true'

		if not self.service_instances.has_key(name):
			self.service_instances[name] = []
		self.service_instances[name].append((instance,enabled))
		# This is only to placate the getChildText
		# function. There's no need to return anything, as
		# a separate list is being populated to be used
		# later.
		return ''

	# <network>
	
	def handle_network(self, node, iter):
		net = {}
		dhcp = 0
		child = iter.firstChild()
		while child :
			if child.nodeName =='dhcp':
				dhcp = 1
			else:
				net[child.nodeName] = self.getChildText(child).strip()
			child = iter.nextSibling()
		if not net.has_key('interface'):
			net['interface'] = 'PRIMARY'
		self.ks['sysidcfg'].append("network_interface=%s{" %
			net.pop('interface'))
		if dhcp == 1:
			self.ks['sysidcfg'].append("\t\tdhcp")
		for i in net:
			self.ks['sysidcfg'].append("\t\t%s=%s" % (i, net[i]))
		self.ks['sysidcfg'].append("}")


	# <package>
	
	def handle_package(self, node):
		attr = node.attributes
		if self.isMeta(node):
			key = "pkgcl"
		else:
			key = "pkg"

		if self.isDisabled(node):
			key = key + "_off"
		else:
			key = key + "_on"

		self.ks[key].append(self.getChildText(node).strip())
		
	# patch
	def handle_patch(self, node):
		attr = node.attributes
		self.ks['patch'].append(self.getChildText(node))
	# <pre>
		
	def handle_pre(self, node):
		self.ks['begin'].append(self.getChildText(node))

	# <post>
	
	def handle_post(self, node):
		"""Function works in an interesting way. On solaris the post
		sections are executed in the installer environment rather than
		in the installed environment. So the way we do it is to write
		a script for every post section, with the correct interpreter
		and execute it with a chroot command.
		"""
		attr = node.attributes
		# By default we always want to chroot, unless
		# otherwise specified
		if attr.getNamedItem((None, 'chroot')):
			chroot = attr.getNamedItem((None, 'chroot')).value
		else:
			chroot = 'yes'

		# By default, the interpreter is always /bin/sh, unless
		# otherwise specified.
		if attr.getNamedItem((None, 'interpreter')):
			interpreter = attr.getNamedItem((None,
				'interpreter')).value
		else:
			interpreter = '/bin/sh'

		# The args that are supplied are for the command that
		# you want to run, and not to the installer section.
		if attr.getNamedItem((None, 'arg')):
			arg = attr.getNamedItem((None, 'arg')).value
		else:
			arg = ''

		list = []
		if chroot == 'yes':
			list.append("cat > /a/tmp/post_section_%d << '__eof__'"
					% self.finish_section)
			list.append("#!%s" % interpreter)
			list.append(self.getChildText(node))
			list.append("__eof__")
			list.append("chmod a+rx /a/tmp/post_section_%d"
					% self.finish_section)
			list.append("chroot /a /tmp/post_section_%d %s"
					% (self.finish_section, arg))
		else:
			if interpreter is not '/bin/sh':
				list.append("cat > /tmp/post_section_%d "
					"<< '__eof__'"
					% self.finish_section)
				list.append("#!%s" % interpreter)
				list.append(self.getChildText(node))
				list.append("__eof__")
				list.append("chmod a+rx /tmp/post_section_%d"
					% self.finish_section)
				list.append("%s /tmp/post_section_%d"
					% (interpreter, self.finish_section))
			
			else:
				list.append(self.getChildText(node))

		self.finish_section = self.finish_section+1
		self.ks['finish'] += list

	def generate(self, section):
		"""Function generates the requested section
		of the jumpstart file"""
		
		list = []
		
		f = getattr(self, 'generate_%s' % section )
		list += f()

		return list

	def generate_begin(self):
		""" Generates the pre installation scripts"""
		list = []
		list += self.ks['begin']
		return list

	def generate_finish(self):
		list = []
		list += self.generate_order()
		list += self.ks['finish']

		# Generate and add the services section to the finish
		# script. 
		list += self.generate_services()
		# And we're done
		
		return list

	def generate_profile(self):
		if self.ks['url'] != '':
			location = self.ks['url']
		else:
			location = "local_file\t/cdrom"
		list = []
		list.append("# Installation Type")
		list.append("install_type\tinitial_install")
		list.append("\n")
		list.append("# System Type")
		list.append("system_type\tstandalone")
		list.append("\n")
		list.append("# Profile Information")
		list.append("\n")
		list += self.ks['profile']
		list.append("# Partition Information")
		list += self.ks['part']
		list.append("\n")
		list.append("# Packages Section")
		for i in self.ks['pkgcl_on']:
			list.append('cluster\t%s' % i)
		for i in self.ks['pkgcl_off']:
			list.append('cluster\t%s\tdelete' % i)
		for i in self.ks['pkg_on']:
			list.append('package\t%s\tadd' % i)
		for i in self.ks['pkg_off']:
			list.append('package\t%s\tdelete' % i)
		if len(self.ks['patch']) > 0:
			patch_list = string.join(self.ks['patch'],',')
			list.append('patch %s local_file /cdrom/Solaris_10/Patches' % patch_list)

		return list
		
	def generate_sysidcfg(self):
		list = []
		list += self.ks['sysidcfg']
		return list

	def generate_rules(self):
		list = []
		list.append("any\t-\tbegin\tprofile\tfinish")
		return list

	def generate_services(self):

		# Generates an XML file with a list of 
		# all enabled and disabled services. This
		# is going to be used when assembling services
		# on compute nodes.
		# The way to do this is to copy the service manifest
		# xml file to /var/svc/manifest/ which should be done by
		# an explicit cp command in the post section. Then enable
		# these services by adding them to the site.xml command
		# on the target machine.

		if len(self.service_instances) == 0:
			return []
		list= []

		list.append("cat > /a/var/svc/profile/site.xml << '_xml_eof_'")
		# XML Headers, and doctype
		list.append("<?xml version='1.0'?>")
		list.append("<!DOCTYPE service_bundle SYSTEM "
			"'/usr/share/lib/xml/dtd/service_bundle.dtd.1'>")

		# Start service bundle
		list.append("<service_bundle type='profile' name='site'"
			"\n\txmlns:xi='http://www.w3.org/2001/XInclude' >")

		for i in self.service_instances.keys():
			list.append("\t<service name='%s' version='1' type='service'>" % i)
			for j in self.service_instances[i]:
				list.append("\t\t<instance name='%s' enabled='%s'/>" \
						% (j[0], j[1]))
			list.append("\t</service>")

		# End Service bundle
		list.append("</service_bundle>")
		list.append('_xml_eof_')

		return list
