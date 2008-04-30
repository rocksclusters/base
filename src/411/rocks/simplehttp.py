#!/opt/rocks/bin/python
#
# Class and funtions to do simple http GETs without memory leaks
# and other insidious problems of python's standard httplib module.
#
# Original Author 2005 Federico Sacerdoti 
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
# $Log: simplehttp.py,v $
# Revision 1.2  2008/03/06 23:41:32  mjk
# copyright storm on
#
# Revision 1.1  2007/12/10 21:28:33  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.8  2007/06/23 04:03:38  mjk
# mars hill copyright
#
# Revision 1.7  2006/09/11 22:48:48  mjk
# monkey face copyright
#
# Revision 1.6  2006/08/10 00:10:53  mjk
# 4.2 copyright
#
# Revision 1.5  2006/06/30 12:26:31  bruno
# moved all ganglia python code in hpc roll to point to the rocks foundation
# python
#
# Revision 1.4  2005/10/12 18:09:42  mjk
# final copyright for 4.1
#
# Revision 1.3  2005/09/16 01:03:19  mjk
# updated copyright
#
# Revision 1.2  2005/05/24 21:22:45  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/01 02:02:40  mjk
# moved from core to base
#
# Revision 1.1  2005/01/24 23:37:46  fds
# Using my simplehttp library for transfers in 411. No memory leaks, no more
# forking from threads. TCP retries now greatly simplified in the listener.
#
#

import socket

class HTTPException(Exception):
	pass

class IncompleteRead(HTTPException):
	def __init__(self, partial):
		self.partial = partial


class HTTPConnection:
	"""A simple HTTP client class without the memory leaks and other
	insidious problems of Python's standard httplib module. Will probably
	only work with HTTP/1.1 servers, and probably only apache.
	"""

	def __init__(self, server, port=80):
		self.peer = server
		self.port = port
		self.sock = None
		self.headers = {}
		self.fd = None
		self.status = 0
		self.done = 0
		# States
		self.connected = 0
		self.requested = 0
		self.headed = 0


	def setPeer(self, server):
		self.peer = server

	def getPeer(self, server):
		return self.peer

	def setPort(self, port):
		self.port = port

	def getPort(self):
		return self.port

	def getStatus(self):
		return self.status

	def getHeaders(self):
		return self.headers

	def isConnected(self):
		return self.connected

	def connect(self):
		if self.connected:
			raise HTTPException, "Please close() first"
		# Use TCP
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((self.peer, self.port))
		self.connected = 1


	def request(self, method, url, body='', headers=''):
		"""Args are meant to be the same as the httplib function
		of the same name. Method is like "GET" and url is the 
		selector, like "/my-page.html". Headers are a dictionary
		of key,value pairs that will be sent as key: value."""

		if not self.connected:
			raise HTTPException, "I am not connected"

		self.sock.send('%s %s HTTP/1.1\n' % (method, url))
		self.sock.send('Host: %s:%s\n' % (self.peer, self.port))
		self.sock.send('Accept-Encoding: identity\n')
		if body:
			self.sock.send('Content-Length: %d\n' % len(body))
		if headers:
			for key, val in headers.items():
				self.sock.send('%s: %s\n' % (key, val))
		self.sock.send('\n')
		if body:
			self.sock.send(body)

		self.requested = 1


	def getresponse(self):
		"""Returns a dictionary with Status: XXX, Reason: YYYY
		and the rest of the headers in it."""

		if not self.requested:
			raise HTTPException, "I have not made a request"

		self.headers = {}
		self.fd = self.sock.makefile('rb',0)
		self.status = 0
		while 1:
			line = self.fd.readline()
			if line == "\r\n":
				break
			if not self.status:
				tok = line.split()
				self.headers['HTTP'] = tok[0].split('/')[1]
				self.headers['status'] = int(tok[1])
				self.headers['reason'] = tok[2]
				self.status = tok[1]
			else:
				key, val = line.split(':',1)
				self.headers[key.lower()] = val.strip()

		# Get some meta-data for the read
		self.length = None
		if 'content-length' in self.headers:
			self.length = int(self.headers['content-length'])
		self.will_close = 0
		if 'connection' in self.headers:
			if self.headers['connection'].count('close'):
				self.will_close = 1

		self.headed = 1
		return self.headers
		

	def safeRead(self, amt):
		"""Modeled after std httplib. Used when there should be amt
		bytes available to read. If we reach an EOF (or are interrupted
		by a signal at the end of our loop) we will raise an
		IncompleteRead exception."""

		contents = ''
		while amt > 0:
			chunk = self.fp.read(amt)
			if not chunk:
				raise IncompleteRead(contents)
			contents += chunk
			amt -= len(chunk)
		return contents


	def read(self, amt=None):
		"""Returns the contents of the response. Can be called multiple
		times, will return a 0-length string if no more data is
		available.
		"""

		if not self.headed:
			raise HTTPException, "Read the response first"

		if self.done:
			return ''

		contents = ''
		if amt is None:
			if self.will_close:
				# Unbounded read, normal case.
				contents = self.fd.read()
			else:
				contents = self.safeRead(self.length)
			self.readDone()
			return contents
		else:
			# Buffered, chunked read
			if not self.length:
				raise HTTPException, "Cannot find content-length, try non-buffered read"
			if amt > self.length:
				amt = self.length
			self.length -= amt
			contents = self.fd.read(amt)
		
		return contents


	def readDone(self):
		self.done = 1
		self.fd.close()
		self.fd = None


	def reset(self):
		"""Close and clear any previous connections."""

		if self.sock:
			self.sock.close()
			self.sock = None
		self.headers = {}
		if self.fd:
			self.fd.close()
			self.fd = None
		self.done = 0
		self.connected = 0
		self.requested = 0
		self.headed = 0


	def close(self):
		self.reset()

