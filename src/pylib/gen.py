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
# $Log: gen.py,v $
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
# packages to be able to use HTTP for installation does not work and is completely
# usesless. Will use this when the Solaris installer code is advanced
#
# Revision 1.21  2007/09/25 21:56:03  anoop
# Made the jumpstart config generator a bit more http aware. Still an ugly kludge
# that the Sun engineers should work on, to get native http support into pfinstall
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
import time
import xml.dom.NodeFilter
import xml.dom.ext.reader.Sax2
import rocks.js

class NodeFilter(xml.dom.NodeFilter.NodeFilter):

	def __init__(self, arch, osname):
		self.arch = arch
		self.os = osname

	def isCorrectArch(self, node):
		attr = node.attributes
		if attr:
			arch = attr.getNamedItem((None, 'arch'))
			if arch:
				list = []
				for e in string.split(arch.value, ','):
					list.append(string.strip(e))
				arch = list
			else:
				arch = [ self.arch ]
			if self.arch not in arch:
				return 0
		return 1

	def isCorrectOS(self, node):
		attr = node.attributes
		if attr:
			oses = attr.getNamedItem((None, 'os'))
			if oses:
				list = []
				for e in string.split(oses.value, ','):
					list.append(string.strip(e))
				oses = list
			else:
				oses = [ self.os ]
			if self.os not in oses:
				return 0
		return 1
		
		
		
class Generator:
	"""Base class for various DOM based kickstart graph generators.
	The input to all Generators is assumed to be the XML output of KPP."""
	
	def __init__(self):
		self.arch	= None
		self.rcsComment = 'ROCKS'
		self.rcsTag	= 'ROCKS'
		self.rcsEpoch	= int(time.time())

	def setArch(self, arch):
		self.arch = arch
		
	def getArch(self):
		return self.arch
	
	def setOS(self, osname):
		self.os = osname
		
	def getOS(self):
		return self.os

	def setRCSComment(self, s):
		self.rcsComment = s
		
	def getRCSComment(self):
		return self.rcsComment
		
	def setRCSTag(self, s):
		self.rcsTag = s
		
	def getRCSTag(self):
		return self.rcsTag
		
	def setRCSEpoch(self, n):
		self.rcsEpoch = n
		
	def getRCSEpoch(self):
		return self.rcsEpoch
				
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
	
	def rcsBegin(self, file):
		l = []
		rcsdir  = os.path.join(os.path.dirname(file), 'RCS')
		rcsfile = os.path.join(rcsdir, os.path.basename(file))
		l.append('touch %s' % file)
		l.append('if [ ! -d %s ]; then' % rcsdir)
		l.append('	mkdir %s' % rcsdir)
		l.append('fi')
		l.append('if [ ! -f %s,v ]; then' % rcsfile)
		l.append('	echo "initial checkin" | ci %s' % file)
		l.append('fi')
		l.append('co -f %s' % file)
		l.append('t=TAG_`rpm -qf %s | sort | md5sum | tr -cd [:alnum:]`'
			% file)
		l.append('if ! co -f -p$t %s > /dev/null 2>&1; then' % file)
		l.append('	rcs -n$t: %s' % file)
		l.append('fi')
		l.append('if ! co -f -p%s_%s %s > /dev/null 2>&1; then' % 
			(self.rcsTag, self.rcsEpoch, file))
		l.append('	rcs -n%s_%s: %s' % (self.rcsTag, self.rcsEpoch,
			file))
		l.append('	co -f -l -r$t %s' % file)
		l.append('else')
		l.append('	co -f -l %s' % file)
		l.append('fi')
		return '%s\n' % string.join(l, '\n')
		
	def rcsEnd(self, file):
		l = []
		rcsdir  = os.path.join(os.path.dirname(file), 'RCS')
		rcsfile = os.path.join(rcsdir, os.path.basename(file))

		# If NTP changes the clock on us this can break RCS.which
		# has a bunch of timestamp optimizations...
		# This code will replace the timestamp of the last
		# revision with the current clock and then touch the
		# file to be checked in.  This way the delta is always
		# newer than the last revision.
		l.append('cat %s,v | '
			'awk -v date=`date -u +%%Y.%%m.%%d.%%H.%%M.%%S` '
			'\'/^date/ { '
				'printf "date\\t%%s;\\tauthor %%s\\tstate Exp;", '
				'date, $4; '
				'next; '
			'} '
			'{ print; }'
			'\' > %s.bak' % (rcsfile, rcsfile))
			
		# Do a copy/rm rather than a mv to preserve perms on the 
		# RCS file.
			
		l.append('cp %s.bak %s,v' % (rcsfile, rcsfile))
		l.append('rm -f %s.bak' % rcsfile)
		
		l.append('touch %s' % file)

		# Now just check it in as we did before

		l.append('echo "%s" | ci %s' % (self.rcsComment, file))
		l.append('co -f %s' % file)
		return '%s\n' % string.join(l, '\n')
	
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
		
			s = self.rcsBegin(fileName)

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

			s += self.rcsEnd(fileName)

			if fileOwner:
				s += "chown %s %s\n" % (fileOwner, fileName)
			if filePerms:
				s += "chmod %s %s\n" % (filePerms, fileName)
			
			
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
			list += f()
		except:
			pass
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
			
		if not self.isCorrectArch(node):
			return self.FILTER_SKIP

		if not self.isCorrectOS(node):
			return self.FILTER_SKIP
	
		if node.nodeName in [
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
			return self.FILTER_ACCEPT
		else:
			return self.FILTER_SKIP


class OtherNodeFilter_linux(NodeFilter):
	def acceptNode(self, node):
		if node.nodeName == 'kickstart':
			return self.FILTER_ACCEPT
			
		if not self.isCorrectArch(node):
			return self.FILTER_SKIP

		if not self.isCorrectOS(node):
			return self.FILTER_SKIP
	
		if node.nodeName in [ 
			'debug',
			'description',
			'package',
			'pre', 
			'post'
			]:
			return self.FILTER_ACCEPT
		else:
			return self.FILTER_SKIP


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

	
	##
	## Parsing Section
	##
	
	def parse(self, xml_string):
		import cStringIO
		xml_buf = cStringIO.StringIO(xml_string)
		doc = xml.dom.ext.reader.Sax2.FromXmlStream(xml_buf)
		filter = MainNodeFilter_linux(self.getArch(), self.getOS())
		iter = doc.createTreeWalker(doc, filter.SHOW_ELEMENT,
			filter, 0)
		node = iter.nextNode()
		
		while node:
			if node.nodeName == 'main':
				child = iter.firstChild()
				while child:
					self.handle_mainChild(child)
					child = iter.nextSibling()

			node = iter.nextNode()

		filter = OtherNodeFilter_linux(self.getArch(), self.getOS())
		iter = doc.createTreeWalker(doc, filter.SHOW_ELEMENT,
			filter, 0)
		node = iter.nextNode()
		while node:
			if node.nodeName != 'kickstart':
				self.order(node)
				eval('self.handle_%s(node)' % (node.nodeName))
			node = iter.nextNode()


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
			(self.getChildText(node)))
		return


	# <main>
	#	<bootloader>
	# </main>

	def handle_main_bootloader(self, node):
		self.ks['main'].append('bootloader %s' % 
			(self.getChildText(node)))
		return

	# <main>
	#	<lang>
	# </main>

	def handle_main_lang(self, node):
		self.ks['main'].append('lang %s' % 
			(self.getChildText(node)))
		return

	# <main>
	#	<langsupport>
	# </main>

	def handle_main_langsupport(self, node):
		self.ks['main'].append('langsupport --default=%s' %
			(self.getChildText(node)))

		return

	# <main>
	#	<volgroup>
	# </main>

	def handle_main_volgroup(self, node):
		self.ks['main'].append('volgroup %s' % 
			(self.getChildText(node)))
		return

	# <main>
	#	<logvol>
	# </main>

	def handle_main_logvol(self, node):
		self.ks['main'].append('logvol %s' % 
			(self.getChildText(node)))
		return

	# <debug>
	
	def handle_debug(self, node):
		self.ks['debug'].append(self.getChildText(node))
	
	# <package>
		
	def handle_package(self, node):
		rpm = string.strip(self.getChildText(node))

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
		if attr.getNamedItem((None, 'arg')):
			arg = attr.getNamedItem((None, 'arg')).value
		else:
			arg = ''
		list = []
		list.append(arg)
		list.append(self.getChildText(node))
		self.ks['pre'].append(list)

	# <post>
	
	def handle_post(self, node):
		attr = node.attributes
		if attr.getNamedItem((None, 'arg')):
			arg = attr.getNamedItem((None, 'arg')).value
		else:
			arg = ''
		list = []
		list.append(arg)
		list.append(self.getChildText(node))
		self.ks['post'].append(list)


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
			pre_list.append('%%pre %s' % list[0])
			pre_list.append(string.join(list[1:], '\n'))
			
		return pre_list

	def generate_post(self):
		post_list = []
		post_list.append('')

		for list in self.ks['post']:
			post_list.append('%%post %s' % list[0])
			post_list.append(string.join(list[1:], '\n'))
			
		return post_list

		
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
		return self.FILTER_ACCEPT
		if node.nodeName == 'jumpstart':
			return self.FILTER_ACCEPT
		if node.nodeName in [
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
			'dhcp',		# to DHCP or not to DHCP
			'protocol_ipv6',# to IPv6 or not to IPv6
			'display',	# Display config
			'monitor',	# Monitor config
			'keyboard',	# Keyboard Config
			'pointer',	# Mouse config
			'security_policy', # Security config
			]:
			return self.FILTER_ACCEPT
		else:
			return self.FILTER_SKIP


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
		if node.nodeName in [
			'cluster',
			'package',
			'pre',
			'post',
			]:
			return self.FILTER_ACCEPT
		else:
			return self.FILTER_SKIP

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
		self.ks['begin']	= [] # Begin Section
		self.ks['finish']	= [] # Finish Section
		self.ks['service_on']	= [] # Enabled Services section
		self.ks['service_off']	= [] # Disabled Services section
		self.finish_section	= 0  # Iterator. This counts up for
					     # every post section that's encountered
					     
		self.service_instances	= {}
		self.setRCSTag('JGEN')
						

	def parse(self, xml_string):
		"""
		Creates an XML tree representation of the XML string,
		decompiles it, and parses the string.
		"""
		import cStringIO
		self.xml_buf = cStringIO.StringIO(xml_string)
		self.xml_doc = xml.dom.ext.reader.Sax2.FromXmlStream(self.xml_buf)
		self.xml_filter = MainNodeFilter_sunos(self.getArch(), self.getOS())
		self.xml_tree = self.xml_doc.createTreeWalker(self.xml_doc,
			self.xml_filter.SHOW_ELEMENT, self.xml_filter, 0)
		node = self.xml_tree.nextNode()
		while node:
			if node.nodeName == 'main':
				child = self.xml_tree.firstChild()
				while child:
					self.handle_mainChild(child)
					child = self.xml_tree.nextSibling()
			if node.nodeName in [
				'part',
				'name_service',
				'network',
				]:
				f = getattr(self, "handle_%s" % node.nodeName)
				f(node)

			node = self.xml_tree.nextNode()

		self.xml_filter = OtherNodeFilter_sunos(self.getArch(), self.getOS())
		self.xml_tree = self.xml_doc.createTreeWalker(self.xml_doc, 
			self.xml_filter.SHOW_ELEMENT, self.xml_filter, 0)
		node = self.xml_tree.nextNode()
		while node:
			if node.nodeName != 'jumpstart':
				self.order(node)
				eval('self.handle_%s(node)' % (node.nodeName))
			node = self.xml_tree.nextNode()
			
	def handle_main_clearpart(self, node):
		self.ks['part'][0:0] = ['fdisk\trootdisk\tsolaris\tall']

	def handle_main_url(self, node):
		self.ks['url'] = self.getChildText(node)
	
	def handle_main_rootpw(self, node):
		self.ks['sysidcfg'].append("root_password=%s" % string.strip(self.getChildText(node)))

	def handle_main_locale(self, node):
		self.ks['sysidcfg'].append("system_locale=%s" % string.strip(self.getChildText(node)))

	def handle_main_timezone(self, node):
		self.ks['sysidcfg'].append("timezone=%s" % string.strip(self.getChildText(node)))

	def handle_main_timeserver(self, node):
		self.ks['sysidcfg'].append("timeserver=%s" % string.strip(self.getChildText(node)))

	def handle_main_nfs4_domain(self, node):
		self.ks['sysidcfg'].append("nfs4_domain=%s" % string.strip(self.getChildText(node)))

	def handle_name_service(self, node):
		dns = {}
		child = self.xml_tree.firstChild()
		while(child):
			dns[child.nodeName] = string.strip(self.getChildText(child))
			child = self.xml_tree.nextSibling()
		if not dns.has_key('domain_name'):
			dns['domain_name'] = 'local'
		if not dns.has_key('name_server'):
			dns['name_server'] = '10.1.1.1'
		if not dns.has_key('search'):
			dns['search'] = 'local'
		self.ks['sysidcfg'].append("name_service=DNS {")
		for i in dns:
			self.ks['sysidcfg'].append('\t%s=%s' % (i, dns[i]))
		self.ks['sysidcfg'].append('}')
			
	
	def handle_main_security_policy(self, node):
		self.ks['sysidcfg'].append("security_policy=%s" % string.strip(self.getChildText(node)))
	
	def handle_main_display(self, node):
		self.ks['sysidcfg'].append("display=%s" % string.strip(self.getChildText(node)))

	def handle_main_monitor(self, node):
		self.ks['sysidcfg'].append("monitor=%s" % string.strip(self.getChildText(node)))

	def handle_main_keyboard(self, node):
		self.ks['sysidcfg'].append("keyboard=%s" % string.strip(self.getChildText(node)))

	def handle_main_pointer(self, node):
		self.ks['sysidcfg'].append("pointer=%s" % string.strip(self.getChildText(node)))
		

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

	#-----------------------------------------------------------#
	# These functions are yet to be defined depending on
	# the redefinition of the xml files. Most likely
	# they'll get their own handling tags, rather than
	# being children of the main tag
	def handle_part(self, node):
		partition = {}
		child = self.xml_tree.firstChild()
		while(child):
			partition[child.nodeName] = self.getChildText(child)
			child = self.xml_tree.nextSibling()
		if not partition.has_key('slice'):
			partition['slice'] = 'any'
		else:
			partition['slice'] = 'rootdisk.' + partition['slice']
		self.ks['part'].append("filesys\t%s\t%s\t%s" %
			(partition['slice'], 
			 partition['size'], 
			 partition['filesys'])
		)

	def handle_network(self, node):
		net = {}
		dhcp = 0
		child = self.xml_tree.firstChild()
		while(child):
			if child.nodeName =='dhcp':
				dhcp = 1
			else:
				net[child.nodeName] = string.strip(self.getChildText(child))
			child = self.xml_tree.nextSibling()
		if not net.has_key('interface'):
			net['interface'] = 'PRIMARY'
		self.ks['sysidcfg'].append("network_interface=%s{" % net.pop('interface'))
		if dhcp == 1:
			self.ks['sysidcfg'].append("\t\tdhcp")
		for i in net:
			self.ks['sysidcfg'].append("\t\t%s=%s" % (i, net[i]))
		self.ks['sysidcfg'].append("}")


	def handle_package(self, node):
		self.ks['pkg_on'].append(self.getChildText(node))

	def handle_cluster(self, node):
		self.ks['pkgcl_on'].append(string.strip(self.getChildText(node)))
		#root_cluster = self.getChildText(node) 
		#pkg_cluster = rocks.js.clustertoc_parse(root_cluster)
		#self.ks['pkg_on'] += pkg_cluster.pkg_list
		
	def handle_pre(self, node):
		self.ks['begin'].append(self.getChildText(node))

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
			interpreter = attr.getNamedItem((None, 'interpreter')).value
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
				list.append("cat > /tmp/post_section_%d << '__eof__'"
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
		# script. The way to do this is to copy the service manifest
		# xml file to /var/svc/manifest/ which should be done by
		# an explicit cp command in the post section. Then enable
		# these services by adding them to the site.xml command
		# on the target machine.
		list.append("cat > /a/var/svc/profile/site.xml << '_xml_eof_'")
		list += self.generate_services()
		list.append('_xml_eof_')
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
		list = []

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

		return list
			
	def rcsBegin(self, filename):
		return ''
	
	def rcsEnd(self, filename):
		return ''
