# $Id: __init__.py,v 1.23 2012/05/06 05:48:22 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.5 (Mamba)
# 		         version 6.0 (Mamba)
# 
# Copyright (c) 2000 - 2012 The Regents of the University of California.
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
# Revision 1.23  2012/05/06 05:48:22  phil
# Copyright Storm for Mamba
#
# Revision 1.22  2011/07/23 02:30:26  phil
# Viper Copyright
#
# Revision 1.21  2010/09/07 23:52:51  bruno
# star power for gb
#
# Revision 1.20  2009/05/01 19:06:56  mjk
# chimi con queso
#
# Revision 1.19  2009/04/14 16:12:16  bruno
# push towards chimmy beta
#
# Revision 1.18  2008/10/18 00:55:48  mjk
# copyright 5.1
#
# Revision 1.17  2008/08/05 19:47:58  bruno
# filter out anaconda packages when mirroring
#
# Revision 1.16  2008/07/07 22:45:18  bruno
# if mason wrote science fiction, he would have named the novel:
#
#       I, Rebot
#
# Revision 1.15  2008/05/30 18:19:49  mjk
# CentOS mirrors now use robots.txt to break RPM fetching.
# Disable the robots.txt processing in wget
#
# Revision 1.14  2008/03/16 17:19:06  bruno
# make the arch a parameter: thanks phil and nadya.
#
# Revision 1.13  2008/03/06 23:41:36  mjk
# copyright storm on
#
# Revision 1.12  2007/07/04 17:02:48  bruno
# path is an argument, not a parameter.
#
# Revision 1.11  2007/07/04 01:47:37  mjk
# embrace the anger
#
# Revision 1.10  2007/07/02 18:35:24  bruno
# create cleanup
#
# Revision 1.9  2007/06/23 03:54:51  mjk
# - first pass at consistency
# - still needs some docstrings
# - argument processors take SQL wildcards
# - add cannot run twice (must use set)
# - dump does sets not just adds
#
# Revision 1.8  2007/06/19 16:42:40  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.7  2007/06/07 21:23:04  mjk
# - command derive from verb.command class
# - default is MustBeRoot
# - list.command / dump.command set MustBeRoot = 0
# - removed plugin non-bugfix
#
# Revision 1.6  2007/06/04 20:40:30  bruno
# tweaks to rocks enable/disable roll
#
# Revision 1.5  2007/05/31 22:57:06  bruno
# more tweaks
#
# Revision 1.4  2007/05/31 19:35:41  bruno
# first pass at getting all the 'help' consistent on all the rocks commands
#
# Revision 1.3  2007/05/10 20:37:00  mjk
# - massive rocks-command changes
# -- list host is standardized
# -- usage simpler
# -- help is the docstring
# -- host groups and select statements
# - added viz commands
#
# Revision 1.2  2007/04/06 21:37:22  bruno
# add the rocks-roll replacement and changed 'rocks create mirror' to call
# 'rocks create roll' to build the ISO image
#
# Revision 1.1  2007/04/06 18:24:26  bruno
# converted rocks-mirror
#
#

import os
import stat
import time
import sys
import string
import rocks
import rocks.commands


class Command(rocks.commands.create.command):
	"""	
	Create a Roll ISO image from the packages found in the
	repository located at 'URL'.

	<arg type='string' name='path'>	
	The network location of the repository of packages.
	</arg>
	
	<param type='string' name='rollname'>
	The base name for the created Roll. (default = 'updates').
	</param>
	
	<param type='string' name='version'>
	The version number of the created Roll. (default = the version of 
	Rocks running on this machine).
	</param>

	<param type='string' name='arch'>
	Architecture of the mirror. (default = the architecture of 
	of the OS running on this machine).
	</param>

	<example cmd='create mirror http://mirrors.kernel.org/centos/4.5/updates/i386/RPMS rollname=updates version=4.5'>
	Will mirror all the packages found under the URL
	http://mirrors.kernel.org/centos/4.5/updates/i386/RPMS and will create
	a Roll ISO image named 'updates-4.5-0.i386.disk1.iso'.
	</example>
	"""


	def mirror(self, mirror_path):
		cmd = 'wget -erobots=off --reject "anaconda*rpm" -m -nv -np %s' % (mirror_path)
		os.system(cmd)

		if len(mirror_path) > 6:
			if mirror_path[0:6] == 'ftp://':
				mirrordir = mirror_path[6:]
			elif mirror_path[0:7] == 'http://':
				mirrordir = mirror_path[7:]
			else:
				mirrordir = mirror_path

		os.symlink(mirrordir, 'RPMS')


	def makeRollXML(self, rollname, version, arch, xmlfilename):
		file = open(xmlfilename, 'w')
		file.write('<roll name="%s" interface="4.0">\n' % rollname)

		rolltime = time.strftime('%X')
		rolldate = time.strftime('%b %d %Y')
		rollzone = time.strftime('%Z')
		file.write('\t<timestamp time="%s" date="%s" tz="%s"/>\n' %
			(rolltime, rolldate, rollzone))

		file.write('\t<color edge="lawngreen" node="lawngreen"/>\n')
		file.write('\t<info version="%s" release="0" arch="%s"/>\n' % 
			(version, arch))

		file.write('\t<iso maxsize="0" bootable="0" mkisofs=""/>\n')
		file.write('\t<rpm rolls="0" bin="1" src="0"/>/\n')
		file.write('</roll>\n')
		file.close()


	def clean(self):
		if os.path.islink('RPMS'):
			os.unlink('RPMS')
		os.system('rm -rf disk1')


	def run(self, params, args):

		if len(args) != 1:
			self.abort('must supply one path')
		mirror_path = args[0]
		
		(rollname, version, arch) = self.fillParams(
			[('rollname', 'updates'),
			('version', rocks.version),
			('arch',self.arch)])

		xmlfilename = 'roll-%s.xml' % rollname

		self.clean()
		
		self.mirror(mirror_path)
		self.makeRollXML(rollname, version, arch, xmlfilename)
		
		self.command('create.roll', [ '%s' % (xmlfilename) ] )
		
		self.clean()

