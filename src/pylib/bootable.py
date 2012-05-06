#! /opt/rocks/bin/python
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
# $Log: bootable.py,v $
# Revision 1.29  2012/05/06 05:48:46  phil
# Copyright Storm for Mamba
#
# Revision 1.28  2011/07/23 02:30:49  phil
# Viper Copyright
#
# Revision 1.27  2010/09/07 23:53:08  bruno
# star power for gb
#
# Revision 1.26  2009/05/01 19:07:08  mjk
# chimi con queso
#
# Revision 1.25  2008/10/18 00:56:02  mjk
# copyright 5.1
#
# Revision 1.24  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.23  2007/12/10 21:28:35  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.22  2007/06/23 04:03:24  mjk
# mars hill copyright
#
# Revision 1.21  2006/09/11 22:47:22  mjk
# monkey face copyright
#
# Revision 1.20  2006/08/10 00:09:40  mjk
# 4.2 copyright
#
# Revision 1.19  2006/07/19 19:20:25  bruno
# removed all traces to mount-loop and umount-loop
#
# Revision 1.18  2006/06/21 03:09:53  bruno
# updates to put the frontend networking info in the database just like
# a compute node
#
# Revision 1.17  2006/06/05 17:57:37  bruno
# first steps towards 4.2 beta
#
# Revision 1.16  2006/01/25 22:22:56  bruno
# compute nodes build again
#
# Revision 1.15  2006/01/21 04:06:49  mjk
# new foundation
#
# Revision 1.14  2006/01/16 06:48:59  mjk
# fix python path for source built foundation python
#
# Revision 1.13  2005/12/31 07:08:34  mjk
# add rocks-kpp package
#
# Revision 1.12  2005/10/12 18:08:42  mjk
# final copyright for 4.1
#
# Revision 1.11  2005/09/16 01:02:21  mjk
# updated copyright
#
# Revision 1.10  2005/07/27 01:54:38  bruno
# checkpoint
#
# Revision 1.9  2005/07/11 23:51:35  mjk
# use rocks version of python
#
# Revision 1.8  2005/06/30 19:16:17  bruno
# patch netstg2.img in kernel roll, not with rocks-dist.
#
# this means the --public and --notouch flags are gone.
#
# Revision 1.7  2005/05/24 21:21:57  mjk
# update copyright, release is not any closer
#
# Revision 1.6  2005/05/23 23:16:00  bruno
# got bootable ISOs back
#
# Revision 1.5  2005/04/08 23:17:48  fds
# Dummy comps.rpm file in bootable rolls for installer
#
# Revision 1.4  2005/03/23 20:50:34  bruno
# fix to find local packages regardless of what directory you're in
#
# Revision 1.3  2005/03/21 23:46:30  bruno
# everything's a roll support added
#
# Revision 1.2  2005/03/02 21:19:02  bruno
# don't install rocks-kickstart-profiles -- it doesn't exist anymore
#
# Revision 1.1  2005/03/01 00:22:08  mjk
# moved to base roll
#
# Revision 1.4  2004/12/13 14:43:31  bruno
# if a roll is bootable, then try to get the kernel RPMS locally first.
#
# if there are no local kernel RPMS, then look in the distro.
#
# Revision 1.3  2004/11/23 04:27:16  bruno
# really make it architecturally neutral
#
# Revision 1.2  2004/11/23 04:15:47  bruno
# make it architecturally neutral
#
# Revision 1.1  2004/11/23 02:43:19  bruno
# added support to make any roll bootable.
#
# to make a roll bootable, just add the following line to version.mk in
# the home directory of a roll:
#
# 	BOOTABLE = 1
#
#

#
# make any media bootable
#
import os
import shutil
import tempfile
import rocks.dist
import rocks.file
import rocks.util


class Bootable:

	def __init__(self, dist):
		self.dist = dist

		#
		# build a list of CPUs, from 'best' to 'worst' match
		#

		#
		# the 'native' cpu is always first
		#
		self.cpus = []
		i86cpus = [ 'i686', 'i586', 'i486', 'i386' ]

		native = os.uname()[4]
		self.cpus.append(native)

		if native in i86cpus:
			self.cpus += i86cpus

		self.cpus.append('noarch')
		return


	def getBestRPM(self, name):
		r = self.dist.getRPM(name)
		if r == None:
			return None
			
		rpm = None

		if len(r) == 1:
			rpm = r[0]
		elif len(r) > 1:
			print 'found more than one RPM for %s' % (name)

			for c in self.cpus:
				for i in r:
					if i.getPackageArch() == c:
						rpm = i
						break

				if rpm:
					print '\tusing %s' % \
							rpm.getUniqueName()
					break
			
		return rpm


	def applyRPM(self, rpm, root, flags=''):
		"""Used to 'patch' the new distribution with RPMs from the
		distribution.  We use this to always get the correct
		genhdlist, and to apply eKV to Rocks distributions.
        
		Throws a ValueError if it cannot find the specified RPM, and
		BuildError if the RPM was found but could not be installed."""

		dbdir = os.path.join(root, 'var', 'lib', 'rpm')

		os.makedirs(os.path.join(root, dbdir))
		reloc = os.system("rpm -q --queryformat '%{prefixes}\n' -p " +
			rpm.getFullName() + "| grep none > /dev/null")

		cmd = 'rpm -i --nomd5 --force --nodeps --ignorearch ' + \
			'--dbpath %s ' % (dbdir)
		if reloc:
			cmd = cmd + '--prefix %s %s %s' % (root, flags,
							rpm.getFullName())
		else:
			cmd = cmd + '--badreloc --relocate /=%s %s %s' \
					% (root, flags, rpm.getFullName())

		retval = os.system(cmd + ' > /dev/null 2>&1')
		shutil.rmtree(os.path.join(root, dbdir))

		if retval == 256:
			raise ValueError, "could not apply RPM %s" % \
				(rpm.getFullName())

		return retval


	def patchImage(self, image_name):
		#
		# image_name = full pathname to stage2.img file
		#
		cwd = os.getcwd()

		# Create a scratch area on the local disk of the machine, we
		# don't want to do this in the distribution since it might be
		# over NFS (not a problem, just slow).
        
		tmp = tempfile.mktemp()
		os.makedirs(tmp)

		stageimg = os.path.join(tmp, 'img')	# uncompress img
		stagemnt = os.path.join(tmp, 'mnt')	# mounted image
		stagesrc = os.path.join(tmp, 'src')	# working image
		os.makedirs(stagemnt)

		# - uncompress the the 2nd stage image from the distribution
		# - mount the file on the loopback device
		#	(requires SUID 'C' code)
		# - copy all file into the working images
		# - umount the loopback device

		shutil.copy(image_name, stageimg)

		os.system('mount -oloop -t squashfs %s %s' %
			(stageimg, stagemnt))

		os.chdir(stagemnt)
		os.system('find . | cpio -pdu %s 2> /dev/null' % stagesrc)
		os.chdir(cwd)

		os.system('umount %s' % stagemnt)

		# Stamp the new image with our likeness so the new loader
		# will "verify" its authenticity. This stamp must be repeated
		# in an identical file in the initrd.

		stamp = open(os.path.join(stagesrc, ".buildstamp"), "w")
		stamp.write("Rocks-RedHat\n")
		stamp.close()

		# - create a new image file based on the size of the
		#	working image
		# - mount the file on loopback
		# - copy the working image into the mounted images
		# - umount the file
		# - compress, and copy, the image back into the distribution

		print '    building CRAM filesystem ...'
		os.system('mkcramfs %s %s > /dev/null' % \
			(stagesrc, image_name))

		# Erase the evidence.
		shutil.rmtree(tmp)
		return


	def installBootfiles(self, destination):
		name = 'rocks-boot-cdrom'
		RPM = self.getBestRPM(name)
		if not RPM:
			raise ValueError, "could not find %s" % name

		self.applyRPM(RPM, destination)
		return


	def copyBasefiles(self, destination):
		if not os.path.exists(destination):
			os.makedirs(destination)
		basepath = os.path.join(self.dist.getPath(), 'RedHat', 'base')
		cmd = 'cp %s/* %s' % (basepath, destination)
		os.system(cmd)
		os.system('touch %s/comps.rpm' % destination)
		return


	def installNetstage(self, destination):
		cmd = 'rm -f %s/stage2.img' % (destination)
		os.system(cmd)

		name = 'rocks-boot-netstage'
		RPM = self.getBestRPM(name)
		if not RPM:
			raise ValueError, "could not find %s" % name

		self.applyRPM(RPM, destination)

		name = 'rocks-anaconda-updates'
		RPM = self.getBestRPM(name)
		if not RPM:
			raise ValueError, "could not find %s" % name

		self.applyRPM(RPM, destination)

		#
		# put product.img in the ISO
		#
		shutil.copy('%s/images/product.img' % (self.dist.getPath()),
			'%s/images' % (destination))

		return

