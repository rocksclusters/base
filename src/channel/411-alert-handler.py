#! /opt/rocks/bin/python
#
# Pulled out of the listener code and made a standalone program that
# the Rocks RPC Channel 411-alert calls directly.  This will eventually
# go away also.
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
# $Log: 411-alert-handler.py,v $
# Revision 1.7  2012/11/27 00:48:08  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.6  2012/05/06 05:48:18  phil
# Copyright Storm for Mamba
#
# Revision 1.5  2011/08/05 00:33:08  anoop
# Run post section of a filter once the file is written
#
# Revision 1.4  2011/07/23 02:30:24  phil
# Viper Copyright
#
# Revision 1.3  2010/10/21 22:03:18  mjk
# - linux and solaris both send only .info and above to the frontend
#   debug stays off the network
# - changed syslog levels to debug (see above)
# - proper wait return code handling with W* macros
#
# Revision 1.2  2010/10/21 20:51:17  mjk
# - timestamp is now a timeval (microseconds)
# - re-entry testing is done in 411-alert-handler using a pickle file for state
# - more logging
#
# Looks good, but need to turn down the logging to keep the network quite.
#
# Revision 1.1  2010/10/20 21:12:34  mjk
# works
#
# Revision 1.6  2010/09/07 23:52:48  bruno
# star power for gb
#
# Revision 1.5  2009/05/01 19:06:49  mjk
# chimi con queso
#
# Revision 1.4  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.3  2008/07/16 22:33:59  bruno
# don't republish 411 alerts.
#
# this causes a traffic storm on large clusters and all other 411 listeners
# will toss the message any way (411 listeners only accept messages from the
# frontend).
#
# Revision 1.2  2008/03/06 23:41:32  mjk
# copyright storm on
#
# Revision 1.1  2007/12/10 21:28:33  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.10  2007/06/23 04:03:38  mjk
# mars hill copyright
#
# Revision 1.9  2006/09/11 22:48:46  mjk
# monkey face copyright
#
# Revision 1.8  2006/08/10 00:10:53  mjk
# 4.2 copyright
#
# Revision 1.7  2006/01/16 23:05:35  bruno
# applied fix from federico sacerdoti
#
# Revision 1.6  2006/01/16 06:49:09  mjk
# fix python path for source built foundation python
#
# Revision 1.5  2005/10/12 18:09:41  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:03:18  mjk
# updated copyright
#
# Revision 1.3  2005/08/08 21:24:59  mjk
# foundation
#
# Revision 1.2  2005/05/24 21:22:44  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/01 02:02:40  mjk
# moved from core to base
#
# Revision 1.29  2005/01/24 23:37:44  fds
# Using my simplehttp library for transfers in 411. No memory leaks, no more
# forking from threads. TCP retries now greatly simplified in the listener.
#
# Revision 1.28  2005/01/04 22:09:02  fds
# Retry multiple times if necessary, dont rely on TCP.
#
# Revision 1.27  2004/11/02 01:39:53  fds
# Converge faster by increasing load on frontend papache server (suggesion by phil).
#
# Revision 1.26  2004/11/02 00:43:26  fds
# Listening to Phil. Put more load on frontend apache's server. Should lead
# to faster 411 convergence on large clusters. Also use correct mcast channel.
#
# Revision 1.25  2004/10/04 19:19:09  fds
# A non-zero DMAX for 411 feedback metrics. Made possible by new
# cluster-gmetric page.
#
# Revision 1.24  2004/09/07 21:50:22  fds
# 80-col, better error handling.
#
# Revision 1.23  2004/07/21 17:46:46  fds
# Alerts handle group names with spaces. Important
# for Rocks Membership names
#
# Revision 1.22  2004/07/21 00:50:25  fds
# 411get listing now respects groups. Moved group processing into
# base class.
#
# Revision 1.21  2004/07/20 19:47:17  fds
# 411 group support. Also cleaned out some depricated options.
#
# Revision 1.20  2004/06/08 21:41:35  fds
# 80-col code and fix error reporting.
#
# Revision 1.19  2004/03/25 03:15:11  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.18  2004/03/09 18:27:11  fds
# Dont graph info metric, type is now timestamp.
#
# Revision 1.17  2004/03/09 02:31:30  fds
# 411 hardcore. Achieve reliable multicast the same way ganglia does:
# repeat yourself until you are hoarse. Use 'receptor' classes to inform
# a Repeater411 metric of new alerts, which are then re-published every
# 20sec for an hour.
#
# Assumes receipt of your own mcast packet is reliable. This design should
# achieve reliable 411 alerts in the long run, while maintaining simplicity.
#
# Revision 1.16  2003/10/30 02:31:33  fds
# Small changes
#
# Revision 1.15  2003/10/20 19:31:38  fds
# Respect to master scores, better doc formatting.
# Turned off debug mode for all modules.
#
# Revision 1.14  2003/09/26 17:33:54  fds
# Cleaner isUs check, not overly Exceptionriffic.
#
# Revision 1.13  2003/09/25 18:18:08  fds
# Ignoring alerts from ourselves.
#
# Revision 1.12  2003/09/09 01:44:42  fds
# Using Master helper class. Started
# structure for complex 411 service.
#
# Revision 1.11  2003/09/08 05:17:53  fds
# On our way to using URLs
#
# Revision 1.10  2003/09/08 05:09:05  fds
# Parsing character data in conf file. Not Used, ugly code, slow.
#
# Revision 1.9  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.8  2003/08/13 21:48:27  fds
# Saved case where child does not exit cleanly on failure.
#
# Revision 1.7  2003/08/09 01:01:31  fds
# Dont do too much in the constructor.
#
# Revision 1.6  2003/07/23 18:47:55  fds
# Added 'disable' option to the config file.
#
# Revision 1.5  2003/07/22 22:19:45  fds
# Getting ready for packaging.
#
# Revision 1.4  2003/07/21 23:46:22  fds
# Listener does not need a configuration file, can incorporate new masters dynamically.
#
# Revision 1.3  2003/07/16 21:28:56  fds
# Sign, verify deal with base64 signatures now, header format improved.
#
# Revision 1.2  2003/07/16 06:19:48  fds
# Moved sign and verify tasks to service411. Allowed for multiple master
# servers in listeners, even dynamically discovered ones (as long as they
# are identified and put into self.masters). Master servers identified by
# IP address.
#
# Revision 1.1  2003/07/15 23:48:57  fds
# New 411 alert design.
#
# Revision 1.1  2003/07/02 23:26:09  fds
# A low frequency 411 pull engine (Ganglia independant).
#
#

import os
import sys
import random
import syslog
import urllib
import pickle
import rocks.service411


class Listen411(rocks.service411.Service411):

	def __init__(self):
		rocks.service411.Service411.__init__(self)

	def run(self, url, sig):

		# If this is called as a handler it will have a signature that needs
		# to be verfified.  Otherwise allow to be called manually to update
		# a file.  This might become the new 411get method.
		
		if sig and not self.verify(url, sig):
			syslog.syslog(syslog.LOG_ERR, 'bad signature')
			return

		url = urllib.unquote(url)

		# If this file is not registered in one of our groups it belongs
		# to other nodes (we just saw it because the alert is broadcasted).
		# In the case just ignore it.
		
		groupPaths = []
		for g in self.groups:
			if not g:
				continue
			groupPaths.append('/'.join(g))

		master = rocks.service411.Master(url)
		path  = master.getDir()
		group = path.replace(self.urldir, '')
		group = group[2:-1]

		found = False
		for g in groupPaths:
			if g.find(group) == 0:
				found = True
		if not found:
			return

		# The alert was for us, so fetch the file using a random retry if
		# the server is busy.
		
		retry = 3
		while retry:
			try:
				contents, meta = self.get(url)
				self.write(contents, meta)
				syslog.syslog(syslog.LOG_INFO, 'wrote (file="%s")' % url)
				try:
					f = getattr(self.plugin, 'post')
					f()
				except:
					pass
				retry = 0
			except:
				import time
				time.sleep(random.uniform(0, 30))
				# we don't syslog this since the msg would also
				# hit the network to the frontend, making things worse.
				retry -= 1


syslog.openlog('411-alert-handler', syslog.LOG_PID, syslog.LOG_LOCAL0)

if len(sys.argv) == 5:
	filename  = sys.argv[1]
	signature = sys.argv[2]
	sec       = long(sys.argv[3])
	usec      = int(sys.argv[4])
else:
	sys.exit(-1);

time = sec + usec / 1e6
syslog.syslog(syslog.LOG_DEBUG, 'handle (file="%s" time="%.6f")' % (filename, time))

# 411-alert-handler.pkl keeps a list of timestamps of all the file alerts we have
# seen.  If an alert has an identical or early timestamp it is assumed to be a
# repeated message and is ignored.  We also return 1 to indicate the repeat.

timestamps = {}
if os.path.exists('/tmp/411-alert-handler.pkl'):
	fin = open('/tmp/411-alert-handler.pkl', 'rb')
	try:
		timestamps = pickle.load(fin)
	except:
		# something went awry file is probably corrupted
		os.remove('/tmp/411-alert-handler.pkl')
	fin.close()

if timestamps.has_key(filename) and timestamps[filename] == time:
	syslog.syslog(syslog.LOG_DEBUG, 'dup (file="%s" time="%.6f")' % (filename, time))
	sys.exit(1)

timestamps[filename] = time
	
# Call the old (modified) listener class code to verify the signature, download the
# file, and update the file on disk.

handler = Listen411()
handler.run(filename, signature)

# Write the updated timestamps to disk, for our next run.

fout = open('/tmp/411-alert-handler.pkl', 'wb')
pickle.dump(timestamps, fout)
fout.close()

sys.exit(0)
