#!/opt/rocks/bin/python
#
# A script to run a greceptor metric module without the daemon. 
# Does not require rocks.app, so as to be easy to use for 3rd party
# applications. Intended to help run metrics from cron, for example.
#
# Requires that certain files exist, such as gmon.events.
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
# Original Author: Federico Sacerdoti (fds@sdsc.edu)
# 
# $Log: grunner.py,v $
# Revision 1.4  2009/05/01 19:07:09  mjk
# chimi con queso
#
# Revision 1.3  2008/10/18 00:56:02  mjk
# copyright 5.1
#
# Revision 1.2  2008/03/06 23:41:45  mjk
# copyright storm on
#
# Revision 1.1  2008/01/04 23:04:44  bruno
# moved ganglia-pylib and receptor from hpc to base roll
#
# Revision 1.9  2007/06/23 04:03:39  mjk
# mars hill copyright
#
# Revision 1.8  2006/09/11 22:48:53  mjk
# monkey face copyright
#
# Revision 1.7  2006/08/10 00:10:58  mjk
# 4.2 copyright
#
# Revision 1.6  2006/01/16 06:49:11  mjk
# fix python path for source built foundation python
#
# Revision 1.5  2005/10/12 18:09:49  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:03:26  mjk
# updated copyright
#
# Revision 1.3  2005/07/26 21:24:39  bruno
# updated to use the rocks foundation
#
# Revision 1.2  2005/05/24 21:22:51  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/12 00:50:26  fds
# Greceptor. Moved from monolithic source tree.
#
# Revision 1.3  2004/03/25 03:15:04  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.2  2004/02/16 20:25:14  fds
# Allow metrics to bow out, like in greceptor.
#
# Revision 1.1  2004/02/16 20:13:23  fds
# A small script that will run a ganglia python metric like greceptor.
# Use for cron instead of greceptor.
#
#

import sys
import syslog
import types
import os



class App:

	def __init__(self, argv):
		if len(argv) > 1:
			self.metricfile = argv[1]
			if self.metricfile.endswith(".py"):
				self.metricfile = self.metricfile[:-3]
		else:
			print "Please specify a ganglia metric file."
			sys.exit(1)
			
		self.doMetric = 0


	def schedule(self, event, now=0):
		self.doMetric = 1


	def loadModules(self, file):
		"""Import all the python code in a directory. Path is 
		like gmon.metrics"""

		info = "Grunner running metrics in %s" % file

		mod = __import__(file)
		try:
			initEvents = getattr(mod, "initEvents")
		except AttributeError:
			info = info + "(no initEvents(), skipping) "
			return []

		syslog.syslog(info)

		# Call the entry point to get a tuple of event
		# classes.
		return initEvents()
	

	def startEvent(self, metric_class):

		if type(metric_class) == types.ClassType:
			metric = metric_class(self)
			metric.schedule(self)
			if not self.doMetric:
				raise Exception, "'%s' does not want to be run." % metric.name()
			#print "Publishing metric %s" % metric.name()
			metric.run()


	def run(self):

		events = self.loadModules(self.metricfile)

		if not events:
			raise Exception, "No metrics found"

		if type(events) == types.TupleType:
			for event in events:
				self.startEvent(event)
		else:
			# There is only one metric class in file.
			self.startEvent(events)



# Main
app=App(sys.argv)
try:
	app.run()
except Exception, msg:
	print "**Error: %s" % msg
	sys.exit(1)

