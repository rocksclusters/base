#! /opt/rocks/bin/python
#
# Writes the /boot/grub/rocks.conf file, based on grub.conf.
# Used during postAction of kickstart.
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
# $Log: grub.py,v $
# Revision 1.12  2008/08/28 04:39:02  phil
# Hooks to write a xen vs. non-xen rocks.conf file.
#
# Revision 1.11  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.10  2008/01/23 20:59:12  bruno
# can now add kernel boot parameters to xen-enabled kernels
#
# Revision 1.9  2007/06/23 04:03:24  mjk
# mars hill copyright
#
# Revision 1.8  2006/09/11 22:47:23  mjk
# monkey face copyright
#
# Revision 1.7  2006/08/10 00:09:41  mjk
# 4.2 copyright
#
# Revision 1.6  2006/01/16 06:48:59  mjk
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
# Revision 1.2  2005/05/24 21:21:57  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/01 00:22:08  mjk
# moved to base roll
#
# Revision 1.4  2004/12/09 01:22:33  fds
# More consitant append() operation, more reliable. Tested.
#
# Revision 1.3  2004/11/02 00:36:50  fds
# grub.py
#
# Revision 1.2  2004/08/21 00:23:34  fds
# Support for cluster shepherd.
#
# Revision 1.1  2004/04/26 20:14:11  fds
# Used in kickstart process multiple times. Imported on the fly in post section
# just after it is installed.
#
#
import string
import os

class App:

	def __init__(self):
		self.defaultargs = 'ramdisk_size=150000 kssendmac '
		self.setFilename('rocks.conf')
		self.title = 'Rocks Reinstall'
		self.installKernel = 'kickstart/default/vmlinuz'  
		self.installRamdisk = 'kickstart/default/initrd.img'

	def getFilename(self, name):
		return self.filename

	def setFilename(self, name):
		self.filename = '/boot/grub/%s' % name

	def getBootTitle(self, name):
		return self.title

	def setBootTitle(self, name):
		self.title = name

	def getInstallKernel(self, name):
		return self.installKernel

	def setInstallKernel(self, name):
		self.installKernel = name

	def getInstallRamdisk(self, name):
		return self.installRamdisk

	def setInstallRamdisk(self, name):
		self.installRamdisk = name

	def run(self, args=''):
		"""Write the /boot/grub/rocks.conf file. Extra arguments
		are used for frontend Reinstall."""

		original = '/boot/grub/grub-orig.conf'
		if not os.path.exists(original):
			original = '/boot/grub/grub.conf'
		file = open(original, 'r')
		outfile = open(self.filename, 'w')

		saveit = 0
		orig_kernels = []

		for line in file.readlines():
			tokens = string.split(line)

			if tokens[0] == 'kernel':
				kernelpath = os.path.dirname(tokens[1])
				kernelflags = string.join(tokens[2:])
			elif tokens[0] == 'root':
				root = line
			elif tokens[0] != 'title' and tokens[0] != 'initrd' and tokens[0] != 'module':
				# Write the header
				outfile.write(line)

			if tokens[0] == 'title':
				saveit = 1

			if saveit:
				orig_kernels.append(line)

		file.close()

		#
		# write the rocks reinstall grub configuration file
		#
		outfile.write('title %s\n' % self.title)
		outfile.write(root)
		outfile.write('\tkernel %s/%s %s ' \
			% (kernelpath, self.installKernel, kernelflags))
		outfile.write(self.defaultargs)
		if args:
			outfile.write(args)
		outfile.write('\n')
		outfile.write('\tinitrd %s/%s\n' \
			% (kernelpath, self.installRamdisk))

		for line in orig_kernels:
			outfile.write(line)

		outfile.close()
		
		
	def append(self, args):
		"""Append kernel args to an existing grub conf file."""
		
		#
		# append the user-supplied arguments
		#
		gotTitle = 0
		contents = ''

		infile = open(self.filename, 'r')
		for line in infile.readlines():
			if line.count(self.title):
				gotTitle = 1

			l = line.split()

			if gotTitle and len(l) > 1 and l[0] == 'kernel' and \
				(l[1].count('xen') or l[1].count('vmlinuz')):

				contents += "%s %s\n" % (line[:-1], args)
				gotTitle = 0
				continue

			contents += line
		infile.close()
		
		outfile = open(self.filename, 'w')
		outfile.write(contents)
		outfile.close()
			
			

if __name__ == "__main__":
	app=App()
	app.run()
