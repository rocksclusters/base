#! /opt/rocks/bin/python
#
# $Id: kcgi.py,v 1.36 2009/07/16 22:46:28 bruno Exp $
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
# $Log: kcgi.py,v $
# Revision 1.36  2009/07/16 22:46:28  bruno
# support for cross-kickstarting
#
# Revision 1.35  2009/05/09 16:06:38  bruno
# support for lights out frontend installs
#
# Revision 1.34  2009/05/08 02:35:20  bruno
# need a couple more attributes to build a frontend VM
#
# Revision 1.33  2009/05/01 19:07:07  mjk
# chimi con queso
#
# Revision 1.32  2009/02/11 19:26:46  bruno
# kickstart.cgi now uses the 'wan' node instead of the 'server-wan' node for
# public kickstarting
#
# Revision 1.31  2009/01/08 01:20:58  bruno
# for anoop
#
# Revision 1.30  2008/12/19 21:08:54  mjk
# - solaris jgen code looks more like linux kgen code now
# - removed solaris <part> tag (outside of <main> section)
# - everything using cond now (arch,os are converted)
# - cond now works inside node files also
# - conditional edges work on linux, needs testing on solaris
#
# Revision 1.29  2008/12/18 22:31:21  mjk
# - kickstarting set node attributes for later checks
#
# Revision 1.28  2008/10/18 00:56:01  mjk
# copyright 5.1
#
# Revision 1.27  2008/07/22 00:34:41  bruno
# first whack at vlan support
#
# Revision 1.26  2008/07/02 17:34:08  bruno
# fix for central installs
#
# Revision 1.25  2008/03/06 23:41:43  mjk
# copyright storm on
#
# Revision 1.24  2007/12/10 21:28:35  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.23  2007/06/23 04:03:23  mjk
# mars hill copyright
#
# Revision 1.22  2007/05/30 22:55:52  anoop
# *** empty log message ***
#
# Revision 1.21  2007/02/28 03:06:29  mjk
# - "rocks list host xml" replaces kpp
# - kickstart.cgi uses "rocks list host xml"
# - indirects in node xml now works
#
# Revision 1.20  2006/09/11 22:47:16  mjk
# monkey face copyright
#
# Revision 1.19  2006/08/10 00:09:37  mjk
# 4.2 copyright
#
# Revision 1.18  2006/01/16 06:48:58  mjk
# fix python path for source built foundation python
#
# Revision 1.17  2005/12/09 18:32:11  bruno
# if there is an XML parse error, catch the exception then continue in order
# to correctly increment the 'load counter'.
#
# Revision 1.16  2005/10/12 18:08:39  mjk
# final copyright for 4.1
#
# Revision 1.15  2005/10/09 19:30:13  bruno
# add a bit of defensive programming
#
# Revision 1.14  2005/10/09 19:20:14  bruno
# change the kickstart.cgi load throttling code into a counting semaphore.
# initialize the semaphore to the number of CPUs on the frontend multiplied by 2.
# as the number of CPUs on the frontend increases, we'll be able to support
# more concurrent executions of kpp.
#
# also, create an init script that removes the kickstart.cgi.lck file every
# time the service is started/stopped. this ensures a frontend reboot will
# reset the state of the throttling code.
#
# Revision 1.13  2005/10/08 18:15:39  bruno
# dynamically create the kickstart.cgi.lck lock file
#
# Revision 1.12  2005/10/04 16:45:54  bruno
# compute nodes now run kgen to produce the final kickstart file.
#
# Revision 1.11  2005/09/29 03:35:05  phil
# Fixes runaway python on the server when running kickstart.cgi
# a) tracking the number of generating kickstarting instances using a lockfile as a monitor (does not fail if lockfile is missing or unreadable)
# b) properly generate headers for 503 errors and add Retry-Time: directive to the header
#
# This allows even slow frontends to install complete racks without
# being brought to its knees.
#
# Still need to experiment with the number of concurrent generators on older
# boxen.
#
# Revision 1.10  2005/09/16 01:02:19  mjk
# updated copyright
#
# Revision 1.9  2005/07/11 23:51:35  mjk
# use rocks version of python
#
# Revision 1.8  2005/05/27 20:56:17  fds
# Ignore file open errors in certain cases.
#
# Revision 1.7  2005/05/24 21:28:39  fds
# Access works with new dist.py. Use rocks.clusterdb when acting for shepherd:
# one way to insert nodes into database, that does full duplicate checking.
#
# Revision 1.6  2005/05/24 21:21:54  mjk
# update copyright, release is not any closer
#
# Revision 1.5  2005/05/24 16:49:09  mjk
# kickstart works again
#
# Revision 1.4  2005/05/23 23:59:23  fds
# Frontend Restore
#
# Revision 1.3  2005/05/06 00:16:14  fds
# fixed small python bug.
#
# Revision 1.2  2005/03/10 19:29:32  fds
# Fix from Matt Wise's problem description. Allow access to ip as well
# as name for WAN kickstarts.
#
# Revision 1.1  2005/03/01 02:02:48  mjk
# moved from core to base
#
# Revision 1.85  2005/02/11 23:38:16  mjk
# - blow up the bridge
# - kgen and kroll do actually work (but kroll is not complete)
# - file,roll attrs added to all tags by kpp
# - gen has generator,nodefilter base classes
# - replaced rcs ci/co code with new stuff
# - very close to adding rolls on the fly
#
# Revision 1.84  2004/11/02 00:41:27  fds
# Support for wan-all-access. Used for centrals, public frontends.
#
# Revision 1.83  2004/10/16 03:56:08  fds
# Validated kickstart nacks on rockstar
#
# Revision 1.82  2004/10/04 19:21:41  fds
# More info to syslog on node insert
#
# Revision 1.81  2004/09/14 01:06:05  fds
# More proper; allows membership in an external cgi request.
#
# Revision 1.80  2004/09/14 00:51:49  fds
# Dont barf on --membership.
#
# Revision 1.79  2004/09/11 01:01:41  fds
# Log node inserts to syslog
#
# Revision 1.78  2004/09/07 23:25:13  fds
# Kickstart gets its load threshold from config file.
#
# Revision 1.77  2004/08/26 23:12:34  fds
# Passing client IP for shepherd.
#
# Revision 1.76  2004/08/21 00:23:13  fds
# Make sure Node_Hostname is set when coming in on a cert.
#
# Revision 1.75  2004/08/17 22:38:06  fds
# Open WAN access earlier.
#
# Revision 1.74  2004/08/16 21:29:55  fds
# The node/networks table duplicate the node 'name'. This is
# not normalized, and makes it harder to change the name. We do
# it to make it easier for dbreports/ConfigNetworks, but still a bad idea.
#
# Revision 1.73  2004/08/13 19:58:26  fds
# Support for cluster shepherd.
#
# Revision 1.72  2004/07/28 22:33:02  fds
# Tweak
#
# Revision 1.71  2004/07/13 19:14:21  fds
# Secure kickstart
#
# Revision 1.70  2004/07/01 22:09:20  fds
# Making per-client wan access directories.
#
# Revision 1.69  2004/06/30 22:50:08  fds
# New form. Kickstart.cgi is put in /home/install/sbin now, for various
# security-related reasons. kcgi knows about 'wan' and 'lan' distros, and
# has a new --dist flag.
#
# Revision 1.68  2004/05/26 18:26:52  fds
# Send nacks when we get busy to insure progress on large parallel installs.
#
# Revision 1.67  2004/04/27 04:38:48  bruno
# added ability to just print out 'pre' section.
#
# Revision 1.66  2004/04/20 04:03:50  fds
# Man you have to watch this guy! He's a loose cannon, never tests his code,
# never thinks, just commits. Commit, always commit. Then of course its our job
# to pick up the pieces... ;)
#
# Revision 1.65  2004/04/06 22:32:06  mjk
# dns aliases are gone for some reason
#
# Revision 1.64  2004/03/25 03:15:41  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.63  2004/03/24 01:36:33  fds
# Better error message.
#
# Revision 1.62  2004/03/24 01:30:10  fds
# kcgi now uses the rocks-dist in install/external to make the initial
# wan kickstart file. This helps if you are on a central and are doing
# 'rocks-dist central' alot during development.
#
# Revision 1.61  2004/03/19 03:24:50  bruno
# updates to support new directory structure for XML files
#
# Revision 1.60  2004/03/12 19:37:15  fds
# Better error handling of bad distributions.
#
# Revision 1.59  2004/03/11 21:41:38  fds
# Adopt mason's new rocks-dist capabilities. Allows a much cleaner WAN
# kickstart. Also added the ability to choose the distro name on central.
#
# Revision 1.58  2004/03/03 19:36:36  fds
# Changes for cross-kickstarting
#
# Revision 1.57  2004/02/12 23:42:31  fds
# Handling DNS failure better.
#
# Revision 1.56  2004/02/06 17:46:43  fds
# Removed --membership from kpp commands.
#
# Revision 1.55  2004/02/02 21:09:18  fds
# Simpler for WAN installs, more logic in node files.
#
# Revision 1.54  2004/02/02 18:37:03  fds
# Support for Wide Area installs. New wanKickstart() method in kcgi issues
# a small ks file with external roll url followed by the installclass, and
# thats it.
#
# Kgen now knows how to only output the installclass.
#
# I dont love this code, but it is the first step.
#
# Revision 1.53  2004/01/31 20:21:47  bruno
# needed to explicitly set the architecture.
#
# this is in support of kickstarting multiple different architectures from
# a single frontend.
#
# thanks to roy dragseth for the bug report and the unit test.
#
# Revision 1.52  2003/10/02 20:04:17  fds
# Fixes for 9
#
# Revision 1.50  2003/09/28 19:44:35  fds
# Using the rocks.kickstart Application baseclass. Simpler.
#
# Revision 1.49  2003/09/27 00:15:14  fds
# Using rocks.build to find our way around local distro.
#
# Revision 1.48  2003/09/22 23:24:14  fds
# Simpler Copyright structure, works with insert-copyright.py
#
# Revision 1.47  2003/09/16 18:08:44  fds
# Using KickstartError in trinity. Errors go to stderr.
#
# Revision 1.46  2003/08/27 17:22:59  mjk
# - Fixed proxy kickstart (--client now works for testing)
# - Turned on glisten service
#
# Revision 1.45  2003/08/26 22:44:20  mjk
# - File tag now takes "expr" attribute (command evaluation)
# - Conversion of old code to file tags
# - Added media-server (used to be server)
# - Killed replace-server on the hpc roll
# - Updated Server database membership (now a media-server)
# - Added Public field to the membership table
# - Insert-ethers only allows a subset of memberships (Public ones) to be
#   inserted.
# - Added getArch() to Application class
# - Kickstart trinity (kcgi,kpp,kgen) all updated self.arch initial value
#
# Revision 1.44  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.43  2003/08/15 21:07:26  mjk
# - RC files only built one per directory (fixed)
# - Default CGI arch is native (used to be i386)
# - Added scheduler,nameservices to rocksrc.xml
# - insert-ethers know what scheduler and nameservice we use
# - I forget what else
#
# Revision 1.42  2003/08/14 17:38:38  mjk
# AW fixes
#
# Revision 1.41  2003/06/18 23:53:27  mjk
# all checked in now, promise
#
# Revision 1.40  2003/06/10 19:39:47  mjk
# handles hostname aliases
#
# Revision 1.39  2003/06/03 22:22:32  mjk
# repair --membership bug (maybe)
#
# Revision 1.38  2003/05/29 20:55:19  mjk
# gateway added to kickstart.cgi
#
# Revision 1.37  2003/05/22 16:36:35  mjk
# copyright
#
# Revision 1.36  2003/04/24 23:22:07  mjk
# might fix everything
#
# Revision 1.35  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.34  2002/10/28 22:48:08  bruno
# added path to kpp and kgen
#
# Revision 1.33  2002/10/28 20:16:20  mjk
# Create the site-nodes directory from rocks-dist
# Kill off mpi-launch
# Added rocks-backup
#
# Revision 1.32  2002/10/18 21:33:26  mjk
# Rocks 2.3 Copyright
#
# Revision 1.31  2002/10/10 21:23:09  bruno
# more opt problems
#
# Revision 1.30  2002/10/10 00:54:52  mjk
# Added close() to the database after using it
#
# Revision 1.29  2002/10/09 21:05:14  bruno
# we can now build a cdrom again (after source tree reorganization)
#
# Revision 1.28  2002/10/04 19:27:19  fds
# Checking for np=P CGI variable, and inserting it into the DB.
#
# Revision 1.27  2002/06/11 20:20:28  mjk
# Added support for release tag
#
# Revision 1.26  2002/02/25 19:51:50  mjk
# - Changed default kcgi membership from "External" to "Laptop"
# - Fixed NFS appliance default data
# - Added database access for frontend-0 (or whatever it's named)
#
# Revision 1.25  2002/02/25 19:08:43  mjk
# Negative package resolution for CDROM and CGI kickstart generation.  I
# lost a single line of python code in kpp that fixed this but it didn't
# get checked in.  Backed out of Greg's code and fixed my screw up.
#
# Revision 1.22  2002/02/14 02:12:29  mjk
# - Removed CD copy gui code from insert-ethers
# - Added CD copy code back to install.xml (using rocks-dist)
# - Added copycd command to rocks-dist
# - Added '-' packages logic to kgen
# - Other file changed to support above
#
# Revision 1.21  2002/02/12 23:48:51  mjk
# - Broken (just a checkpoint)
#
# Revision 1.20  2002/02/08 21:50:36  mjk
# Add cfengine support (don't ask why).
#
# Revision 1.19  2002/01/18 23:27:58  bruno
# updates for 7.2
#
# Revision 1.18  2001/12/18 20:05:53  mjk
# Portal changes
#
# Revision 1.17  2001/11/24 21:09:20  bruno
# changed content type to "application/octet-stream" to try to kill the ol'
# "i can't save the kickstart file" whine.
#
# Revision 1.16  2001/11/21 01:47:56  bruno
# you know, it's the little things that totally hose a distribution
#
# Revision 1.15  2001/11/20 23:41:02  bruno
# small fixes for 2.1.1
#
# Revision 1.14  2001/11/09 23:50:53  mjk
# - Post release ia64 changes
#
# Revision 1.13  2001/11/09 00:19:02  mjk
# ia64 changes
#
# Revision 1.12  2001/11/08 23:39:54  mjk
# --host changes to kcgi
#
# Revision 1.11  2001/10/30 23:39:19  mjk
# killed arch column in db
#
# Revision 1.10  2001/10/24 00:17:44  mjk
# typo
#
# Revision 1.9  2001/10/24 00:15:47  mjk
# - Working on new kickstart form
#
# Revision 1.8  2001/10/19 22:11:36  mjk
# getting ready for php webform
#
# Revision 1.7  2001/10/18 20:06:45  mjk
# Changes groups table to memberships
#
# Revision 1.6  2001/10/02 03:16:38  mjk
# - Update to bruno's new auto-part stuff
# - Doesn't work but checkin anyway
#
# Revision 1.5  2001/09/21 18:36:53  mjk
# - Fixed multiple swapfiles
# - Added models CGI (and genmodel.py)
# - Kickstart CGI now accepts form data
# - Fixed turning off services (kudzu, et al)
#
# Revision 1.4  2001/09/14 21:45:42  mjk
# - Testing on ia32 compute nodes
# - A CGI kickstart takes 5 seconds
# - Working on ia64 compute nodes
#
# Revision 1.3  2001/09/10 18:26:38  mjk
# *** empty log message ***
#
# Revision 1.2  2001/09/05 00:27:15  mjk
# main and packages section is correct for compute nodes
#
# Revision 1.1  2001/08/21 01:52:38  mjk
# - <module> tag now prevent multiple inclusion
# - add dot support (ATT graph tool, just changed to GNU, we ship it now)
# - moved kickstart.cgi from rocks-dist RPM over here (called kcgi.py)
# - added <tree><node> tags
#

import os
import fcntl
import sys
import cgi
import xml
import string
import socket
import syslog
import rocks.util
import rocks.kickstart
import rocks.clusterdb
import re
from xml.sax import saxutils
from xml.sax import handler
from xml.sax import make_parser
from rocks.util import KickstartError


class App(rocks.kickstart.Application):

	def __init__(self, argv):
		rocks.kickstart.Application.__init__(self, argv)
		self.usage_name		= 'Kickstart CGI'
		self.usage_version	= '5.0'
		self.form		= cgi.FieldStorage()
		# The max number of simultaneous instances of this script.
		self.loadThresh		= 10
		self.privateNetmask	= ''
		self.allAccess		= 0
		self.doRestore		= 0
		self.clusterdb		= rocks.clusterdb.Nodes(self)
		self.lockFile		= '/var/tmp/kickstart.cgi.lck'

		# Lookup the hostname of the client machine.

		caddr = None
		if self.form.has_key('client'):
			caddr = self.form['client'].value
		elif os.environ.has_key('REMOTE_ADDR'):
                	caddr = os.environ['REMOTE_ADDR']

		self.clientName = None
		self.clientList = []
		try:
			host = socket.gethostbyaddr(caddr)
			self.clientList.append(host[0])	# hostname
			self.clientList.extend(host[1])	# aliases
			self.clientList.extend(host[2])	# ip address
		except:
			self.clientList.append(caddr)

		# Default to native architecture and try to pick up the
		# correct value from the form.
		
		if self.form.has_key('arch'):
			self.arch = self.form['arch'].value

			
		# If the node reported the number of CPUs it has, record it.
		if self.form.has_key('np'):
			self.cpus = self.form['np'].value
		else:
			self.cpus = None

		# What generator should we use.  Defualt to kickstart,
		# could be cfengine.

		if self.form.has_key('generator'):
			self.generator = self.form['generator'].value
		else:
			self.generator = 'kgen'

		if self.form.has_key('membership'):
			self.membership = self.form['membership'].value
		else:
			self.membership = None

		self.distname = None

		# Set to change the default search path for kpp and kgen.

		self.helperpath = os.path.join(os.sep, 'opt', 'rocks', 'sbin')
			
		# Add application flags to inherited flags
		self.getopt.s.extend([('c:', 'client')])
		self.getopt.l.extend([('arch=', 'arch'),
				      ('client=', 'client'),
				      ('membership=', 'group-name'),
				      ('loadthresh=', 'max siblings'),
				      ('dist=', 'distribution'),
				      ('wan-all-access'),
				      ('restore'),
				      ('public')])
		

	def parseArg(self, c):
		if rocks.kickstart.Application.parseArg(self, c):
			return 1
		elif c[0] in ('-c', '--client'):
			self.clientList = [ c[1] ]
			try:
				caddr = socket.gethostbyname(c[1])
				self.clientList.append(caddr)
			except:
				pass
			self.clientName = c[1]
		elif c[0] == '--membership':
			self.membership = c[1]
		elif c[0] == '--public':
			self.public = 1
		elif c[0] == '--loadthresh':
			self.loadThresh = int(c[1])
		elif c[0] == '--dist':
			self.distname = c[1]
		elif c[0] == '--wan-all-access':
			self.allAccess = 1
		elif c[0] == '--restore':
			self.doRestore = 1


	def trailer(self):
		out = []
		out.append('#</pre></body></html>')
		return out


	def getNodeName(self, id):
		self.execute("""select networks.name from networks,subnets
			where node = %d and subnets.name = 'private' and
			networks.subnet = subnets.id and
			(networks.device is NULL or
			networks.device not like 'vlan%%') """ % id)
		try:
			name, = self.fetchone()
		except TypeError:
			name = 'localhost'
		return name


	def getCopyright(self):
		copyright="""#
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
# @Copyright@"""
		return string.split(copyright, "\n")


	def name2coord(self, name):
		"""Extracts the physical coordinates from a node name"""

		pat="-(?P<Rack>\d+)-(?P<Rank>\d+)$"
		coord = re.compile(pat)
		m = coord.search(name)
		if not m:
			raise KickstartError, \
				"Could not find coords of node %s" % name
		else:
			return (m.group('Rack'), m.group('Rank'))
		

	def getMembershipId(self, name):
		try:
			self.execute("select id from memberships "
				"where name='%s'" % name)
			return self.fetchone()[0]
		except:
			raise KickstartError, \
				"Could not find membership %s" % name


	def insertNode(self):
		"""Checks if request has been authenticated with a 
		valid certificate. If so, inserts node into database."""

		errorMsg = "Client %s is internal, not in database, " \
			"and not authenticated." % self.clientList

		if not os.environ.has_key('SSL_CLIENT_VERIFY'):
			raise KickstartError, errorMsg

		if os.environ['SSL_CLIENT_VERIFY'] != 'SUCCESS':
			raise KickstartError, errorMsg
			
		dn = os.environ['SSL_CLIENT_S_DN']
		ip = name = membership = None
		nameKey = 'CN='
		membershipKey = 'CN=RocksMembership:'
		ipKey = 'CN=RocksPrivateAddress:'
		for element in dn.split('/'):
			if element.count(membershipKey):
				membership = element[len(membershipKey):]
			elif element.count(ipKey):
				ip = element[len(ipKey):]
			elif element.count(nameKey):
				name = element[len(nameKey):]

		if not ip or not name or not membership:
			raise KickstartError, "Client has a malformed cert"
		rack, rank = self.name2coord(name)
		mid = self.getMembershipId(membership)

		# Act like insert-ethers. Will raise ValueError if any
		# of these fields already exist in the db.

		self.clusterdb.insert(name, mid, rack, rank, ip=ip, 
			netmask=self.privateNetmask)
		syslog.syslog("kickstart.cgi: inserted node %s %s %s" 
			% (membership, name, ip))
		return self.clusterdb.getNodeId()


	def localKickstart(self):

		membership=None
		id = None
		if self.membership:
			membership = self.membership
		else:
			# Iterate over all the hostnames (aliases, IP addrs)
			# of the node to find the host in the database.
			for name in self.clientList:
				id = self.getNodeId(name)
				if id:
					break
			if not id:
				id = self.insertNode()
			self.clientName = self.getNodeName(id)

		# Update the number of CPUs for this node.  Do nothing
		# is we are just a "--membership"

		if id and self.cpus != None:
			update = 'update nodes set CPUs=%s where id=%d' \
				 % (self.cpus, id)
			self.execute(update)

		# If we have a client IP address lookup the
		# information needed to build its kickstart file.
		# Otherwise we look up the information to build a
		# generic membership kickstart file.
		
		if not membership:
			query = ('select '
				 'appliances.Graph,'
				 'appliances.Node,'
				 'distributions.Name '
				 'from nodes,memberships,appliances,'
				 'distributions '
				 'where nodes.ID=%d and '
				 'memberships.ID=nodes.Membership and '
				 'memberships.Appliance=appliances.ID and '
				 'memberships.Distribution=distributions.ID' %
				 id)
		else:
			query = ('select '
				 'appliances.Graph,'
				 'appliances.Node,'
				 'distributions.Name '
				 'from memberships,appliances,distributions '
				 'where memberships.Name="%s" and '
				 'memberships.Appliance=appliances.ID and '
				 'memberships.Distribution=distributions.ID' %
				 membership)
			
		self.execute(query)
		try:
			graph, node, dist = self.fetchone()
		except TypeError:
			self.report.append('<h1>Bad Data from Database</h1>')
			print self
			return
		self.close()
		

		# The values we just pulled from the database are the
		# default values.  The FORM data can override any of
		# these values.

		if self.form.has_key('graph'):
			graph = self.form['graph'].value
		if self.form.has_key('node'):
			node = self.form['node'].value
		if self.form.has_key('arch'):
			self.arch = self.form['arch'].value
		if self.form.has_key('dist'):
			dist = self.form['dist'].value
		if self.form.has_key('os'):
			OS = self.form['os'].value
		else:
			OS = 'linux' # should aways come from loader

		rcl = '/opt/rocks/bin/rocks set host attr %s' % self.clientName
		os.system('%s arch %s'	% (rcl, self.arch))
		os.system('%s os %s'	% (rcl, OS))
			
		dist = os.path.join(dist, 'lan')

		# Command line args has the highest precedence.
		if self.distname:
			dist = self.distname

		self.dist.setDist(dist)
		self.dist.setArch(self.arch)
		distroot = self.dist.getReleasePath()
		buildroot = os.path.join(distroot, 'build')
		# We want path without '/home/install'
		self.dist.setRoot('')

		# Export the form data to the environment to make it
		# available to the first stage KPP pass over the XML
		# files.

		for var in self.form.keys():
			os.environ[var] = self.form[var].value

		for line in os.popen("""
			/opt/rocks/bin/rocks list host xml arch=%s os=linux %s
			""" %  (self.arch, self.clientName)).readlines():
			
			self.report.append(line[:-1])


	def wanKickstart(self):
		"""Sends a minimal kickstart file for wide-area installs."""
		# Default distribution name.
		if self.form.has_key('arch'):
			self.arch = self.form['arch'].value
		if self.form.has_key('os'):
			OS = self.form['os'].value
		else:
			OS = 'linux' # should aways come from loader

		#
		# get the minimal attributes
		#
		attrs = {}

		for i in [ 'Kickstart_Lang', 'Kickstart_Keyboard',
				'Kickstart_PublicHostname',
				'Kickstart_PrivateKickstartBasedir' ]:

			cmd = '/opt/rocks/bin/rocks list attr | '
			cmd += "grep %s: | awk '{print $2}'" % i
			for line in os.popen(cmd).readlines():
				var = line[:-1]
			attrs[i] = var.strip()

		attrs['hostname'] = self.clientList[0]
		attrs['arch'] = self.arch
		attrs['os'] = OS

		cmd = '/opt/rocks/bin/rocks list node xml wan '
		cmd += 'attrs="%s"' % (attrs)
		for line in os.popen(cmd).readlines():
			self.report.append(line[:-1])


	def proxyKickstart(self):
		try:
			fin = open('nodes.xml', 'r')
		except IOError:
			raise KickstartError, 'cannot kickstart external hosts'
			
		parser  = make_parser()
		handler = NodesHandler()
		parser.setContentHandler(handler)
		parser.parse(fin)
		fin.close()

		try:
			server, client, path = \
			handler.getServer(self.clientName)
		except TypeError:
			raise KickstartError, \
				"unknown host (not found in nodes.xml)", \
				self.clientName

		if not path:
			path = 'install'
		url = 'http://%s/%s/kickstart.cgi?client=%s' % (server,
								path,
								client)

		cmd = 'wget -qO- %s' % url
		for line in os.popen(cmd).readlines():
			self.report.append(line[:-1])

		return


	def initCount(self):
		try:
			#	
			# get the number of processors
			#	
			cmd = "grep 'processor' /proc/cpuinfo | wc -l"
			numprocessors = os.popen(cmd).readline()

			#
			# multiply it by two
			#
			count = int(numprocessors) * 2
		except:
			count = 2
			pass

		return count


	def openLockFile(self):
		try: 
			fp = open(self.lockFile, 'r+')
		except:
			fp = None
			pass

		if fp == None:
			#
			# if lockfile doesn't exist, then try to recreate it
			#
			try:
				fp = open(self.lockFile, 'w+')
			except:
				fp = None
				pass

		return fp


	def checkLoad(self):
		fp = self.openLockFile()

		#
		# if lockfile doesn't exist or is unreadable return
		#
		if fp == None:
			return 0

		fcntl.lockf(fp, fcntl.LOCK_EX)
		fp.seek(0)
		input = fp.readline()
		if input == '':
			siblings = self.initCount()
		else:
			siblings = int(input)

		if siblings > 0:
			siblings = siblings - 1
			fp.seek(0)
			fp.write("%d\n" % siblings)
			fp.flush()
			fcntl.lockf(fp, fcntl.LOCK_UN)
			fp.close()
		else:
			fcntl.lockf(fp, fcntl.LOCK_UN)
			fp.close()
			raise KickstartError, \
				"%d kickstart.cgi processes: %s" % \
					(siblings, self.clientName)


	def completedLoad(self):
		#
		# we're done with kickstart file generation.
		#
		# update the lock file to reflect the fact that one more
		# unit of kickstart file generation can now occur
		#

		fp = self.openLockFile()

		#
		# if lockfile doesn't exist or is unreadable return
		#
		if fp == None:
			return 0
		
		fcntl.lockf(fp, fcntl.LOCK_EX)

		input = fp.readline()
		siblings = int(input)
		siblings = siblings + 1

		fp.seek(0)
		fp.write("%d\n" % siblings)
		fp.flush()

		fcntl.lockf(fp, fcntl.LOCK_UN)
		fp.close()

		return 1


	def insertAccess(self, urlroot, host, ip=''):
		"""Gives access to this WAN client using .htaccess files.
		This is a side effect, and is out of band from kickstart
		generation."""

		firstdir = self.dist.getArch()
		os.chdir(urlroot)
		try:
			os.mkdir(host)
		except:
			# This is to prevent collisions between multiple
			# kcgi processes.
			if os.path.exists(os.path.join(host,'rolls')) and \
				os.path.exists(os.path.join(host,firstdir)):
					return
		os.chdir(host)
		try:
			os.symlink('../%s' % firstdir, firstdir)
			os.symlink('../rolls', 'rolls')

			access=open('.htaccess','w')

			acl = host
			if ip:
				acl += " %s" % ip
			access.write('Allow from %s\n' % (acl))
			access.write('Deny from all\n')
			access.close()

		except:
			pass
		self.report.append('# Opened WAN access to %s\n' % host)


	def isInternal(self):
		"""Returns true if the client request is inside our private
		network."""

		network = self.getGlobalVar('Kickstart','PrivateNetwork')
		netmask = self.getGlobalVar('Kickstart','PrivateNetmask')
		self.privateNetmask = netmask

		# Test based on our client's IP address.
		work = string.split(network, '.')
		mask = string.split(netmask, '.')
		ip = string.split(self.clientList[-1], '.')

		for i in range(0, len(ip)):
			a = int(ip[i]) & int(mask[i])
			b = int(work[i]) & int(mask[i])

			if a != b:
				return 0

		return 1
	

	def run(self):

		try:
			self.checkLoad()
		except KickstartError:
			print "Content-type: text/html"
			print "Status: 503 Service Busy"
			print "Retry-After: 15"
			print
			print "<h1>Service is Busy</h1>"
			sys.exit(1)

		try:
			self.connect()

			# If request comes from internal network, it is
			# internal. Otherwise, this is a WAN request.

			if not self.clientList[0] or self.isInternal():
				self.localKickstart()
			else:
				self.wanKickstart()
		except:
			pass
			
		#
		# build the output string
		#
		self.completedLoad()
		out = string.join(self.report, '\n')
		
		print 'Content-type: application/octet-stream'
		print 'Content-length: %d' % (len(out))
		print ''
		print out


	
class NodesHandler(rocks.util.ParseXML):

	def __init__(self):
		rocks.util.ParseXML.__init__(self)
		self.nodes		= {}
		self.attrs		= rocks.util.Struct()
		self.attrs.default	= rocks.util.Struct()


	def getServer(self, client):
		try:
			val = self.nodes[client]
		except KeyError:
			val = None
		return val


	def addClient(self):
		if self.attrs.spoof:
			val = (self.attrs.server, self.attrs.spoof,
			       self.attrs.path)
		else:
			val = (self.attrs.server, self.attrs.client,
			       self.attrs.path)
		key = self.attrs.client
		self.nodes[key] = val


	def endElement_proxy(self, name):
		if not self.attrs.server:
			self.attrs.server = self.attrs.default.server
		if not self.attrs.client:
			self.attrs.client = self.attrs.default.client
		if not self.attrs.path:
			self.attrs.path = self.attrs.default.path
		if not self.attrs.spoof:
			self.attrs.spoof = self.attrs.default.spoof

		if self.attrs.client:
			self.addClient()


	def startElement_client(self, name, attrs):
		self.text		= ''
		self.attrs.server	= self.attrs.default.server
		self.attrs.path		= self.attrs.default.path
		self.attrs.spoof	= self.attrs.default.spoof
		
		if attrs.has_key('server'):
			self.attrs.server = attrs['server']
		if attrs.has_key('path'):
			self.attrs.path = attrs['path']
		if attrs.has_key('spoof'):
			self.attrs.spoof = attrs['spoof']


	def endElement_client(self, name):
		self.attrs.client = self.text
		self.addClient()
		self.attrs.client = None



app = App(sys.argv)
app.parseArgs('kcgi')
try:
	app.run()
except KickstartError, msg:
	sys.stderr.write("kcgi error - %s\n" % msg)
	sys.exit(-1)


