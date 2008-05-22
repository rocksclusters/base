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
# $Log: rebuild.py,v $
# Revision 1.15  2008/05/22 21:02:07  bruno
# rocks-dist is dead!
#
# moved default location of distro from /export/home/install to
# /export/rocks/install
#
# Revision 1.14  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.13  2007/06/23 04:03:24  mjk
# mars hill copyright
#
# Revision 1.12  2006/09/11 22:47:23  mjk
# monkey face copyright
#
# Revision 1.11  2006/08/10 00:09:41  mjk
# 4.2 copyright
#
# Revision 1.10  2006/01/16 06:49:00  mjk
# fix python path for source built foundation python
#
# Revision 1.9  2005/10/12 18:08:42  mjk
# final copyright for 4.1
#
# Revision 1.8  2005/09/16 01:02:21  mjk
# updated copyright
#
# Revision 1.7  2005/07/11 23:51:35  mjk
# use rocks version of python
#
# Revision 1.6  2005/05/24 21:21:57  mjk
# update copyright, release is not any closer
#
# Revision 1.5  2005/03/22 06:46:36  bruno
# added a function to list the SRPMS which have not be built yet
#
# Revision 1.4  2005/03/15 17:06:44  bruno
# cleanup status line
#
# Revision 1.3  2005/03/15 07:06:56  bruno
# be fast
#
# Revision 1.2  2005/03/14 23:21:14  bruno
# added 'self.' to donedir
#
# Revision 1.1  2005/03/01 00:22:08  mjk
# moved to base roll
#
# Revision 1.4  2005/02/22 23:10:46  bruno
# now using generic 'build' script instead of 'build.sh' -- we can use
# any ol' turing machine
#
# Revision 1.3  2005/02/22 21:32:20  bruno
# can now call any program named 'build.sh'
#
# Revision 1.2  2005/02/21 21:22:09  bruno
# now using 'rocks-build' to make all SRPMS
#
# Revision 1.1  2005/02/21 06:43:17  bruno
# the beginning of making a build-rocks.py script
#
#
import os
import os.path
import rpm


class Rebuild:

	def getRebuildPath(self):
		self.rebuild = os.path.join(self.dist.getRootPath(), 'rebuild')
		return self.rebuild


	def __init__(self, dist):
		self.dist = dist

		#
		# where the build state files go (e.g., 'kernel*.src.rpm.done')
		#
		self.donedir = os.path.join(self.getRebuildPath(), 'spool',
			self.dist.getProductRelease(),
			self.dist.getLang(), 'os', self.dist.getArch())
		if not os.path.exists(self.donedir):
			os.makedirs(self.donedir)

		#
		# location of the patch scripts (e.g., 'kernel/build')
		#
		self.patchdir = os.path.join(self.getRebuildPath(), 'patches')

		#
		# where all the built binary RPMS will go
		#
		self.completedir = os.path.join(self.getRebuildPath(),
			self.dist.getProductRelease(),
			self.dist.getLang(), 'os', self.dist.getArch(),
				'RedHat')
		if not os.path.exists(self.completedir):
			os.makedirs(self.completedir)

		#
		# support data structures that allow us to query individual
		# RPM and SRPM packages
		#
		self.ts = rpm.ts()
		self.ts.setVSFlags(rpm._RPMVSF_NOSIGNATURES)

		return


	def displayStatusLine(self, cmd, logfile):
		import sys

		log = open(logfile, 'w')

		r = os.popen(cmd, 'r')

		currLength = 0
		prevLength = 0

		while 1:
			l = r.readline()
			log.write(l)

			if not l:
				break

			line = l.expandtabs()

			if len(line) > 79:
				data = line[0:78]
			else:
				data = line[:-1]

			currLength = len(data)
			pad = ''
			for i in range(0, prevLength - currLength):
				pad = pad + ' '
			prevLength = currLength

			print data + pad + '\r',
			sys.stdout.flush()

		log.close()

		retval = r.close()
		if retval == None:
			print '          Success' + '\r'
		else:
			print

		return retval


	def getDistribution(self, rname):
		try:
			fdno = os.open(rname.getFullName(), os.O_RDONLY)
			rpminfo = self.ts.hdrFromFdno(fdno)
			os.close(fdno)
			distro = rpminfo[rpm.RPMTAG_DISTRIBUTION]
		except:
			distro = None
			pass
				
		return distro


	def getPackager(self, rname):
		try:
			fdno = os.open(rname.getFullName(), os.O_RDONLY)
			rpminfo = self.ts.hdrFromFdno(fdno)
			os.close(fdno)
			packager = rpminfo[rpm.RPMTAG_PACKAGER]
		except:
			packager = None
			pass

		return packager


	def getSourceRPM(self, rname):
		try:
			fdno = os.open(rname.getFullName(), os.O_RDONLY)
			rpminfo = self.ts.hdrFromFdno(fdno)
			os.close(fdno)
			sourcerpm = rpminfo[rpm.RPMTAG_SOURCERPM]
		except:
			sourcerpm = None
			pass

		return sourcerpm


	def getRequires(self, rname):
		try:
			fdno = os.open(rname.getFullName(), os.O_RDONLY)
			rpminfo = self.ts.hdrFromFdno(fdno)
			os.close(fdno)
			requires = rpminfo[rpm.RPMTAG_REQUIRES]
			print 'requires: ', requires
		except:
			requires = None
			pass

		return requires


	#
	# the commands
	#
	def buildYumRepository(self):
		print 'Building Yum Repository'
		cmd = 'yum-arch -l %s' % (self.dist.getReleasePath())
		os.system(cmd)
		
		return


	def touchRocksBuiltPackages(self):
		for rname in self.dist.getRPMS():
			packager = self.getPackager(rname)
			distro = self.getDistribution(rname)

			if (packager == 'Rocks' or distro == 'Rocks') \
						or \
					(packager == [] and distro == []): 

				cmd = 'touch %s/%s.done' % (self.donedir,
						self.getSourceRPM(rname))
				os.system(cmd)
			
		return


	def installRequiredPackages(self):
		#
		# look through all the source RPMS. if a source RPM doesn't
		# have a '.done' file, then it still needs to be built
		#
		# before we try to build it, make sure all it's required
		# binary RPMS are installed
		#
		reqlist = []	
		for rname in self.dist.getSRPMS():
			donefile = os.path.join(self.donedir,
						rname.getName() + '.done')
			if not os.path.exists(donefile):
				requires = self.getRequires(rname)

				#
				# sometimes a requirement is for a file
				# rather than a package -- skip 'file'
				# requirements
				#
				if requires == None or requires[0] == '/':
					continue

				for req in requires:
					if req[0:7] == 'rpmlib(':
						continue

					if req not in reqlist:
						reqlist.append(req)

		for req in reqlist:
			cmd = 'yum install %s' % (req)
			print 'installRequiredPackages:cmd:',cmd
			os.system(cmd)

		return


	def validateBuiltPackages(self):
		#
		# make sure we built all the packages
		#
		for rname in self.dist.getRPMS():
			try:
				packager = self.getPackager(rname)
				distro = self.getDistribution(rname)

				if (packager == [] and distro == []) \
						or \
					(packager == None and distro == None):

					continue

				if packager != 'Rocks' and distro != 'Rocks':
					print '%s' % (rname.getName())
					print '\tbuilt by: %s' % (packager)
					print '\t\tfrom distribution: %s\n' \
						% (distro)
			except:
				pass

		return


	def buildPackage(self, pkg):
		import rocks.build

		cmd = ''

		#
		# look for general patch file (e.g., 'kernel/build')
		#
		p = os.path.join(self.patchdir, pkg.getBaseName(), 'build')
		if os.path.exists(p):
			cmd = '%s' % (p)

		#
		# look for a specific patch file (full SRPM name)
		#
		p = os.path.join(self.patchdir, pkg.getName(), 'build')
		if os.path.exists(p):
			cmd = '%s' % (p)

		if cmd == '':
			cmd = 'rpmbuild --rebuild %s' % (pkg.getFullName())
		else:
			cmd = 'ROCKS_REBUILD_SRPM=%s %s' % \
							(pkg.getFullName(), cmd)

		#
		# prep the environment
		#
		os.system('rm -rf /usr/src/redhat/SOURCES/*')
		os.system('rm -rf /usr/src/redhat/SPECS/*')
		os.system('rm -rf /usr/src/redhat/BUILD/*')
		os.system('rm -rf /usr/src/redhat/RPMS/*')
		os.system('rm -rf /usr/src/redhat/SRPMS/*')

		logfile = os.path.join(self.donedir, pkg.getName() + '.log')
		donefile = os.path.join(self.donedir, pkg.getName() + '.done')

		print 'Building: %s' % (pkg.getName())
		cmd += ' 2>&1 '

		if self.displayStatusLine(cmd, logfile) == None:
			#
			# the command was successful, touch the .done file
			#
			os.system('touch %s' % (donefile))

		#
		# copy over the resulting built binary packages (if any)
		#
		cmd = 'cp -Rp /usr/src/redhat/RPMS/ %s' % (self.completedir)
		os.system(cmd)

		return


	def getNotDone(self):
		import stat

		list = []

		for rname in self.dist.getSRPMS():
			buildit = 0

			if rname.getName()[-7:] != 'src.rpm':
				continue

			srpmdone = os.path.join(self.donedir,
						rname.getName() + '.done')
			if not os.path.exists(srpmdone):
				list.append(rname)
			else:
				#
				# check the timestamps
				#
				srpmdone_mtime = os.stat(srpmdone) \
								[stat.ST_MTIME]
				srpm_mtime = os.stat(rname.getFullName()) \
								[stat.ST_MTIME]

				if srpm_mtime > srpmdone_mtime:
					#
					# if the SRPM is newer than its '.done'
					# file, then rebuild it
					#
					list.append(rname)

		return list


	def getMissing(self):
		list = []
		for rpm in self.getNotDone():
			list.append(rpm.getName())

		return list


	def rebuildPackages(self):
		for rpm in self.getNotDone():
			self.buildPackage(rpm)
				
		return

