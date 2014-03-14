#! @PYTHON@
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
# $Log: rocks.py,v $
# Revision 1.32  2012/11/27 00:48:09  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.31  2012/05/06 05:48:18  phil
# Copyright Storm for Mamba
#
# Revision 1.30  2011/07/23 02:30:24  phil
# Viper Copyright
#
# Revision 1.29  2011/05/26 23:16:59  phil
# Disambiguate the command line
#
# Revision 1.28  2011/05/13 21:37:35  anoop
# Treat each user as themselves
#
# Revision 1.27  2011/05/12 21:44:54  anoop
# Dont barf if space exists around a password
#
# Revision 1.26  2010/09/07 23:52:49  bruno
# star power for gb
#
# Revision 1.25  2009/06/05 19:56:25  bruno
# make mtu optional
#
# Revision 1.24  2009/06/05 18:35:54  mjk
# Try UNIX socket first, then network socket for DB connect
#
# Revision 1.23  2009/06/03 18:53:43  mjk
# - sudo support for ubuntu boy (this is cool)
# - connect to DB over the network socket not the UNIX domain socket
# - added x11 param to rocks.run.host to disable x11forwarding
#
# Revision 1.22  2009/05/01 19:06:50  mjk
# chimi con queso
#
# Revision 1.21  2009/04/28 22:00:33  mjk
# use foundation db
#
# Revision 1.20  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.19  2008/03/06 23:41:33  mjk
# copyright storm on
#
# Revision 1.18  2007/09/28 18:50:35  anoop
# Continue quietly, if database not present. This gives us a chance to run
# the command line utils in the installation environments on both the frontend
# and on the compute node. This is crucial if we want to move away from using
# kpp and kgen, and towards a standard processing infrastructure.
#
# Revision 1.17  2007/08/14 21:20:28  anoop
# Cannot break command line now.
#
# Revision 1.16  2007/08/14 20:11:17  anoop
# Perhaps it's time we started using foundation mysql
# rather than Redhat supplied Mysql
#
# Revision 1.15  2007/07/05 19:43:52  bruno
# perms
#
# Revision 1.14  2007/07/03 17:49:50  phil
# Actually use the password stored in /root/.my.cnf
#
# Revision 1.13  2007/07/03 04:58:42  phil
# Add a password for apache access to the database.
# Randomly generate password and store in /root/.my.cnf.
# Modify rocks.py and sql.py to read the password, if available
#
# Revision 1.12  2007/06/19 16:42:39  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.11  2007/05/25 03:12:30  mjk
# - help takes a flag instead of an argument
# - added bash/readline completion
#
# Revision 1.10  2007/04/19 22:49:57  bruno
# might be off by one
#
# Revision 1.9  2007/04/19 22:45:12  mjk
# control newlines at end of output
#
# Revision 1.8  2007/02/28 03:06:28  mjk
# - "rocks list host xml" replaces kpp
# - kickstart.cgi uses "rocks list host xml"
# - indirects in node xml now works
#
# Revision 1.7  2007/02/08 17:48:48  mjk
# - single syslog open/close
# - log plug-ins
#
# Revision 1.6  2007/02/08 17:31:24  mjk
# Added root check for root-only commands
# Added syslog tracking to record changes to the cluster
#
# Revision 1.5  2006/12/18 19:52:49  mjk
# fix help
#
# Revision 1.4  2006/12/15 23:53:18  bruno
# only print if you have something to say
#
# Revision 1.3  2006/12/06 23:45:11  mjk
# added xxxText methods
#
# Revision 1.2  2006/11/22 02:15:46  mjk
# working version
#
# Revision 1.1  2006/11/02 21:49:46  mjk
# prototype
#

import os
import pwd
import sys
import string
import syslog
import rocks	# need this so we can load the rocks.commands.* modules


    
syslog.openlog('rockscommand', syslog.LOG_PID, syslog.LOG_LOCAL0)



# Several Commands are run in the installation environment before the
# cluster database is created.  To enable this we only attempt to establish
# a database connection, if it fails it is not considered an error.
try:
	import sqlalchemy # needed for the exception
	import rocks.db.helper

	database = rocks.db.helper.DatabaseHelper()
	database.connect()

except ImportError:
	pass
except sqlalchemy.exc.OperationalError:
	pass



# If the command line is empty treat as if the user typed "rocks help"

if len(sys.argv) == 1:
	args = [ 'list', 'help' ]
else:
	args = sys.argv[1:]
	
# Check if the rocks command has been quoted.

module = None
cmd = args[0].split()
if len(cmd) > 1:
	s = 'rocks.commands.%s' % string.join(cmd, '.')
	try:
		__import__(s)
		module = eval(s)
		i = 1
	except:
		module = None

# Treat the entire command line as if it were a python command module and
# keep popping arguments off the end until we get a match.  If no match is
# found issue an error.

if not module:
	for i in range(len(args), 0, -1):
		s = 'rocks.commands.%s' % string.join(args[:i], '.')
		try:
			__import__(s)
			module = eval(s)
			if module:
				break
		except ImportError:
			continue

if not module:
	print 'error - invalid rocks command "%s"' % args[0]
	sys.exit(-1)

name = string.join(string.split(s, '.')[2:], ' ')


# If we can load the command object then fall through and invoke the run()
# method.  Otherwise the user did not give a complete command line and
# we call the help command based on the partial command given.

try:	
	command   = getattr(module, 'Command')(database)
except AttributeError:
	import rocks.commands.list.help
	help = rocks.commands.list.help.Command(database)
	fullmodpath = s.split('.')
	submodpath  = string.join(fullmodpath[2:], '/')
	help.run({'subdir': submodpath}, [])
	print help.getText()
	sys.exit(-1)

if command.MustBeRoot and not (command.isRootUser() or command.isApacheUser()):
	os.system('sudo %s' % string.join(sys.argv,' '))
else:
	command.runWrapper(name, args[i:])
	text = command.getText()
	if len(text) > 0:
		print text,
		if text[len(text)-1] != '\n':
			print


syslog.closelog()


