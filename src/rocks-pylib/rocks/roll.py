#! /opt/rocks/bin/python
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
# 
# Copyright (c) 2000 - 2014 The Regents of the University of California.
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
# $Log: roll.py,v $
# Revision 1.25  2012/11/27 00:48:40  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.24  2012/05/06 05:48:47  phil
# Copyright Storm for Mamba
#
# Revision 1.23  2012/01/07 05:03:21  phil
#
# Fixups
#
# Revision 1.22  2012/01/06 19:20:06  phil
# Use yum to install OS packages when bootstrapping
#
# Revision 1.21  2011/07/23 02:30:49  phil
# Viper Copyright
#
# Revision 1.20  2010/09/07 23:53:08  bruno
# star power for gb
#
# Revision 1.19  2009/05/01 19:07:08  mjk
# chimi con queso
#
# Revision 1.18  2009/01/08 01:20:58  bruno
# for anoop
#
# Revision 1.17  2008/10/18 00:56:02  mjk
# copyright 5.1
#
# Revision 1.16  2008/08/07 21:19:23  bruno
# OS roll building fix
#
# Revision 1.15  2008/05/22 21:02:07  bruno
# rocks-dist is dead!
#
# moved default location of distro from /export/home/install to
# /export/rocks/install
#
# Revision 1.14  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.13  2007/12/13 02:53:40  bruno
# can now build a bootable kernel CD and build a physical frontend with V
# on RHEL 5 update 1
#
# Revision 1.12  2007/12/10 21:28:35  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.11  2007/06/23 04:03:24  mjk
# mars hill copyright
#
# Revision 1.10  2006/09/11 22:47:23  mjk
# monkey face copyright
#
# Revision 1.9  2006/08/10 00:09:41  mjk
# 4.2 copyright
#
# Revision 1.8  2006/06/08 20:04:20  bruno
# added class to interface with rocks media (CDs and network)
#
# Revision 1.7  2006/06/05 17:57:37  bruno
# first steps towards 4.2 beta
#
# Revision 1.6  2006/01/16 06:49:00  mjk
# fix python path for source built foundation python
#
# Revision 1.5  2005/10/12 18:08:42  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:02:21  mjk
# updated copyright
#
# Revision 1.3  2005/07/11 23:51:35  mjk
# use rocks version of python
#
# Revision 1.2  2005/07/11 21:55:48  mjk
# changes for foundation
#
# Revision 1.1  2005/07/11 17:31:28  mjk
# moved code from rocks-roll
#
#


import os
import sys
import re
import string
import tempfile
from xml.dom                 import ext
from xml.dom.ext.reader.Sax2 import FromXmlStream
from xml.sax._exceptions     import SAXParseException
import rocks.file
import rocks.util
import rocks.gen

class Distribution:

	def __init__(self, arch, name='rocks-dist'):
		self.arch = arch
		self.tree = None
		self.name = name
	
	def getPath(self):
		return os.path.join(self.name, self.arch)
		
	def systemRepoList(self):
		""" Generate the list of Enabled Repos from the system yum configuration.
                    Can use this list to explicitly disable these repos when installing from
                    a purely local repo """
		preamble = 1
		repolist = []
		a = os.popen("yum repolist")
		for line in a.readlines():
			if preamble and re.search("repo id", line):
				preamble = 0
				continue
			if not preamble:
				if not re.search("repolist:",line):
					repolist.append(string.split(line)[0])
		return repolist

	def createLocalYumConf(self):
		""" Create a yum conf file to enable this distribution """
		(fd, self.yumConfFile) = tempfile.mkstemp()
		confstr = "[temprepo] \n"
		confstr += "name=tempRepo \n"
		confstr += "baseurl=file://%s \n"
		confstr += "enabled=1 \n"
		confstr += "gpgcheck=0 \n"
		os.write(fd, confstr % self.tree.getRoot())
		os.close(fd)
		 
	 
	def generate(self, flags=""):
		rocks.util.system('/opt/rocks/bin/rocks create distro ' + \
			'dist=%s %s' % (self.name, flags))
		self.tree = rocks.file.Tree(os.path.join(os.getcwd(), 
			self.getPath()))
		self.createLocalYumConf()
		
	def getRPMS(self):
		return self.tree.getFiles(os.path.join('RedHat', 'RPMS'))

	def getSRPMS(self):
		return self.tree.getFiles('SRPMS')
		
	def getRPM(self, name):
		l = []
		for rpm in self.getRPMS():
			try:
				if rpm.getPackageName() == name:
					l.append(rpm)
			except:
				pass
		if len(l) > 0:
			return l
		return None

	def installPackagesYum(self,pkgList, options=' '):
		""" Given a package list (no version #s, but could have an arch tag), attempt to install
		the pkgList via yum.  Have to disable the system repos, if there are any """
		cmd = "yum -y install -c %s" % self.yumConfFile
		ignoreRepos = self.systemRepoList()
		if len(ignoreRepos) > 0:
			cmd += " --disablerepo=%s" % (','.join(ignoreRepos))
		cmd += " %s" % options
		cmd += " %s" % ' '.join(pkgList) 
		print 'cmd', cmd
		return os.system(cmd)
		
		
		


#
# used to parse rolls.xml file
#
class ScreenNodeFilter(rocks.gen.NodeFilter):
	def acceptNode(self, node):
		if node.nodeName in [ 
			'rolls',
			'roll',
			]:
			return self.FILTER_ACCEPT
		else:
			return self.FILTER_SKIP


osGenerator = getattr(rocks.gen, 'Generator_%s' % os.uname()[0].lower())

class Generator(osGenerator):
	def __init__(self):
		osGenerator.__init__(self)	
		self.rolls = []
		self.os = os.uname()[0].lower()
		return

	##
	## Parsing Section
	##
	def parse(self, file):
		doc  = FromXmlStream(file)

		filter = ScreenNodeFilter({})
		iter = doc.createTreeWalker(doc, filter.SHOW_ELEMENT,
			filter, 0)
		node = iter.nextNode()

		while node:
			if node.nodeName == 'roll':
				self.handle_rollChild(node)
			node = iter.nextNode()

			
	# <roll>
	def handle_rollChild(self, node):
		attr = node.attributes
		if attr.getNamedItem((None, 'name')):
			name = attr.getNamedItem((None, 'name')).value
		else:
			name = ''

		if attr.getNamedItem((None, 'version')):
			version = attr.getNamedItem((None, 'version')).value
		else:
			version = ''

		if attr.getNamedItem((None, 'arch')):
			arch = attr.getNamedItem((None, 'arch')).value
		else:
			arch = ''

		if attr.getNamedItem((None, 'url')):
			url = attr.getNamedItem((None, 'url')).value
		else:
			url = ''

		if attr.getNamedItem((None, 'diskid')):
			diskid = attr.getNamedItem((None, 'diskid')).value
		else:
			diskid = ''

		self.rolls.append((name, version, arch, url, diskid))

		return

