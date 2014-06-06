# $Id: __init__.py,v 1.9 2012/11/27 00:48:31 phil Exp $
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
# $Log: __init__.py,v $
# Revision 1.9  2012/11/27 00:48:31  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.8  2012/05/06 05:48:37  phil
# Copyright Storm for Mamba
#
# Revision 1.7  2011/07/23 02:30:40  phil
# Viper Copyright
#
# Revision 1.6  2011/04/21 02:30:59  anoop
# Parallel class now takes care of serializing
# tasks that may overrun the system. If more than
# a set number of tasks are running, then requesting
# tasks will wait till slots are available to run
#
# Each task now prints out error messages if they fail
# on remote hosts. This way, we can track which syncs failed
# and which ones succeeded.
#
# Revision 1.5  2011/04/14 23:08:58  anoop
# Move parallel class up one level, so that all sync commands can
# take advantage of it.
#
# Added rocks sync host sharedkey. This distributes the 411 shared key
# to compute nodes
#
# Revision 1.4  2010/09/07 23:53:03  bruno
# star power for gb
#
# Revision 1.3  2009/05/01 19:07:04  mjk
# chimi con queso
#
# Revision 1.2  2008/10/18 00:55:58  mjk
# copyright 5.1
#
# Revision 1.1  2008/08/22 23:26:38  bruno
# closer
#
#
#

import rocks.commands
import threading
import subprocess
import sys
import os
import fcntl
import time

# Threading limits.
max_threading = 512
timeout	= 30

# Arbitrary Process Limits. This will be
# ignored if this information is in the
# database as a rocks attribute.
max_processes = 32

# Counting Semaphore file
semfile = '/var/lock/rocks-sync-host.lock'

lock = threading.Lock()

class command(rocks.commands.HostArgumentProcessor,
        rocks.commands.sync.command):

	def getExecCommand(self, host, localhost=None):
		"""return a string for executing commands on local or remote nodes"""

		if not localhost:
			localhost = self.getHostnames(["localhost"])[0]

		#
		# do not use ssh for localhost (so we can fix FE with the network
		# down)
		#
		if host == localhost :
			return 'bash > /dev/null 2>&1 '
		else:
			return 'ssh -T -x %s bash > /dev/null 2>&1 ' % host


class Parallel(threading.Thread):
	def __init__(self, cmd, host=None):
		
		# The command to run
		self.cmd = cmd

		# thread lock object that controls thread access to
		# the semaphore file.
		self.s = lock
		
		# Host information so that we may print out
		# errors from the host
		self.host = host
		
		# Make sure each call can only start
		# "max_threading" number of threads
		while threading.activeCount() > max_threading:
			time.sleep(0.001)
		threading.Thread.__init__(self)

		# Check to see if semaphore file is present.
		# If not, create it. This file is going to be
		# used as a simple counting semaphore.
		# This code exists here in the unlikely event that the
		# semaphore file was somehow removed. The
		# semaphore file is created on the frontend
		# using "rocks sync config"
		if not os.path.exists(semfile):
			f = open(semfile, 'w+')
			f.write('%04d\n' % max_processes)
			f.close()

		self.lockfile = open(semfile, 'r+')


	def lock(self):
		"""Helper function to lock the thread and
		the semaphore file. This is necessary
		because, at any give time, a single thread
		of a single process must be the only entity
		updating/querying to the file"""

		# Acquire the threading lock first
		self.s.acquire()
		# Acquire the file lock
		fcntl.lockf(self.lockfile, fcntl.LOCK_EX)

	def unlock(self):
		"""Helper function to unlock the thread and
		the semaphore file"""

		# Release the file lock first
		fcntl.lockf(self.lockfile, fcntl.LOCK_UN)
		# Release the thread lock
		self.s.release()

	def getAvailProcSlots(self):
		"""Return the number of available
		processing slots"""
		self.lockfile.flush()
		self.lockfile.seek(0)
		return int(self.lockfile.readline())

	def incAvailProcSlots(self):
		"""This function serves to increment the
		contents the semaphore"""

		# Acquire a lock
		self.lock()

		# Read number of currently executing processes
		c0 = self.getAvailProcSlots()

		c1 = c0 + 1
		self.lockfile.seek(0)
		self.lockfile.write('%04d\n' % c1)
		self.lockfile.flush()
		# Unlock semaphore
		self.unlock()
	
	def decAvailProcSlots(self):
		"""This function serves to decrement the
		semaphore counter"""

		self.lock()
		# Read the semaphore count
		c0 = self.getAvailProcSlots()
		
		# If there are no slots available,
		# wait till one becomes available
		# before decrementing it again 
		while (c0 == 0):
			# Unlock semaphore so someone else
			# may decrement it.
			self.unlock()
			# Wait
			time.sleep(0.01)
			# Check again
			self.lock()
			c0 = self.getAvailProcSlots()

		# Once we reach this point, that means
		# we are free to update the semaphore
		# without a race condition
		# Decrement count of available slots.
		c1 = c0 - 1
		self.lockfile.seek(0)
		self.lockfile.write('%04d\n' % c1)
		self.lockfile.flush()
		# Unlock semaphore
		self.unlock()

	def run(self):

		# decrement available process slots
		self.decAvailProcSlots()

		# Run the command
		self.exec_proc()

		# increment available process slots
		self.incAvailProcSlots()
		
	def exec_proc(self):
		"""Execute the process requested"""

		try:
			p = os.system(self.cmd)
		except:
			# Lock stderr so that we can write safely
			fcntl.lockf(sys.stderr, fcntl.LOCK_EX)
			sys.stderr.flush()
			# print error message
			sys.stderr.write("%s running %s\nraised %s: %s\n" % \
				(self.name, self.cmd, \
				sys.exc_info()[0], sys.exc_info()[1]))
			sys.stderr.flush()
			# unlock stderr
			fcntl.lockf(sys.stderr, fcntl.LOCK_UN)
			# Always return. Otherwise, semaphore counter
			# will not be incremented. 
			return
		# If the command errors out
		if p != 0:
			# Lock stderr so that we can write safely
			fcntl.lockf(sys.stderr, fcntl.LOCK_EX)
			sys.stderr.flush()
			# print error code
			sys.stderr.write("Error running: %s\n" % self.cmd)
			sys.stderr.write("%s returned error code %d\n" \
				% (self.host, p))
			sys.stderr.flush()
			# unlock stderr
			fcntl.lockf(sys.stderr, fcntl.LOCK_UN)

RollName = "base"
