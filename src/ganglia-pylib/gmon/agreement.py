#!/opt/rocks/bin/python
#
# The Davis distributed agreement protocol for Rocks.
# Used to create and maintain an MPD ring.
#
# Original author: Federico Sacerdoti (fds@sdsc.edu) (2003)
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

import os
import random
import string
import gmon.events
from gmon.Gmetric import publish
import gmon.Network
import rocks.net


# An exception to raise if we cannot start our service.

class ServiceError(Exception):
	pass


# Using multiple inheritance to "mix-in" methods from the
# Metric class. Our first allegiance is to Metric.

class Agreement(gmon.events.Metric, rocks.net.Application):
	""" An implementation of a protocol that solves agreement
	in a distributed system. We call this immortal agreement, since
	the protocol never finishes. Nodes can join or leave at any time."""

	def __init__(self, app):
		gmon.events.Metric.__init__(self, app)
		rocks.net.Application.__init__(self)

		# The name of the ganglia metric we will use.
		self.metric = "Agreement-%s" % self.service()
		self.altmetric = "%s-Alt" % self.metric
		self.choice = None
		self.doorway = None
		self.lastchoice = None
		# Recommit flag: a stable property. True once we have commit
		# to a choice and then later were forced to reconsider.
		self.resetmode = 0

		# We use IP addresses so services can start even if
		# DNS is down. We dont know our color name until we parseArgs().
		self.color = None

		# Start in war mode since we are initially unconverged.
		self.frequency = self.warFrequency()
		self.verbose = 0


	def service(self):
		"The name of the service using Agreement."
		return 'raw'

	def name(self):
		return self.metric

	def warFrequency(self):
		"""Returns the war frequency in seconds. We have two frequencies, 'war'
		and 'peace'. War occurs when the protocol is converging and a leader
		has not been agreed upon."""
		return 15

	def peaceFrequency(self):
		"""Returns the peace frequency in seconds. Peace occupies the stable
		periods in the protocol. The peace frequency is calmer than during
		war."""
		return 300

	def atPeace(self):
		"""Returns true if we are at peace."""
		return (self.frequency == self.peaceFrequency())

	def commit(self):
		"""Call to derived classes, when agreement has been reached.
		Should return any commit info, such as a port number, etc. or
		raise a gmon.agreement.ServiceError on failure. Host, port for service
		is available from a call to getChannel()."""
		pass

	def checkhealth(self):
		"""A call to derived classes for them to check on their service.
		Called once per round if agreement has been reached."""
		pass

	def recommit(self):
		"""Call to derived classes when choice (in self.choice)
		has changed. Should be rare."""
		pass

	def getChannel(self):
		"""Returns the preffered doorway for a client to connect to this service. If
		None, then we are the kicker."""
		return self.doorway

	def getDoorway(self):
		"Same as getChannel."
		return self.doorway

	def reset(self):
		"""Uncommits this node and restarts the protocol."""
		self.color.uncommit()
		self.resetmode = 1

	def start(self):
		"""Starts or restarts our service. If successful, we
		record a non-null self.choice.info value."""

		if not self.kicker and not self.choice.hasCommit():
			# Cannot commit when kicker has not started yet. If they
			# die before committing, we will eventually choose another one.
			raise ServiceError

		if self.resetmode:
			startService = self.recommit
		else:
			startService = self.commit

		# Call the base class.
		info = startService()

		if self.kicker:
			# We set the service info for the color group.
			self.choice.commit(info)

		self.color.commit(info)


	def publishcolor(self):
		"""Publishes our color choice to Global Cluster state S."""

		# The tmax and dmax (time-to-live) of our messages.
		age = self.tmax()

		self.publish(self.metric, str(self.choice),
			tmax=age, dmax=age)

		# Only publish alternate if we have sucessfully commit, and are not
		# the leader.
		if not self.color.hasCommit():
			return
		if self.color == self.choice:
			return

		# Advertize an alternative entry point: our initial color,
		# and local commit info.
		self.publish(self.altmetric, str(self.color),
			tmax=age, dmax=age)


	def sendAlert(self):
		"""Sends an alert to peers that we have switched from a peaceful
		state to one of emergency. Does not need to be long-lived."""
		self.publish("%s-alert" % self.metric, "wake up", 
			tmax=20, dmax=20)
			

	def split(self, color_tuple):
		"""Safely returns the color and commit info portions
		of a color tuple"""

		if not color_tuple:
			return None, None

		t = string.split(color_tuple,":")
		if len(t) > 1:
			return t[0], t[1]
		else:
			return t[0], None


	def findColorPeer(self, color):
		"""Find another service that has started in our
		color group. Essentially will be a random peer, and is
		used for load balancing."""

		for m in self.allcolors.values():
			c, info = Color(m["VAL"]).getChannel()
			host = m["IP"]

			if c and c == color:
				if host in self.peers:
					return Color(self.peers[host]['VAL'])

		return None


	def getcolors(self):
		"""Collects the set of color groups in Global Clusters state S,
		and removes stale members."""

		colors = {}
		seen = {}

		for m in self.allcolors.values():
			color = Color(m["VAL"])
			c, info = color.getChannel()

			# Always prefer Alternate entry points, as they are
			# confirmations of a running service.

			if c not in seen:
				p = self.findColorPeer(c)
				if p:
					seen[c] = 1
					color.setPeer(p)
				else:
					# If there are no alternates and the host
					# with this color is not participating,
					# discard this color as a candidate. Subtle.
					if c not in self.allcolors:
						continue

			if c not in colors:
				colors[c] = color
			else:
				colors[c].grow(info)

		return colors

		
	def choose(self, colors):
		"""The core logic of the protocol. Choose the biggest color group,
		break ties randomly."""

		if len(colors) == 0:
			# Choose our own color.
			return Color(self.color.getColor())

		else:
			# We have at least one color group.
			max = 0

			# Invariant: biggest always contains the colors who have
			# the largest size. (More than one for a tie).
			biggest = []

			for color in colors.values():

				colorsize = color.getSize()

				if not max or max < colorsize:
					max = colorsize
					# Max has increased, reset biggest.
					biggest = []
					biggest.append(color)
				elif max == colorsize:
					biggest.append(color)

			# Choose a random color from biggest.
			return random.choice(biggest)


	def run(self):
		"""Called at the beginning of each round r."""

		if not self.color:
			self.parseRC(rcbase='rocks')
			try:
				self.color = Color(self.privateIP())
			except Exception, msg:
				self.warning("%s, cannot start Agreement." % msg)
				return
			# An optimization: when we start, make sure everyone
			# is awake so we can converge fast (we need mesgs from
			# over half the cluster before committing.)
			self.sendAlert()

		self.lastchoice = self.choice
		self.kicker = 0

		# Get metrics from our peers.
		# Query result is q[host IP] = metric.

		r = self.getReceptor(self.metric)
		if not r:
			self.warning("Cannot find a receptor for %s" % self.metric)
			return

		a = self.getReceptor(self.altmetric)
		if not a:
			self.warning("Cannot find a receptor for %s" % altmetric)
			return

		r.getLock()
		a.getLock()

		# Timeout old messages
		r.clean()
		a.clean()
		
		self.allcolors = r.getMetrics()
		self.peers = a.getMetrics()

		if self.verbose:
			print "All colors: %s" % self.allcolors
			print "Peers: %s" % self.peers

		colors = self.getcolors()

		r.releaseLock()
		a.releaseLock()

		self.choice = self.choose(colors)

		if self.verbose:
			print "Cleaned Colors are %s" % colors
			print "Choosing color %s" % self.choice

		# Assume the worst.
		self.frequency = self.warFrequency()
		
		if self.color.hasCommit():
			try:
				self.checkhealth()
			except ServiceError:
				# An optimization: to speed the removal of stale msgs, we
				# publish once at our war freq (lower TTL).
				self.publishcolor()
				
				# We will need to choose another entry point
				# into the service. Any down entry points will
				# eventually time out and be removed from
				# candidacy.
				self.color.uncommit()
				
				# Most of our peers are at peace, and we know
				# every node probably will need attention now.
				self.sendAlert()
				return

			# Rarely we may have to recommit to another color.
			if self.lastchoice != self.choice:
				self.reset()
				return
			
			# We can relax (the normal case).
			self.frequency = self.peaceFrequency()
			
		else:
			# We kick off the service if we have chosen our own color
			# and no alternates for the color exist.
			if self.choice == self.color and not self.choice.getPeer():
				self.kicker = 1
				self.doorway = (None, None)

			else:
				self.doorway = self.choice.getDoorway()

			# Commit only if our group will definately be chosen.
			# An optimization that relies on (an eventual) accurate 
			# knowledge of |V|. Our estimator should be ok.

			if self.choice.getSize() > (self.app.clusterSize() / 2):
				try:
					self.start()
				except ServiceError:
					# Let our metrics time out.
					return
			else:
				# Any choiceinfo here is a relic of past generations.
				self.choice.uncommit()

		self.publishcolor()



class Color:
	"""Represents a color group in the Agreement protocol.
	A small helper class."""

	def __init__(self, color, peer=None):
		self.size = 1
		t = color.split(':')
		self.color = t[0]
		self.info = ''
		if len(t) > 1:
			self.info = t[1]
		self.peer = peer

	def __cmp__(self, a):
		if not a: 
			return -1

		if a.getColor() == self.color:
			return 0
		else:
			return -1

	def __str__(self):
		return "%s:%s" % self.getChannel()

	def grow(self, info):
		"""Grow the size of this group by one. The info
		is generally the port of the leader service"""

		if not self.info:
			self.info = info
		self.size = self.size + 1

	def getSize(self):
		return self.size

	def getColor(self):
		return self.color
		
	def getPort(self):
		return self.info
		
	def getInfo(self):
		return self.info

	def getChannel(self):
		return (self.color, self.info)

	def getDoorway(self):
		"""Return an entry point into the color group. To load balance 
		a bit we favor our peer entry point over the leader."""
		if self.peer:
			return self.peer.getChannel()
		else:
			return self.getChannel()

	def uncommit(self):
		self.info = ''

	def commit(self, info):
		"""Committed state is represented by a non-zero
		info number"""

		if not info:
			info = os.getpid()
		self.info = info

	def setColor(self, val):
		self.color = val

	def setPeer(self, p):
		"""The peer is a random active running service in our color
		group."""
		self.peer = p

	def getPeer(self):
		return self.peer

	def hasCommit(self):
		if self.info:
			return 1
		else:
			return 0



class Listener(gmon.events.Listener):
	"""A convenience class to quickly make the Greceptor listeners
	necessary to support the Agreement protocol. Since a listener
	can only respond to a single name (hash lookup issues prevent
	wildcard names), we need two modules for each Agreement service:
	one for the Agreement-[service] metric, and one for
	Agreement-[service]-Alt. """

	def __init__(self, app):
		gmon.events.Listener.__init__(self, app)

	def name(self):
		"""The metric name we're interested in. Must match
		our agreement metric module."""
		return "Agreement-%s" % self.service()

	def service(self):
		return "raw"

	def run(self, metric):
		self.receptor.getLock()
		self.receptor.addMetric(metric)
		self.receptor.releaseLock()



class AlertListener(gmon.events.Listener):
	"""A convenience listener class that can jolt our metric if 
	necessary. Responds to Agreement instability alerts from
	other nodes. Alerts arrive based on agreement.checkhealth() calls."""
	
	def __init__(self, app):
		gmon.events.Listener.__init__(self, app)
		self.agreement_metric = None
		
	def name(self):
		return "Agreement-%s-alert" % self.service()
		
	def service(self):
		return "raw"
		
	def run(self, alert):
		"""Called when we have received an alert from a
		node. May not make entirely accurate decisions (there is
		no lock on self.frequency, which determines atPeace()),
		but usually will be ok. Especially since there will be
		multiple alerts per emergency."""
		
		# Must call this here since the metric does not exist
		# in our constructor. Have to be careful with this metric 
		# since there are few locks on its internal state.
		if not self.agreement_metric:
			try:
				self.agreement_metric = self.app.director.\
					getMetric("Agreement-%s" % self.service())
			except gmon.director.ReceptorError:
				return
				
		if self.agreement_metric.atPeace():
			self.agreement_metric.jolt()
		# else if we are at war, ignore alert.


