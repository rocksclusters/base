#! @PYTHON@
#
# $RCSfile: insert-ethers.py,v $
#
# Insert-ethers evolution
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
# $Log: insert-ethers.py,v $
# Revision 1.55  2012/11/27 00:48:49  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.54  2012/10/02 18:01:00  clem
# insert-ether now checks that the user supplied a valid IP
#
# Reported by Suresh Singh
# http://marc.info/?l=npaci-rocks-discussion&m=134593126713897&w=2
#
# Revision 1.53  2012/05/06 05:48:49  phil
# Copyright Storm for Mamba
#
# Revision 1.52  2012/01/30 06:15:07  phil
# should work on both 5 (python 2.4) and 6 (python 2.6)
#
# Revision 1.50  2010/09/07 23:53:09  bruno
# star power for gb
#
# Revision 1.49  2010/07/14 22:41:14  anoop
# Add the "kickstartable" attribute to appliances. Use this attribute
# to determine if insert-ethers needs to wait for a node to kickstart
# after getting an IP address
#
# Revision 1.48  2009/07/03 00:39:26  bruno
# fix replace code
#
# Revision 1.47  2009/05/21 21:16:26  bruno
# nuke nutty flags
#
# Revision 1.46  2009/05/01 19:07:09  mjk
# chimi con queso
#
# Revision 1.45  2009/03/23 23:03:57  bruno
# can build frontends and computes
#
# Revision 1.44  2009/03/06 22:45:41  bruno
# nuke 'dbreport access' and 'dbreport machines'
#
# Revision 1.43  2008/11/21 19:10:10  bruno
# restart syslog if we see 'last message repeated' messages from the frontend
#
# Revision 1.42  2008/10/30 21:44:58  bruno
# fix -- thanks to thomas hamel for the bug report
#
# Revision 1.41  2008/10/18 00:56:03  mjk
# copyright 5.1
#
# Revision 1.40  2008/09/09 23:10:45  bruno
# added some solaris/sunos changes for anoop
#
# Revision 1.39  2008/08/28 18:11:21  anoop
# Remove duplicate database connect lines. This is, most likely,
# the cause of the problem where plugins couldn't access the database
#
# Revision 1.38  2008/08/27 02:41:08  anoop
# Very minor changes to the database schema to store os type along
# with appliance. This is mainly to include solaris support for
# a compute appliance
#
# Revision 1.37  2008/07/24 22:39:12  anoop
# Don't forget the comma, don't forget the comma, don't forget the comma
#
# Revision 1.36  2008/07/23 00:29:55  anoop
# Modified the database to support per-node OS field. This will help
# determine the kind of provisioning for each node
#
# Modification to insert-ethers, rocks command line, and pylib to
# support the same.
#
# Revision 1.35  2008/05/22 21:02:07  bruno
# rocks-dist is dead!
#
# moved default location of distro from /export/home/install to
# /export/rocks/install
#
# Revision 1.34  2008/04/15 22:14:45  bruno
# call rocks command line to remove a host
#
# Revision 1.33  2008/03/17 23:49:32  bruno
# remapped F10/F11 to F8/F9
#
# Revision 1.32  2008/03/06 23:41:45  mjk
# copyright storm on
#
# Revision 1.31  2007/08/28 15:49:27  anoop
# Stupid bug fixed. Next time, I need to remember to put code below a comment,
# and not just leave it at the comment.
#
# Revision 1.30  2007/06/25 23:24:36  bruno
# added a command to remove the PXE boot configuration for a node that
# is removed with insert-ethers
#
# Revision 1.29  2007/06/23 04:03:25  mjk
# mars hill copyright
#
# Revision 1.28  2007/06/09 00:27:09  anoop
# Again, moving away from using device names, to using subnets.
#
# Revision 1.27  2007/06/05 16:37:05  anoop
# Heavy modifications to insert-ethers, to accomadate the new database schema.
# Now, just a little less buggy than before. Sorry for the delay
#
# Revision 1.26  2007/05/30 23:00:55  anoop
# Pre-alpha version of the new insert ethers, tested to some extent
# Still a huge number of bugs. Please bear with me
#
# Revision 1.25  2006/09/11 22:47:28  mjk
# monkey face copyright
#
# Revision 1.24  2006/08/10 00:09:45  mjk
# 4.2 copyright
#
# Revision 1.23  2006/07/06 19:50:11  bruno
# for 'dump' command, print name of utility from argv -- that way, we can
# specify the full pathname when these tools are used during an installation
# and the path has not yet been initialized.
#
# Revision 1.22  2006/06/05 23:00:17  bruno
# order the appliance types alphabetically
#
# Revision 1.21  2006/01/26 01:18:45  bruno
# syntax fixups
#
# Revision 1.20  2006/01/23 21:36:57  yuchan
# update for supporting mult-byte -yuchan
#
# Revision 1.19  2006/01/16 06:49:01  mjk
# fix python path for source built foundation python
#
# Revision 1.18  2005/10/12 18:08:46  mjk
# final copyright for 4.1
#
# Revision 1.17  2005/09/16 01:02:25  mjk
# updated copyright
#
# Revision 1.16  2005/09/15 22:08:40  bruno
# don't run insert-ethers until rocks-dist completes
#
# Revision 1.15  2005/09/02 00:05:50  bruno
# pushing toward 4.1 beta
#
# Revision 1.14  2005/07/11 23:51:37  mjk
# use rocks version of python
#
# Revision 1.13  2005/06/10 13:40:33  mjk
# connect to DB for update also
#
# Revision 1.12  2005/05/27 22:09:01  bruno
# the 'added' and 'removed' plugin functions now also get the nodeid
#
# Revision 1.11  2005/05/24 21:22:00  mjk
# update copyright, release is not any closer
#
# Revision 1.10  2005/05/23 23:59:24  fds
# Frontend Restore
#
# Revision 1.9  2005/05/07 02:23:24  fds
# Fixed bug with --staticip pointed out by Qiang Xu.
#
# Revision 1.8  2005/03/31 02:45:40  fds
# removed debug statements
#
# Revision 1.7  2005/03/31 02:30:56  fds
# sacerdoti in for phil.
#
# Revision 1.6  2005/03/30 21:13:07  fds
# Put back old discover() logic.
#
# Revision 1.5  2005/03/26 01:09:37  fds
# Using rc file inheritance to read global securityrc file. Requires multiple
# inheritance in the XML parser class: no other way, we are in OO purgatory,
# some would say one of the early rings of hell. Happy good friday.
#
# Revision 1.4  2005/03/14 22:19:31  fds
# Tweaks to exception handling.
#
# Revision 1.3  2005/03/14 20:25:18  fds
# Plugin architecture: service control is modular. Rolls can add hooks without
# touching insert-ethers itself. Plugins can be ordered relative to each other by
# filename.
#
# Revision 1.2  2005/03/10 00:18:00  fds
# Fix --help hijack: move rocks-distrc parsing later.
#
# Revision 1.1  2005/03/01 02:03:17  mjk
# moved from core to base
#
# Revision 1.118  2005/02/23 01:41:37  fds
# Be hardcore but not hardcoded.
#
# Revision 1.117  2005/02/16 20:22:16  phil
# check for duplicateIP correctly when static ip is specified
#
# Revision 1.116  2005/02/08 22:47:11  phil
# Won't let you insert a duplicate, non-empty mac address, but messaging is
# getting lost.
# Still need to have a clean way to turn off interactive when not wanted.
#
# Revision 1.115  2005/02/08 19:49:54  phil
# More boundary condition checking. Will not insert an (Appliance,Rack,Rank)
# duplicate, even if the specified hostnames are different.
# Setting basename now works properly
#
# Revision 1.114  2005/02/08 05:58:38  phil
# Setting ip address from command line works (but should check if
# the IPaddress already exists)
#
# Revision 1.113  2005/02/08 05:49:19  phil
#
# Now sports a --dump command and a long host of command-line options.
# needs testing (lots of testing) -- need to talk to bruno to understand
# how the plug-and-play ethernet logic is handled
#
# Revision 1.112  2005/01/17 17:18:26  bruno
# insert-ethers now correctly waits for all nodes that have been discovered
# but not yet received their kickstart file.
#
# the real, real fix for bug 15.
#
# Revision 1.111  2005/01/12 21:40:51  bruno
# the real fix for bug 12.
#
# insert-ethers now checks if the hostname for a newly discovered node is
# already in the database. this happens on every discovery.
#
# Revision 1.110  2004/11/23 01:29:16  bruno
# mason type pretty one day
#
# Revision 1.109  2004/11/02 01:39:54  fds
# Converge faster by increasing load on frontend papache server (suggesion by phil).
#
# Revision 1.108  2004/10/21 21:24:30  mjk
# --baseip flag was broken
#
# Revision 1.107  2004/10/21 00:51:33  fds
# Restart ganglia if we add nodes
#
# Revision 1.106  2004/10/15 00:27:38  fds
# --update must respect lock file.
#
# Revision 1.105  2004/10/13 18:34:09  fds
# Dont wait for a kickstart file if you're not going
# to ask for one. Fixes bug 55
#
# Revision 1.104  2004/10/06 18:30:49  fds
# Support for security levels. Minimal changes to insert-ethers.
#
# Revision 1.103  2004/09/14 00:48:28  fds
# Put tick in even if node came in with a cert.
#
# Revision 1.102  2004/09/12 07:08:40  fds
# Dont need this.
#
# Revision 1.101  2004/09/11 05:02:28  fds
# Remove immediately exits; fix for bug 39
#
# Revision 1.100  2004/09/07 22:35:13  fds
# Evolution. Tracks kickstart file accesses. New --max-new and --public-mode
# flags. New exception structure for error handling.
#
# Revision 1.99  2004/08/24 21:58:49  mjk
# bad mason
#
# Revision 1.98  2004/08/23 19:24:30  mjk
# might even work
#
# Revision 1.97  2004/08/17 02:00:35  bruno
# add a check to make sure we don't add a name to the database if that name
# is already in the database.
#
# this addressess bug 15.
#
# Revision 1.96  2004/07/27 18:33:15  fds
# Uses rocks.security to open/close IP-based access
# to local nodes.
#
# Revision 1.95  2004/04/19 20:45:06  fds
# Update hosts file (used to be in NIS, now in DNS).
#
# Revision 1.94  2004/04/16 22:46:52  thadpongp
# make insert-ethers update sce.conf file everytime it's finished
#
# Revision 1.93  2004/04/16 17:29:03  bruno
# make sure to rebuild and restart dns on an '--update'
#
# Revision 1.92  2004/04/13 19:14:18  mjk
# fat fingered the s
#
# Revision 1.91  2004/04/05 18:00:08  mjk
# - Drop NIS hook in insert-ethers (we do not support it anymore)
# - Add SCE Roll hook for Thadpong to write sce conf file when insert-ethers
#   exits.
#
# Revision 1.90  2004/03/25 03:15:52  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.89  2004/03/19 03:18:05  bruno
# needed to remove lock file after the distribution is rebuilt
#
# Revision 1.88  2004/02/06 00:43:55  fds
# Schema migration.
#
# Revision 1.87  2004/02/04 17:39:39  bruno
# on what interface do you want to install?
#
# Revision 1.86  2004/01/28 20:36:59  mjk
# replace getNaodeName() to change naming scheme
#
# Revision 1.85  2003/12/17 18:59:17  mjk
# one of these days I'll have to learn python
#
# Revision 1.84  2003/12/17 18:51:40  mjk
# added lock file
#
# Revision 1.83  2003/12/16 16:29:55  bruno
# bug fix
#
# Revision 1.82  2003/12/15 20:11:44  mjk
# - Created SGE_ARCH to find sge binaries
# - Removed more hard paths
#
# Revision 1.81  2003/12/15 17:28:42  mjk
# use ROCKS_ROOT and SGE_ROOT env vars instead of paths
#
# Revision 1.80  2003/09/24 00:38:28  bruno
# changes for redhat 9
#
# Revision 1.79  2003/08/27 18:11:19  bruno
# from c to mysql
#
# Revision 1.78  2003/08/26 22:44:20  mjk
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
# Revision 1.77  2003/08/15 22:34:47  mjk
# 3.0.0 copyright
#
# Revision 1.76  2003/08/15 21:07:26  mjk
# - RC files only built one per directory (fixed)
# - Default CGI arch is native (used to be i386)
# - Added scheduler,nameservices to rocksrc.xml
# - insert-ethers know what scheduler and nameservice we use
# - I forget what else
#
# Revision 1.75  2003/07/17 22:35:41  bruno
# tweaks
#
# Revision 1.74  2003/07/01 23:32:37  bruno
# added 'remove' flag
#
# Revision 1.72  2003/04/01 23:15:54  fds
# Added support for the DNS server.
#
# Revision 1.71  2003/03/14 04:58:50  bruno
# added a patch for replace that concerns sge
#
# Revision 1.70  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.69  2003/02/11 17:23:43  bruno
# changed os.system() for commands.getstatusoutput() when restarting SGE.
# for some reason, os.system() insisted on displaying standard error messages
# to the screen -- even when redirecting to /dev/null
#
# Revision 1.68  2003/01/09 21:27:53  bruno
# cleaned up bug i put into najib's fix
#
# Revision 1.67  2003/01/07 18:02:03  bruno
# integrated patches from najib for sge
#
# Revision 1.66  2002/12/03 21:03:54  bruno
# fixed syntax error
#
# Revision 1.65  2002/11/27 04:57:53  bruno
# fix: update database, rebuild files, restart services, then pop window
#
# Revision 1.64  2002/11/09 21:31:26  bruno
# needed restart of sge in 'all' section
#
# Revision 1.63  2002/10/18 21:33:26  mjk
# Rocks 2.3 Copyright
#
# Revision 1.62  2002/10/15 23:47:24  bruno
# fixed syntax error
#
# Revision 1.61  2002/10/15 16:10:16  bruno
# added sge (re)configuration code
#
# Revision 1.60  2002/10/15 15:03:30  bruno
# fixed syntax error
#
# Revision 1.59  2002/10/14 19:17:53  bruno
# need to restart maui after pbs is restarted
#
# Revision 1.58  2002/10/10 20:48:06  bruno
# changed make* to dbreport *
#
# Revision 1.57  2002/10/03 16:12:30  bruno
# find *all* machines.*LINUX files
#
# Revision 1.56  2002/09/28 14:49:58  bruno
# added static ip address generation
#
# Revision 1.55  2002/07/30 20:03:24  bruno
# added makemachines to rebuild ethernet-based machines.LINUX file(s)
#
# Revision 1.54  2002/07/19 23:21:07  bruno
# took out pbs restart in the future -- smelled too much like a 'sleep 1'
# fix to a problem
#
# Revision 1.53  2002/07/19 23:12:00  bruno
# added code to restart PBS 20 minutes in the future to catch the case where
# ganglia is not up on a compute node when it is first installed
#
# Revision 1.52  2002/07/13 00:26:23  bruno
# fixed a bug in the restart loop
#
# Revision 1.51  2002/05/21 00:11:43  bruno
# added 'pbs_server' restart for OpenPBS
#
# Revision 1.50  2002/04/22 23:13:40  mjk
# added --nopbs flag back
#
# Revision 1.49  2002/03/15 20:03:18  bruno
# reversed the list of inserted appliances so the most recent inserted
# appliance is at the top of the list.
#
# Revision 1.48  2002/02/21 21:33:27  bruno
# added new copyright
#
# Revision 1.47  2002/02/15 21:43:17  mjk
# use system() for rocks-dist
#
# Revision 1.46  2002/02/14 23:11:45  mjk
# - Changed -x to -e test in install.xml for cdrom device
# - Fixed insert-ethers bad gui
# - Fixed copycd command
#
# Revision 1.45  2002/02/14 02:12:29  mjk
# - Removed CD copy gui code from insert-ethers
# - Added CD copy code back to install.xml (using rocks-dist)
# - Added copycd command to rocks-dist
# - Added '-' packages logic to kgen
# - Other file changed to support above
#
# Revision 1.44  2002/02/12 05:45:46  mjk
# more CD copy changes
#
# Revision 1.43  2002/02/08 19:20:08  mjk
# Fixed ServiceController service list to have singletons instead of
# atoms for single service restarts.  I.e.  use ('foo', ) instead of
# ('foo').
#
# Revision 1.42  2002/02/05 22:37:12  mjk
# - copy files from CDROM or Mirror
# - needs testing
#
# Revision 1.41  2002/01/16 23:52:01  mjk
# Shuffled code around to make room for other tasks
#
# Revision 1.40  2001/11/30 20:05:14  mjk
# - --rank no longer exits after one insert
# - add --update to rebuild dhcp/host/pbs
#
# Revision 1.39  2001/10/31 18:18:56  bruno
# more cleanup
#
# Revision 1.38  2001/10/31 18:13:36  bruno
# removed debug
#
# Revision 1.37  2001/10/30 22:26:08  bruno
# next rev
#
# Revision 1.36  2001/10/30 17:21:34  bruno
# first wack at getting insert-ethers right
#
# Revision 1.35  2001/10/30 15:04:50  bruno
# starting to put gui crap in
#
# Revision 1.34  2001/10/27 00:44:49  bruno
# basic insert ethers is working
#
# Revision 1.33  2001/10/25 22:25:43  mjk
# check point
#
# Revision 1.32  2001/10/24 20:23:32  mjk
# Big ass commit
#


import sys
import os
import string
import time
import signal
import snack
import rocks.sql
import rocks.ip
import rocks.util
import rocks.app
import rocks.kickstart
import rocks.clusterdb
from syslog import syslog

try:
	from rhpl.translate import _, N_
	import rhpl.translate as translate
	translate.textdomain ('insert-ethers')
except:
	from gettext import gettext as _


class InsertError(Exception):
	pass

class InsertDone(Exception):
	pass

class DumpError(Exception):
	pass


class ServiceController:

	def __init__(self):
		self.services = {}
		self.ignoreList         = []
		self.plugins		= []
		self.plugindir		= os.path.abspath(
			'/opt/rocks/var/plugins/')


	def isIgnored(self, service):
		return service in self.ignoreList
	
	def ignore(self, service):
		if service not in self.ignoreList:
			self.ignoreList.append(service)


	def restart(self, service):
		for name in self.services[service]:
			if service not in self.ignoreList:
				eval('self.restart_%s()' % name)


	def loadPlugins(self, app):
		
		if not os.path.exists(self.plugindir):
			return

		if self.plugindir not in sys.path:
			sys.path.append(self.plugindir)
			
		info = _("insert-ethers loading plugins: ")

		modlist = os.listdir(self.plugindir + '/insertethers')
		modlist.sort()
		for f in modlist:
			
			modname, ext = os.path.splitext(f)
			if modname == '__init__' or ext != '.py':
				continue

			info += "%s " % modname
			mods = __import__('insertethers.%s' % modname)
			m = getattr(mods, modname)
			try:
				plugin_class = getattr(m, 'Plugin')
				if not issubclass(plugin_class, 
						rocks.sql.InsertEthersPlugin):
					raise Exception, 'Invalid class'
				
				# Instantiate plugin
				p = plugin_class(app)
				self.plugins.append(p)
			except:
				info += _("(invalid, skipping) ")
		syslog(info)
		
		
	def logError(self, o=''):
		"Logs the last exception to syslog"
		
		oops = "%s threw exception '%s %s'" % \
			(o, sys.exc_type, sys.exc_value)
		syslog(oops)
		
				
	def added(self, nodename, nodeid):
		"Tell all plugins this node has been added."

		for p in self.plugins:
			try:
				p.added(nodename, nodeid)
			except:
				self.logError(p)	
	
	
	def removed(self, nodename, nodeid):
		"Tell all plugins this node has been removed."

		for p in self.plugins:
			try:
				p.removed(nodename, nodeid)
			except:
				self.logError(p)
					
	
	def done(self):
		"Tell plugins we are finished"
		
		for p in self.plugins:
			try:
				p.done()
			except:
				self.logError(p)

	def update(self):
		"Tell plugins to reload"
		
		for p in self.plugins:
			try:
				p.update()
			except:
				self.logError(p)
			

class GUI:

	def __init__(self):
		self.screen = None
	
	def startGUI(self):
		self.screen = snack.SnackScreen()

	def endGUI(self):
		self.screen.finish()

	def errorGUI(self, message, l1=_("Quit"), l2=None):
		return self.modalGUI(str(message), _("Error"), l1, l2)

	def warningGUI(self, message, l1=_("OK"), l2=None):
		return self.modalGUI(str(message), _("Warning"), l1, l2)

	def infoGUI(self, message, l1=_("OK"), l2=None):
		return self.modalGUI(str(message), _("Information"), l1, l2)
		
	def modalGUI(self, message, title, l1, l2):
		form = snack.GridForm(self.screen, title, 2, 2)

		textbox = snack.TextboxReflowed(40, message)
		form.add(textbox, 0, 0)
		if not l2:
			b1 = snack.Button(l1)
			form.add(b1, 0, 1)
		else:
			b1 = snack.Button(l1)
			b2 = snack.Button(l2)
			form.add(b1, 0, 1)
			form.add(b2, 1, 1)

		if form.runOnce() == b1:
			return 0
		else:
			return 1

	
class InsertEthers(GUI):

	def __init__(self, app):
		GUI.__init__(self)
		self.sql		= app
		self.controller		= ServiceController()
		self.clusterdb		= rocks.clusterdb.Nodes(app)
		self.cabinet		= 0
		self.rank		= -1
		self.replace		= ''
		self.only_add_one	= 0
		self.maxNew		= -1 
		self.remove		= 0
		self.membership		= None
		self.basename		= None
		self.distid		= None
		self.restart_services	= 0
		self.inserted		= []
		self.kickstarted	= {}
		self.staticip		= 'false'
		self.lastmsg		= ''
		self.client		= ''
		self.rocksdist_lockFile	= '/var/lock/rocks-dist'
		self.osname		= 'linux'


		## Things for Dumping/Restoring 
		self.doRestart		= 1
		self.mac		= None
		self.dump		= 'false'
		self.ipaddr		= None
		self.netmask		= None
		self.subnet		= 'private' # Internal Network
		self.broadcast		= None
		self.appliance_name	= None
		self.device		= None
		self.module		= None
		self.hostname		= None
		self.ncpus		= 1
		self.logfile		= None

		self.kickstartable	= True

	def log(self, line):
		if not self.logfile:
			self.logfile = open('/tmp/insert-ethers.debug','w')
		self.logfile.write(line + '\n')
		self.logfile.flush()

	def setBasename(self,name):
		self.basename = name 

	def setHostname(self,name):
		self.hostname = name 

	def setMac(self, macaddr):
		self.mac = macaddr

	def setDevice(self, device):
		self.device = device

	def setModule(self, module):
		self.module = module 

	def setIPaddr(self, ipaddr):
		#if this works is a valid IP address
		#if not it throws an exception
		rocks.ip.IPAddr(ipaddr)
		self.ipaddr = ipaddr 

	def setNetmask(self, netmask):
		self.netmask = netmask 

	def setBroadcast(self, bcast):
		self.broadcast = bcast 

	def setCpus(self, ncpus):
		self.ncpus = ncpus 

	def setApplianceName(self,appliance_name):
		self.appliance_name = appliance_name 

	def setDump(self):
		self.Dump = 'true' 

	def setCabinet(self, n):
		self.cabinet = n

	def setRank(self, n):
		self.rank = n

	def setReplace(self, host):
		self.replace = host
		self.only_add_one = 1

	def setRemove(self, host):
		self.replace = host
		self.remove = 1

	def setStatic(self):
		self.staticip = 'true'

	def setMax(self, max):
		self.maxNew = max

	def setOSName(self, osname):
		self.osname = osname

	def startGUI(self):

		GUI.startGUI(self)

		self.form = snack.GridForm(self.screen,
					   _("Inserted Appliances"), 1, 1)
		self.textbox = snack.Textbox(50, 4, "", scroll = 1)
		self.form.add(self.textbox, 0, 0)

		self.screen.drawRootText(0, 0, _("%s -- version %s") % 
					 (self.sql.usage_name,
					  self.sql.usage_version))
		self.screen.drawRootText(0, 1, 
				_("Opened kickstart access to %s network") % 
				self.sql.getPrivateNet())
		self.screen.pushHelpLine(' ')


	def checkAppliance(self, app):

		query='select name from memberships where name="%s" ' % (app)
		if self.sql.execute(query) == 0:
			msg = _("Invalid Appliance \"%s\"") % \
				(self.appliance_name)
			raise InsertError, msg


	def membershipGUI(self):
		#
		# if self.appliance_name is not empty don't ask
		# 
		if self.appliance_name is not None: 
			app_string = []
			app_string.append(self.appliance_name)
			index = 0

		else:
			#
			# display all memberships to the user -- let them choose
			# which type of machine they want to integrate
			#
			query = 'select memberships.name from memberships, appliances '\
				'where memberships.appliance=appliances.id and '\
				'find_in_set("%s",appliances.OS) and ' \
				'memberships.public = "yes" ' \
				'order by memberships.name' \
				 % (self.osname) 

			if self.sql.execute(query) == 0:
				self.errorGUI(_("No appliance names in database"))
				raise InsertError, msg

			app_string = []
			for row in self.sql.fetchall():
				(name, ) = row
				app_string.append(name)

			(button, index) = \
			snack.ListboxChoiceWindow(self.screen,
			_("Choose Appliance Type"), 
			_("Select An Appliance Type:"),
			app_string, buttons = (_("OK"), ), default = 0)

		#
		# Now try do sanity checking that appliance is OK
		#
		query = 'select memberships.id, appliances.name, ' \
			'memberships.distribution from ' \
			'memberships,appliances where ' \
			'memberships.name = "%s" and ' \
			'memberships.appliance = appliances.id' % \
			(app_string[index]) 

		if self.sql.execute(query) == 0:
			msg = _("Could not find appliance (%s) in database") \
				% (app_string[index])
			raise InsertError, msg

		self.membership, basename, self.distid = \
			self.sql.fetchone()
		
		# Check if the appliance is kickstartable. We only need
		# to check the appliance_attributes table in this instance
		# since this value cannot be in any other table yet.
		query = 'select if(aa.value="yes", True, False) from '	+\
			'appliance_attributes aa, appliances a where '	+\
			'a.name="%s" and aa.appliance=a.id ' % basename+\
			'and aa.attr="kickstartable"'
		rows = self.sql.execute(query)
		if rows > 0:
			self.kickstartable = bool(self.sql.fetchone()[0])

		#
		# if the basename was not overridden on the command line
		# use what we just read from the database
		#
		if self.basename is None:
			self.basename = basename
			
		self.setApplianceName(app_string[index])
			

	def batchCommand(self):
		"""Check cmdline args and insert into the database with
		minimal user interaction. Get the missing pieces you need from 
		the gui if necessary."""

		if not self.appliance_name:
			self.startGUI()
			self.membershipGUI()
			self.endGUI()

		# Once more to initialize the membership id and such.
		self.membershipGUI()

		self.initializeRank()
		self.ipaddr = self.getnextIP(self.subnet)

		#
		# mac == "None" is a special case (eg. frontends are like this)
		#        here "None" is the literal string. 
		#
		if self.mac == "None":
			self.mac = None
		
		# Will emit a ValueError if node already exists, 
		# catch later.
		nodename = self.getNodename()

		self.clusterdb.insert(nodename, self.membership, 
			self.cabinet, self.rank, self.mac, self.ipaddr, 
			self.netmask, self.subnet, self.osname)

		# Execute any plugins when adding hosts via
		# command-line parameters
		self.controller.added(nodename, self.clusterdb.getNodeId())

		self.sql.link.commit()

		print "Inserted node %s" % nodename
		return


	def dumpCommands(self):

		query = 'select nodes.name, nodes.rack, nodes.rank, '\
			'nodes.cpus, memberships.name, '\
			'networks.mac, networks.device, networks.module, '\
			'networks.IP, networks.netmask ' \
			'from nodes,memberships,networks,subnets where '\
			'nodes.membership = memberships.ID and '\
			'nodes.id = networks.node and and ' \
			'subnets.name="%s" and networks.subnet=subnets.id ' \
			'order by memberships.name,nodes.rack,nodes.rank' \
				% (self.subnet)

		if self.sql.execute(query) == 0:
			msg = _("Could not find any nodes in database")
			raise dumpError, msg
		for row in self.sql.fetchall():
			(name,rack,rank,cpus,membership,mac,device,\
				module,ipaddr,netmask) = row
			print '%s --hostname="%s" --rack=%d '\
			'--rank=%d --cpus=%d --appliance="%s" --mac="%s" '\
			'--device="%s" --module="%s" --ipaddr="%s" '\
			'--netmask="%s" --norestart --batch' % \
			(sys.argv[0],name,rack,rank,cpus,membership,mac,device,\
				module,ipaddr,netmask)


	def statusGUI(self):
		"Updates the list of nodes in 'Inserted Appliances' window"

		macs_n_names = ''
		ks = ''
		for (mac, name) in self.inserted:
			if name not in self.kickstarted:
				ks = ''
			elif self.kickstarted[name] == 0:
				ks = '( )'
			elif self.kickstarted[name] == 200:
				ks = '(*)'
			else:	# An error
				ks = '(%s)' % self.kickstarted[name]
			macs_n_names += '%s\t%s\t%s\n' % (mac, name, ks)

		self.textbox.setText(macs_n_names)

		self.form.draw()
		self.screen.refresh()


	def waitGUI(self):
		"""Shows a list of discovered but not kickstarted nodes
		for a few seconds."""

		not_done = ''
		hosts = self.kickstarted.keys()
		hosts.sort()
		for name in hosts:
			status = self.kickstarted[name]
			if status != 200:
				ks = '( )'
				if status:
					ks = '(%s)' % status
				not_done += '%s \t %s\n' % (name, ks)

		form = snack.GridForm(self.screen, 
			_("Not kickstarted, please wait..."), 1, 1)
		textbox = snack.Textbox(35, 4, not_done, scroll=1)
		form.add(textbox, 0,0)

		form.draw()
		self.screen.refresh()
		time.sleep(1)
		self.screen.popWindow()


	def replaceNode(self):
		if self.replace:
			#
			# need to get cabinet/rank from previous host before
			# removing it
			#
			query = """select rack,rank from nodes where
				name = "%s" """ % (self.replace)
			
			if self.sql.execute(query) > 0:	
				(self.cabinet, self.rank) = self.sql.fetchone()

			#
			# need to temporarily remove the lock file, otherwise
			# 'rocks sync config' won't update /etc/dhcpd.conf
			# and the other configuration files
			#
			lockFile = '/var/lock/insert-ethers'
			os.unlink(lockFile)
			os.system('/opt/rocks/bin/rocks remove host %s' %
				(self.replace))
			os.system('touch %s' % lockFile)


	def initializeRank(self):
		if self.rank != -1:
			# The user specified the rank
			return

		#
		# the rank flag was *not* specified by the user
		#
		# derive the rank value for this node from the
		# database
		#
		# the 'select rack,' and 'group by rack' clauses are
		# there because there is a weird side-effect with
		# using just max(rank) *and* when there are no rows
		# that match the membership/rack specification. the
		# select will return one row with the NULL value.
		# but, if we add 'select rack,' and 'group by rack'
		# then if no rows match, the select will return 0
		# rows, just like we want.
		#
		query = 'select rank,max(rank) from nodes where ' \
			'membership = %d and rack = %d ' \
			'group by rack' % \
				(self.membership, self.cabinet)

		if self.sql.execute(query) > 0:
			#
			# get the current highest rank value for
			# this cabinet
			#
			(rank, max_rank) = self.sql.fetchone()

			self.rank = max_rank + 1
		else:
			#
			# there are no configured machines for this
			# cabinet
			#
			self.rank = 0
		return



	def askuserIP(self, nodename):
		#
		# ask the user for an IP address
		#
		done = 0

		while not done:
			entry = snack.Entry(15)

			rc, values = snack.EntryWindow(self.screen,
				_("IP Address Selection"),
				_("Enter the IP address for host %s") % (nodename),
				[ (_("IP Address"), entry) ],
				buttons = [ 'Ok' ])

			ipaddr = entry.value()
			try:
				self.clusterdb.checkIP(ipaddr)
				self.setIPaddr(ipaddr)
				done = 1
			except ValueError:
				snack.ButtonChoiceWindow(self.screen,
					_("Duplicate IP"),
					_("The IP address (%s) already exists.\n\n"),
					_("Please select another.") % (ipaddr),
					buttons = [ _("OK") ])

		return ipaddr


	def getnetmask(self, dev):
		import subprocess
		import shlex

		#
		# check if bcast,netmask already specified
		#
		if self.netmask is not None and self.broadcast is not None:
			# The user specified broadcast, netmask
			return(self.broadcast,self.netmask)
		#
		# get an IP address
		#
		bcast = ''
		mask  = ''

		cmd = '/sbin/ifconfig %s' % dev
		p = subprocess.Popen(shlex.split(cmd), stdout = subprocess.PIPE)

		for line in p.stdout.readlines():
			tokens = string.split(line)

			for i in tokens:
				values = string.split(i, ':')

				if values[0] == 'Bcast':
					bcast = values[1]
				elif values[0] == 'Mask':
					mask = values[1]

		# Set the values into this node's in-memory object
		self.setNetmask(mask)
		self.setBroadcast(bcast)

		return (bcast, mask)

	def getnetwork(self,subnet):
		
		self.sql.execute("select subnet,netmask from subnets where name='%s'" % (subnet))
		network,netmask = self.sql.fetchone()
		return network,netmask
			
	def getnextIP(self, subnet):
	
		network,mask = self.getnetwork(subnet)
		mask_ip = rocks.ip.IPAddr(mask)
		network_ip = rocks.ip.IPAddr(network)
		bcast_ip = rocks.ip.IPAddr(network_ip | rocks.ip.IPAddr(~mask_ip))
		bcast = "%s" % (bcast_ip)
		
		if self.ipaddr is not None :
			return self.ipaddr

		if bcast != '' and mask != '':
		
			# Create the IPGenerator and if the user choose a 
			# base ip address to the IPGenerator to start there.
			# Should really be a method in the class to set this,
			# but I need this today on 3.2.0.  Revisit soon (mjk)
			
			ip = rocks.ip.IPGenerator(bcast, mask)
			if self.sql.ipBaseAddress:
				ip.addr = rocks.ip.IPAddr(
							self.sql.ipBaseAddress)

			#
			# look in the database for a free address
			#
			while 1:
			
				# Go to the next ip address.  Default is still
				# to count backwards, but allow the user to
				# set us to count forwards.
				
				ip.next(self.sql.ipIncrement)
				
				nodeid = self.sql.getNodeId(ip.curr())
				if nodeid is None:
					return ip.curr()

		#
		# if we make it to here, an error occurred
		#
		print 'error: getnextIP: could not get IP address ',
		print 'for device (%s)' % (dev)
		return '0.0.0.0'


	def addit(self, mac, nodename, ip, netmask):

		self.clusterdb.insert(nodename, self.membership, 
			self.cabinet, self.rank, mac, ip, netmask, self.subnet, self.osname)

		self.controller.added(nodename, self.clusterdb.getNodeId())
		self.restart_services = 1

		self.sql.link.commit()
			
		list = [(mac, nodename)]
		list.extend(self.inserted)
		self.inserted = list
		if self.distid is not None:
			self.kickstarted[nodename] = 0
		return 


	def printDiscovered(self, mac):
		form = snack.GridForm(self.screen,
			      _("Discovered New Appliance"), 1, 1)

		new_app = _("Discovered a new appliance with MAC (%s)") % (mac)
		textbox = snack.Textbox(len(new_app), 1, new_app)
		form.add(textbox, 0, 0)

		#
		# display the message for 2 seconds
		#
		form.draw()
		self.screen.refresh()
		time.sleep(2)
		self.screen.popWindow()
			

	def getNodename(self):
		# if the hostname was explicitly set on command line use it
		if self.hostname is not None:
			return self.hostname
		else:
			return '%s-%d-%d' % (self.basename, 
				self.cabinet, self.rank)

	def getFrontendName(self):
		name = self.sql.getGlobalVar('Kickstart','PrivateHostname')
		return name

	
	def discover(self, mac, dev):
		"Returns 'true' if we inserted a new node, 'false' otherwise."
		
		retval = 'false'

		query = 'select mac from networks where mac="%s"' % (mac)

		if self.sql.execute(query) == 0:
			nodename = self.getNodename()

			(bcast, netmask) = self.getnetmask(dev)
			if self.staticip == 'true':
				#
				# if the user requested to enter static
				# IP addresses, open the form
				#
				self.printDiscovered(mac)

				ipaddr = self.askuserIP(nodename)
				self.addit(mac, nodename, ipaddr, netmask)
			else:
				ipaddr = self.getnextIP(self.subnet)
				self.addit(mac, nodename, ipaddr, netmask)
				self.printDiscovered(mac)
				
			retval = 'true'

		return retval


	def checkDone(self, result, suggest_done):
		"""Returns true if we are ready to exit, false if some nodes
		have been discovered but not yet requested their kickstart
		file. """

		# Normal case
		if result == 'TIMER' and not suggest_done:
			return 0

		if result == 'F9':
			return 1

		# If the nodes are not kickstartable
		if self.kickstartable == False:
			return 1

		# Check if we can really go.
		ok = 1
		for status in self.kickstarted.values():
			if status != 200:
				ok = 0
				break
		if not ok:
			if result == 'F8':
				self.waitGUI()
		else:
			if suggest_done or result == 'F8':
				return 1
		return 0

	
	def listenKs(self, line):
		"""Look in log line for a kickstart request."""
		
		# Track accesses both with and without local certs.
		interesting = line.count('install/sbin/public/kickstart.cgi') \
			or line.count('install/sbin/kickstart.cgi') \
			or line.count('install/sbin/public/jumpstart.cgi')
		if not interesting:
			return 

		fields = line.split()
		try:
			status = int(fields[8])
		except:
			raise ValueError, _("Apache log file not well formed!")

		nodeid = int(self.sql.getNodeId(fields[0]))
		self.sql.execute('select name from nodes where id=%d' % nodeid)
		try:
			name, = self.sql.fetchone()
		except:
			if status == 200:
				raise InsertError, \
				 _("Unknown node %s got a kickstart file!") \
				 % fields[0]
			return

		if name not in self.kickstarted:
			return

		self.kickstarted[name] = status

		self.statusGUI()


	def listenDhcp(self, line):
		"""Look in log line for a DHCP discover message."""

		tokens = string.split(line[:-1])
		if len(tokens) > 5 and tokens[4] == 'dhcpd:' and \
		   (tokens[5] in [ 'DHCPDISCOVER', 'BOOTREQUEST' ]):
			
			# Remove the ":" from the interface value. If
			# this request does not come from our private
			# net, ignore it.

			interface = tokens[9].replace(':','').strip()
			
			# Next get the interface for the specified subnet.
			# This is done using a database lookup

			self.sql.execute("""select networks.device from
				networks, subnets, nodes where
				subnets.name='%s' and nodes.name='%s' 
				and networks.subnet=subnets.id and
				networks.node=nodes.id""" % (self.subnet,
				self.getFrontendName()))
			
			subnet_dev = self.sql.fetchone()[0]
			if interface != subnet_dev:
				return

			if self.discover(tokens[7], interface) == 'false':
				return

			self.statusGUI()

			#
			# for the cases where insert-ethers will only add one
			# node to the database (replace or rank flags are set),
			# then exit after one node is added
			#
			if self.only_add_one == 1:
				self.screen.drawRootText(0, 2, 
					_("Waiting for %s to kickstart...") %
					self.kickstarted.keys()[0])
				# Use exception structure so we dont have 
				# to keep track of the state.
				raise InsertDone, _("Suggest Done")

			if self.maxNew > 0:
				self.maxNew -= 1
				if self.maxNew == 0:
					raise InsertDone, _("Suggest Done")

			self.rank = self.rank + 1

		elif len(tokens) > 6 and tokens[4] == 'last' and \
			tokens[5] == 'message' and tokens[6] == 'repeated':

			n = os.uname()[1]
			shortname = n.split('.')[0]

			if tokens[3] == shortname:
				#
				# restart syslog (only if the repeated messages
				# are from the frontend).
				#
				# this addresses the case where a node is
				# PXE booting before insert-ethers is started.
				# by restarting syslog, the DHCP messages
				# will now show up (and not be flagged as
				# repeated).
				#
				cmd = '/sbin/service syslog restart '
				cmd += '> /dev/null 2>&1'
				os.system(cmd)

	def distDone(self):
		if os.path.exists(self.rocksdist_lockFile):
			self.warningGUI(_("Rocks distribution is not ready\n\n")
				+ _("Please wait for 'rocks create distro' to complete\n"))
			return 0
		return 1

			
	def run(self):
		if self.dump == 'true' :
			self.dumpCommands()
			return

		#
		# Batch does not make sense with --staticip, use --ipaddr.
		#
		if (self.mac is not None) and (self.staticip == 'false'):
			# Make sure plugins are loaded for hosts
			# added in via command-line parameters
			self.controller.loadPlugins(self.sql)

			self.batchCommand()

			# Cleanup the plugins
			self.controller.done()

			return

		self.startGUI()

		#
		# make sure 'rocks create distro' is not still building the
		# distro
		#
		if self.distDone() == 0:
			self.endGUI()
			return

		self.controller.loadPlugins(self.sql)

		try:
			if self.replace:
				self.replaceNode()
			if self.remove:
				self.endGUI()
				self.controller.done()
				print "Removed node %s" % self.replace
				return

			self.membershipGUI()
			self.initializeRank()

			if self.hostname:
				self.clusterdb.checkName(self.hostname)

		except (ValueError, InsertError), msg:
			self.errorGUI(msg)
			self.endGUI()
			sys.stderr.write(_("%s\n") % str(msg))
			return

		log = open('/var/log/messages', 'r')
		log.seek(0,2)

		kslog = open('/var/log/httpd/ssl_access_log','r')
		kslog.seek(0,2)

		#
		# key used to quit
		#
		self.screen.pushHelpLine(
			_(" Press <F8> to quit, press <F9> to force quit"))
		self.form.addHotKey('F8')
		self.form.addHotKey('F9')
		self.form.setTimer(1000)

		self.statusGUI()

		result = self.form.run()
		suggest_done = 0
		done = 0
		while not done:

			# Check syslog for a new line

			syslog_line = log.readline()
			if syslog_line and not suggest_done:
				try:
					self.listenDhcp(syslog_line)
				except InsertDone:
					suggest_done = 1

				except (ValueError, InsertError), msg:
					self.warningGUI(msg)
				continue

			# Check http log for a new line

			access_line = kslog.readline()
			if access_line:
				try:
					self.listenKs(access_line)
				except InsertError, msg:
					self.warningGUI(msg)
				continue

			result = self.form.run()
			done = self.checkDone(result, suggest_done)

		#
		# if there was a change to the database, restart some
		# services
		#
		if self.restart_services == 1:
			form = snack.GridForm(self.screen,
					      _("Restarting Services"), 1, 1)

			message = _("Restarting Services...")
			textbox = snack.Textbox(len(message), 1, message)
			form.add(textbox, 0, 0)
			form.draw()
			self.screen.refresh()

			self.controller.done()
				
			self.screen.popWindow()

		#
		# cleanup
		#
		log.close()
		self.endGUI()

		if self.lastmsg != '':
			sys.stderr.write(_("%s\n") % self.lastmsg)
			
	
	def runPublicOnly(self):
		"""Start GUI but don't listen. Simply opens up kickstart
		access to private network."""

		self.startGUI()
		self.screen.pushHelpLine(_(" Press <F8> to quit "))
		self.form.addHotKey('F8')
		self.textbox.setText(
			_("Kickstart access opened to %s,\n") +
			_("not listening...")
				% self.sql.getPrivateNet())
		self.form.run()
		self.endGUI()



class CreateDist(GUI):

	def __init__(self, app):
		GUI.__init__(self)
		self.app = app

	def buildDistribution(self):
		cwd = os.getcwd()
		os.chdir(self.app.dist.getRootPath())
		os.system('rocks-dist dist')
		os.chdir(cwd)
		print 'You may now run insert-ethers'
		
	def run(self):
		self.startGUI()
		self.warningGUI(_("Rocks distribution is not ready"))
		self.endGUI()
		
		self.buildDistribution()


		

class App(rocks.sql.Application):

	def __init__(self, argv):
		rocks.sql.Application.__init__(self, argv)
		self.rcfileHandler	= RCFileHandler
		self.insertor		= InsertEthers(self)
		self.dist		= None
		self.controller		= ServiceController()
		self.lockFile		= '/var/lock/insert-ethers'
		self.ipBaseAddress	= None
		self.ipIncrement	= -1
		self.doPublicMode	= 0
		self.doUpdate		= 0
		self.batch		= 0

		self.getopt.l.extend([
			('baseip=', 'ip address'),
			('basename=', 'basename'),
			('hostname=', 'hostname'),
			('ipaddr=', 'ip address'),
			('cabinet=', 'number'),
			('rack=', 'number'),
			('inc=', 'number'),
			('rank=', 'number'),
			('replace=', 'hostname'),
			('remove=', 'hostname'),
			('os=', 'the OS to install on the machines'),
			('update'),
			('staticip')
		])


	def parseArg(self, c):
		if rocks.sql.Application.parseArg(self, c):
			return 1
		elif c[0] == '--baseip':
			self.ipBaseAddress = c[1]
		elif c[0] == '--basename':
			self.insertor.setBasename(c[1])
		elif c[0] == '--hostname':
			self.insertor.setHostname(c[1])
			self.insertor.setMax(1)
		elif c[0] == '--ipaddr':
			self.insertor.setIPaddr(c[1])
			self.insertor.setMax(1)
		elif c[0] in ('--cabinet','--rack'):
			self.insertor.setCabinet(int(c[1]))
		elif c[0] == '--os':
			self.insertor.setOSName(c[1])
		elif c[0] == '--inc':
			self.ipIncrement = int(c[1])
		elif c[0] == '--rank':
			self.insertor.setRank(int(c[1]))
		elif c[0] == '--replace':
			self.insertor.setReplace(c[1])
		elif c[0] == '--remove':
			self.insertor.setRemove(c[1])
		elif c[0] == '--update':
			self.doUpdate = 1
		elif c[0] == '--staticip':
			self.insertor.setStatic()
			self.batch = 1
		return 0


	def getPrivateNet(self):
		try:
			net = self.getGlobalVar('Kickstart','PrivateNetwork')
			mask = self.getGlobalVar('Kickstart','PrivateNetmask')
		except:
			net = '10.0.0.0'
			mask = '255.0.0.0'
		
		return "%s/%s" % (net, mask)


	def cleanup(self):
		try:
			os.unlink(self.lockFile)
		except:
			pass


	def run(self):
		self.connect()

		if self.batch:
			# We may not be running as root user
			self.insertor.run()
			return

		if os.path.isfile(self.lockFile):
			raise _("error - lock file %s exists") % self.lockFile
			sys.exit(-1)
		else:
			os.system('touch %s' % self.lockFile)
			
		if self.doUpdate:
			self.controller.loadPlugins(self)
			self.controller.update()
			os.unlink(self.lockFile)
			return

		if self.doPublicMode:
			self.insertor.runPublicOnly()
		else:
			self.insertor.run()

		self.cleanup()



class RCFileHandler(rocks.sql.RCFileHandler):
    
	def __init__(self, app):
		rocks.sql.RCFileHandler.__init__(self, app)

	def startElement_nameserver(self, name, attrs):
		ns = attrs.get('name')



app = App(sys.argv)
app.parseArgs()
try:
	app.run()
except Exception, msg:
	sys.stderr.write('error - ' + str(msg) + '\n')
	app.cleanup()
	sys.exit(1)
