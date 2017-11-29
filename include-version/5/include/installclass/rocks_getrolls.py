#
# $Id: rocks_getrolls.py,v 1.6 2012/11/27 00:48:01 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWindwer)
# 		         version 7.0 (Manzanita)
# 
# Copyright (c) 2000 - 2017 The Regents of the University of California.
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
# $Log: rocks_getrolls.py,v $
# Revision 1.6  2012/11/27 00:48:01  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.5  2012/10/19 23:11:27  clem
# The "Why did you do that?" saga...
#
# Obviously patching anaconda did not work.
# Python snippet in the kickstart file are still failing (obviously :-()
#
# This time I try upgrading python with the same source code used by the
# original python from RH (heavily patched), let's hope The Force will be
# with me this time...
#
# Revision 1.4  2012/10/19 18:25:50  clem
# Another installment of "Why did you do that?"
#
# Redhat decided to patch python 2.4.3 and to move some function which once where in
# os.py as a built-in methods (this is a python 2.6 code) with no version change
# though.
#
# This obviously messes up when you run foundation-python insde anaconda which has
# the pythonpath pointing to the redhat libraries first.
#
# Here some more description of the bug:
# https://bugzilla.redhat.com/show_bug.cgi?id=750555
#
# Revision 1.3  2012/10/11 23:06:08  clem
# frontend with single partition fixup in anaconda for rocks 5
#
# Revision 1.2  2012/05/06 05:48:10  phil
# Copyright Storm for Mamba
#
# Revision 1.1  2012/02/01 20:44:36  phil
# Moved to include-version tree
#
# Revision 1.9  2011/07/23 02:30:14  phil
# Viper Copyright
#
# Revision 1.8  2010/09/07 23:52:46  bruno
# star power for gb
#
# Revision 1.7  2009/05/01 19:06:48  mjk
# chimi con queso
#
# Revision 1.6  2008/10/31 20:35:25  bruno
# resiliency fix -- try harder (and timeout) when trying to get roll directory
# listings
#
# Revision 1.5  2008/10/18 00:55:45  mjk
# copyright 5.1
#
# Revision 1.4  2008/05/22 21:02:06  bruno
# rocks-dist is dead!
#
# moved default location of distro from /export/home/install to
# /export/rocks/install
#
# Revision 1.3  2008/03/06 23:41:30  mjk
# copyright storm on
#
# Revision 1.2  2008/01/04 21:40:52  bruno
# closer to V
#
# Revision 1.1  2007/12/10 21:28:32  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
#
import os
import os.path
import string
from rhpl.translate import _, N_

import rocks.media
import rocks.roll
import rocks.installcgi
import rocks.file

import logging
log = logging.getLogger("anaconda")


def RocksGetRolls(anaconda):
	#
	# download the selected rolls
	#

	#
	# if there isn't a /tmp/rolls.xml file or if this is a client install,
	# then there is are no rolls to fetch -- so return
	#
	media = rocks.media.Media()

	if not os.path.exists('/tmp/rolls.xml'):
		if media.mounted():
			media.ejectCD()
		return

	#
	# in a default installation, make sure /export points to a partition
	# *not* on the '/' partition
	#
	cwd = os.getcwd()
	os.chdir('/mnt/sysimage')

	if not os.path.exists('state'):
		os.mkdir('state')
	if not os.path.exists('state/partition1'):
		os.mkdir('state/partition1')

	try:
		os.symlink('state/partition1', 'export')
	except:
		pass
	os.chdir(cwd)

	#
	# get the roll list by parsing /tmp/rolls.xml
	#
	generator = rocks.roll.Generator()
	generator.parse('/tmp/rolls.xml')

	cwd = os.getcwd()

	#
	# get all the CD-based rolls first
	#
	diskids = []
	for roll in generator.rolls:
		(name, version, arch, url, diskid) = roll

		if diskid != '' and diskid not in diskids:
			diskids.append(diskid)

	diskids.sort()
	for d in diskids:
		#
		# ask the user to put the right media in the bay
		#
		checkCD(anaconda, media, d)

		#
		# then, for each selected roll on this disk, copy it
		#
		for roll in generator.rolls:
			(name, version, arch, url, diskid) = roll
			if diskid == d:
				downloadRoll(anaconda, roll)

	if media.mounted():
		media.ejectCD()

	#
	# now get all the network rolls
	#
	for roll in generator.rolls:
		(rollname, rollversion, rollarch, rollurl, diskid) = roll

		if diskid != '':
			continue

		downloadRoll(anaconda, roll)

	os.chdir(cwd)

	#
	# rebuild the distro
	#
	w = anaconda.intf.waitWindow(_("Rocks-Dist"),
			 _("Rebuilding the Distribution..."))

	cmd = '/opt/rocks/bin/rocks report distro'
	for line in os.popen(cmd).readlines():
		distrodir = line[:-1]

	rootdir = '/mnt/sysimage/%s' % (distrodir)
	
	path = ''
	try:
		path = os.environ['PATH']
	except:
		pass

	#
	# need this path so rocks-dist uses the 'rpm' binary from the rocks
	# path and not the 'busybox' rpm
	#
	os.environ['PATH'] = '/mnt/runtime/rocks/bin:' + path

	installcgi = rocks.installcgi.InstallCGI(rootdir)
	installcgi.createPopt()
	installcgi.rebuildDistro(generator.rolls)

	#
	# make sure the link to the repository is correct for the package
	# installation portion of the install
	#
	arch = os.uname()[4]
	if arch in ['i386', 'i486', 'i586', 'i686']:
		arch = 'i386'

	os.system('umount /mnt/cdrom')
	os.system('rm -rf /mnt/cdrom')
	dir = '/mnt/sysimage/%s/rocks-dist/%s/' % (distrodir, arch)
	os.system('ln -s %s /mnt/cdrom' % (dir))

	w.pop()

	return


def checkCD(anaconda, media, diskname):
	#
	# check that it is the right roll CD
	#
	found_disk = 'false'
	while found_disk == 'false':
		diskid = media.getId()

		if diskname == diskid:
			found_disk = 'true'

		if found_disk == 'false':
			media.ejectCD()

			anaconda.intf.messageWindow(_("Install Roll"),
				_("Put Roll disk")
					+ " '%s' " % (diskname)
					+ _("in the drive\n"))
	return


def downloadRoll(anaconda, roll):
	(rollname, rollversion, rollarch, rollurl, diskid) = roll

	w = anaconda.intf.waitWindow(_("Downloading"),
			 _("Downloading Roll") + 
			" '%s' " % (rollname))

	#
	# test if this roll is in rocks format
	#
	isrocksroll = 1

	u = string.split(rollurl, '/')
	if len(u) > 2 and u[2] == '127.0.0.1':
		#
		# all CDs and DVDs will have the loopback IP address as the
		# the host name, so let's see if a specific directory exists
		# that will indicate to us if this is a rocks roll or
		# a or 'foreign' roll
		#
		p = os.path.join('/mnt/cdrom', rollname, rollversion, rollarch)
		if not os.path.exists(p):
			isrocksroll = 0

	path = os.path.join(rollname, rollversion, rollarch)

	cmd = '/opt/rocks/bin/rocks report distro'
	for line in os.popen(cmd).readlines():
		distrodir = line[:-1]

	localpath = '/mnt/sysimage/%s/rolls/%s' % (distrodir, path)

	if isrocksroll:
		url = '%s' % os.path.join(rollurl, path)
	else:
		#
		# this is not a rocks roll, so append the keywords 'RedHat'
		# and 'RPMS'  onto the local directory name. this allows us
		# to use CentOS and Scientific Linux CDs
		#
		localpath = os.path.join(localpath, 'RedHat', 'RPMS')

		#
		# change the url to point to the RPMS directory
		#
		cdtree = rocks.file.Tree('/mnt/cdrom')
		dirpath = ''
		for dir in cdtree.getDirs():
			d = string.split(dir, '/')
			if d[-1] == 'RPMS':
				dirpath = dir
				break
		
		url = os.path.join('http://127.0.0.1/mnt/cdrom', dirpath)

	cutdirs = len(string.split(url[7:], '/'))
	if isrocksroll:
		#
		# for rolls in rocks format, make sure we copy all the
		# files from the roll (e.g., 'RedHat' and 'base' directories)
		# this is useful for the kernel roll.
		#
		cutdirs -= 1

	os.system('mkdir -p %s' % localpath)
	os.chdir(localpath)

	if os.path.exists('/tmp/updates/rocks/bin/wget'):
		wget = '/tmp/updates/rocks/bin/wget'
	else:
		wget = '/usr/bin/wget'

	#
	# add resiliency flags to wget
	#
	flags = '--dns-timeout=3 --connect-timeout=3 --read-timeout=10 '
	flags += '--tries=3'

	cmd = '%s -m -nv -np -nH %s --cut-dirs=%d %s' \
		% (wget, flags, cutdirs, url)
	cmd += ' >> /tmp/wget.debug'
	os.system(cmd)

	os.system('echo "%s" >> /tmp/wget.debug' % (cmd))

	w.pop()
	return

