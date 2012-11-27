#!/opt/rocks/bin/python
#
# The 411 python module that contains the essential functionality
# for the 411 Secure Information Service. 
#
# Retrieves encrypted files via HTTP.
#
# This module is primarily used by 411 client programs. Files
# are encoded by '411put'.
#
# Assumes the master servers are running Apache.
#
# Original author: Federico Sacerdoti, fds@sdsc.edu (2003)
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
# $Log: service411.py,v $
# Revision 1.15  2012/11/27 00:48:01  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.14  2012/05/06 05:48:16  phil
# Copyright Storm for Mamba
#
# Revision 1.13  2011/07/23 02:30:22  phil
# Viper Copyright
#
# Revision 1.12  2011/04/26 03:30:26  anoop
# Support for pre-send filtering of content,
# and post receive actions.
# Minor cleanup in the way temp files are created.
#
# Revision 1.11  2011/04/21 21:29:05  anoop
# Bug fix
#
# Revision 1.10  2011/04/14 23:10:59  anoop
# 411 client can now download from a privileged source port
# 411get parses the 411 configuration to get information about
# the node that it's running on. This info is converted to attributes
# and sent to the filter plugins, so that they may filter content
# based on node attributes
#
# Revision 1.9  2010/09/07 23:52:48  bruno
# star power for gb
#
# Revision 1.8  2009/05/01 19:06:49  mjk
# chimi con queso
#
# Revision 1.7  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.6  2008/08/12 23:20:13  anoop
# Added filter for auto.master
#
# Modified 411 transport to encode content of the file
# and filter before encrypting them. This helps with the
# problem of stripping whitespaces, and returns the content
# of the files exactly as they should be.
#
# Also modified the password and group filters just a little
# to make them return the correct whitespaces
#
# Revision 1.5  2008/08/09 19:27:51  anoop
# beginning of actual usable 411 plugins. For now password and group file
# plugins
#
# Revision 1.4  2008/07/17 01:35:29  anoop
# Some pruning.
# Removed the present() function as it doesn't have any purpose,
# anymore
#
# Revision 1.3  2008/07/17 01:27:21  anoop
# Major changes to the 411 system
# - 411 now uses XML as transport
# - Has support for plugins, which work like "Active Messages"
#   Basically, the plugins are nothing more than python code
#   which reside on the frontend in /opt/rocks/var/plugin/411/
#   which act as filters for the files that we are trying to
#   send over the wire. The new system will encode the plugin
#   along with the content of the file, and send it over the
#   wire, so that the plugin can be used to filter the content
#   on the client side
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
# Revision 1.9  2007/04/24 01:23:10  phil
# When writing a file, write to a temp in the same directory with
# identical permissions, then move to dest.
#
# Revision 1.8  2006/09/11 22:48:48  mjk
# monkey face copyright
#
# Revision 1.7  2006/08/10 00:10:53  mjk
# 4.2 copyright
#
# Revision 1.6  2006/01/16 06:49:10  mjk
# fix python path for source built foundation python
#
# Revision 1.5  2005/10/12 18:09:42  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:03:19  mjk
# updated copyright
#
# Revision 1.3  2005/08/08 21:25:00  mjk
# foundation
#
# Revision 1.2  2005/05/24 21:22:45  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/01 02:02:40  mjk
# moved from core to base
#
# Revision 1.39  2005/02/12 02:27:53  fds
# 411 second generation: safer, thanks to master-only RSA keypair; all files
# are now signed for integrity. Faster for master, since we run the random
# number generator less (only once per cluster lifetime rather than once per
# encryption).  Keys are kept in /etc/411-security. Amen.
#
# Revision 1.38  2005/01/24 23:37:46  fds
# Using my simplehttp library for transfers in 411. No memory leaks, no more
# forking from threads. TCP retries now greatly simplified in the listener.
#
# Revision 1.37  2004/11/29 20:57:22  fds
# Fix for bug 84. Simplify! Only use the dot-paths to prevent naming collisions
# in 411.d. Use native pathnames to actually write files. Specifically: the 411
# header contains the real path name, not the dot-path translation.
#
# This version of 411 is not compatible with past versions.
#
# Revision 1.36  2004/11/02 00:35:54  fds
# faster for most tasks.
#
# Revision 1.35  2004/09/07 21:46:00  fds
# 80-col code. 411 group operation more correct.
#
# Revision 1.34  2004/07/21 07:36:54  fds
# Can now handle spaces in URL. 80 col.
#
# Revision 1.33  2004/07/21 00:50:27  fds
# 411get listing now respects groups. Moved group processing into
# base class.
#
# Revision 1.32  2004/07/20 19:47:18  fds
# 411 group support. Also cleaned out some depricated options.
#
# Revision 1.31  2004/06/03 17:36:31  fds
# Support for signed messages, and allow different message headers.
#
# Revision 1.30  2004/04/13 20:09:31  fds
# Can set polling interval in config file.
#
# Revision 1.29  2004/03/25 03:15:13  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.28  2003/11/06 22:22:44  fds
# Fixed an error reporting bug.
#
# Revision 1.27  2003/10/21 20:46:47  fds
# Updated copyright
#
# Revision 1.26  2003/10/20 21:30:57  fds
# Small changes
#
# Revision 1.25  2003/10/20 19:31:39  fds
# Respect to master scores, better doc formatting.
# Turned off debug mode for all modules.
#
# Revision 1.24  2003/10/19 20:39:02  fds
# New master score parameter weights 411 servers based on how 
# well they respond.
#
# Revision 1.23  2003/09/24 01:29:24  fds
# Updated Exception
#
# Revision 1.22  2003/09/12 21:43:43  fds
# Cleaning up a bit
#
# Revision 1.21  2003/09/09 01:44:42  fds
# Using Master helper class. Started
# structure for complex 411 service.
#
# Revision 1.20  2003/09/08 05:17:53  fds
# On our way to using URLs
#
# Revision 1.18  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.17  2003/08/13 17:26:11  fds
# Better text handling for strange 411 msgs.
#
# Revision 1.16  2003/08/08 20:49:04  fds
# Better dir parsing, and better msg format.
#
# Revision 1.15  2003/08/01 22:46:58  fds
# Removed dependancy on pycrypto package (using sha hash directly)
#
# Revision 1.14  2003/07/25 19:48:33  fds
# Can publish multiple files, tighter headers.
#
# Revision 1.13  2003/07/23 18:47:55  fds
# Added 'disable' option to the config file.
#
# Revision 1.12  2003/07/22 22:19:45  fds
# Getting ready for packaging.
#
# Revision 1.11  2003/07/22 04:02:25  fds
# Does not rely on the presence of a config file.
#
# Revision 1.10  2003/07/21 23:48:04  fds
# Can handle bad conf files, and does more CVS-like keyword expansion.
#
# Revision 1.9  2003/07/16 21:28:56  fds
# Sign, verify deal with base64 signatures now, header format improved.
#
# Revision 1.8  2003/07/16 06:19:48  fds
# Moved sign and verify tasks to service411. Allowed for multiple master
# servers in listeners, even dynamically discovered ones (as long as they
# are identified and put into self.masters). Master servers identified by
# IP address.
#
# Revision 1.7  2003/07/15 23:48:57  fds
# New 411 alert design.
#
# Revision 1.6  2003/07/15 21:31:07  fds
# Moved encrypt() into service411, more concious of Python's
# httplib memory leaks.
#
# Revision 1.5  2003/07/13 23:32:24  fds
# Less suceptible to a man-in-the-middle-attack. File name,
# owner, and mode are now encrypted along with the contents in HTTP-style headers.
# Naming them only in the HTTP filename was unsafe.
#
# Revision 1.4  2003/07/11 19:04:41  fds
# Handles directories, and transmits file meta data.
#
# Revision 1.3  2003/07/10 00:31:28  fds
# Made Blowfish encryption safer by using distinct sessionkey and initial values
#
# Revision 1.2  2003/07/07 23:56:06  fds
# First design at 411 publisher.
#
#

import os
import sys
import shutil
import rocks.app
import re
import time
import string
import platform
import cStringIO
import tempfile
import types
# Python OpenSSL Wrappers, available at http://sourceforge.net/projects/pow
import POW
# A cryptography-grade random number generator taken from PyCrypt 1.96a6.
# Available at: http://www.amk.ca/python/code/crypto.html
from rocks.randpool import RandomPool
import rocks.util
from rocks.util import mkdir
import base64
import xml.sax
import xml.dom.NodeFilter
import xml.dom.ext.reader.Sax2
import stat
import random
import urllib
import urlparse
import cgi
# No memory leaks in this version, unlike the standard httplib.
from rocks.simplehttp import HTTPConnection


class Error411(Exception):
  pass


class Service411:
	"""Can retrieve a 411 file from a set of master servers.  Has the
	ability to encrypt, and decrypt files using a hybrid RSA-Symmetric
	cryptographic technique. Only as safe as your sysadmin."""

	def __init__(self):
		self.priv_filename = '/etc/411-security/master.key'
		self.pub_filename = '/etc/411-security/master.pub'
		self.shared_filename = '/etc/411-security/shared.key'
		
		self.masters = []
		# Our current favorite
		self.master = None
		self.disable = 0
		self.verbose = 0
		# The directory from which we place our 411 files. Used
		# when translating 411 file paths.
		self.rootdir="/"
		self.sym = None
		self.pool = None
		# Master keys
		self.priv = None
		self.pub = None
		# Shared key, 256bit + 64bit IV
		self.shared = None
		
		self.conn = None
		# Default URL base path to find files.
		self.urldir = '411.d'
		# Groups we are interested in
		self.groups = ['']

		# Store attributes which we can use to filter on.
		self.attrs = {}

		self.config = Conf(self)
		self.config.parse()

		self.plugin = None

		# A regex for our header search.
		pattern = "\n*(?P<comment>.*?)\$411id\$"
		self.header_pattern = re.compile(pattern)

		pattern = "<a href=.+>(?P<filename>.+)</a> +(?P<date>\d+.*) +(?P<size>\d+.*)"
		# Make the pattern matching engine case-insensitive.
		self.dir_pattern = re.compile(pattern, re.I)

		# Use Blowfish with fast Cipher Block Chaining.
		self.sym = POW.Symmetric(POW.BF_CBC)

	def fillPool(self):
		"""Starts the random pool. Dont do in constructor since this
		is computationally intensive."""

		# A cryptographically safe source of random data.
		self.pool = RandomPool(384)


	def setConf(self, conf):
		self.config = conf(self)


	def setConfHandler(self, handler):
		self.config.setHandler(handler)
		self.config.parse()


	def four11Path(self, filename411):
		"""Translates 411 file names into UNIX absolute filenames."""

		# Warning this is UNIX dependant
		n = string.replace(filename411, ".", "/")
		n = string.replace(n, "//", ".")
		return os.path.normpath(os.path.join(self.rootdir, n))


	def path411(self, filename):
		"""Turns an absolute UNIX path into a 411 filename. Every
		period ('.') is a filesystem delimeter (like /), and all
		filenames are assumed to be absolute, to start with a /. A
		literal period is coded as a double period ('..'). """

		# Warning, this is UNIX dependant.
		n = string.replace(filename[1:], ".", "..")
		n = string.replace(n, "/", ".")
		return n


	def connect(self, master=None):
		"""Opens a HTTP 1.1 connection to the first live master server.
		Will use the master argument if specified, otherwise consults
		internal master server list.  This connection can service
		multiple requests."""

		if self.conn:
			self.disconnect()

		if master:
			masters = [master]
		else:
			masters = self.getMasters()
			if not masters:
				raise ValueError, \
				"We have no master servers to connect to."

		conn = None
		for master in masters:
			# Split address into host & port
			m = master.getAddress().split(':')
			if len(m) == 2:
				conn = HTTPConnection(m[0], int(m[1]))
			else:
				conn = HTTPConnection(m[0]) 

			# Test the connection.
			try:
				# Set variable so that connection originates
				# from privileged port only. This way, only
				# root can initialize this connection
				conn.privileged_port = True
				conn.connect()
			except:
				# If we cannot connect, devalue this server.
				master.decScore()
				conn = None
				continue
			else:
				# We pick the first master that accepts a
				# connection.
				self.master = master
				master.incScore()
				break

		if conn:
			self.conn = conn
		else:
			raise Error411, \
				"Could not reach a master server. Masters: %s" \
				% masters


	def disconnect(self):
		"""Closes the master HTTP connection. """

		if self.conn:
			self.conn.close()
		self.conn = None


	def get(self, file):
		""" Retrives a 411 file. If arg is empty, a directory listing
		dictionary is returned. If file is valid, returns the decrypted
		contents and its associated meta data.  """

		if not file:
			raise Error411, "I need a file to get"

		# Allow you to get a full URL.
		if file.count("http://"):
			m = Master(file)
			self.connect(m)
			file = os.path.basename(file)
		else:
			# We use our internal configuration.
			self.connect()

		path = self.master.getDir() + file
		self.conn.request('GET', urllib.quote(path))
		headers = self.conn.getresponse()
		status = headers['status']
		reason = headers['reason']

		if status != 200:
			raise Error411, "Could not get file '%s%s': %s %s" % \
				(self.master.getUrl(), file, status, reason)

		contents = self.conn.read()
		self.disconnect()

		if file[-1] == '/':		# A directory
			return contents
		else:
			return self.decrypt(contents)


	def find(self, path="/"):
		"""Finds all relevant files to retrieve on a master server.
		Returns dict indexed by file path containing mtime and size."""

		self.files = {}
		self.findHelper(path)
		return self.files


	def findHelper(self, path, depth=0):

		listing = self.get(path)
		lines = listing.split("\n")
		for line in lines:
			m = self.dir_pattern.search(line)
			if not m:
				continue
			#print line
			filename = m.group('filename')
			if filename == "Parent Directory":
				continue
			if filename[-1] == '/':
				if self.verbose:
					print "Found directory %s (%s)" \
						% (path+filename, depth)
				if self.isInteresting(path+filename, depth):
					self.findHelper(path+filename, depth+1)
				continue
			date = m.group('date').strip()
			size = m.group('size').strip()
			self.files[path + filename] = {"Name": filename,
				"Modified": date, "Size" : size}


	def isInteresting(self, path, level):
		"""Matches an offered group our registered groups. Slow,
		search time is squared with the number of registered groups.
		"""

		offered = path[1:-1].split('/')
		elements = len(offered)
		for r in self.groups:
			if not r:
				continue
			if self.verbose:
				print "Matching %s to %s level %s" \
					% (offered, r[:len(offered)], level)
			try:
				# Shorten the registered group to match
				# the offerred one, then compare. Allows
				# group inheritance.
				if offered == r[:len(offered)]:
					return 1
			except:
				continue
		return 0


	def readKeys(self):
		"""Loads the 411 shared and master RSA keys"""


		pub_file = open(self.pub_filename, 'r')
		self.pub = POW.pemRead(POW.RSA_PUBLIC_KEY, pub_file.read())
		pub_file.close()
		
		shared_file = open(self.shared_filename, 'r')
		self.shared = self.readSharedKey(shared_file.read())
		shared_file.close()

		if os.path.exists(self.priv_filename):
			priv_file = open(self.priv_filename, 'r')
			self.priv = POW.pemRead(POW.RSA_PRIVATE_KEY, priv_file.read())
			priv_file.close()


	def makeSharedKey(self):
		"""Uses our cryptographically safe random number generator to 
		give us a 256bit session key and 64bit Init Vector, in 411 format."""
		
		if not self.pool:
			self.fillPool()

		while 1:
			self.pool.stir()
			randomkey = self.pool.get_bytes(40)
			# First 256 bits are for the session key
			sessionkey = randomkey[:32]
			# Last 64 bits are for the CBC initial value.
			initialvalue = randomkey[-8:]
			try:
				self.sym.encryptInit(sessionkey, initialvalue)
			except TypeError:
				# Need a new session key (null chars in our key)
				continue
			else:
				break

		key = "-----BEGIN 411 SHARED KEY-----\n"
		key += base64.encodestring(randomkey)
		key += "-----END 411 SHARED KEY-----\n"
		return key
		
	
	def readSharedKey(self, key64):
		"""Read a 411 shared key in base64 encoding and return the
		binary bits"""

		header = "-----BEGIN 411 SHARED KEY-----\n"
		footer = "-----END 411 SHARED KEY-----\n"
		try:
			a = key64.index(header) + len(header)
			b = key64.index(footer)
			key = base64.decodestring(key64[a:b])
		except:
			raise Error411, \
				"This does not appear to be a 411 shared key."
		return key


	def encrypt(self, plaintext,
			header = "-----BEGIN 411 MESSAGE-----\n",
			footer = "-----END 411 MESSAGE-----\n",
			sign = 1):
		"""Encrypts the plain text message using a hybrid cryptography
		technique: a 256-bit random session key is encrypted with the
		cluster shared key. The session key is used to quickly encrypt
		the message with the Blowfish symmetrical algorithm."""

		if not self.shared:
			self.readKeys()

		# First 256 bits are for the session key,
		# Last 64 bits are for the CBC initial value.
		try:
			self.sym.encryptInit(self.shared[:32], self.shared[-8:])
		except TypeError:
			raise Error411, "Invalid Shared Key"

		# Sign the text with the master private key
		if sign:
			if not self.priv:
				raise Error411, "I need the master private key to sign messages"
			sig = self.sign(plaintext)
		else:
			sig = "Not Signed"

		# Encrypt the text with Blowfish for speed.
		ciphertext = self.sym.update(plaintext) + self.sym.final()
		ciphertext_base64 = base64.encodestring(ciphertext)

		# Message format (v2.0):
		# digital signature
		# <blank line>
		# symmetrically-encrypted message
		msg = header
		msg += sig + "\n"
		msg += ciphertext_base64
		msg += footer
		return msg


	def decrypt(self, contents,
			header = "-----BEGIN 411 MESSAGE-----\n", 
			footer = "-----END 411 MESSAGE-----\n",
			type411 = 1):
		"""Uses the shared key to read 411 messages. For 411
		type messages, returns the tuple (contents, meta) where meta is
		a dictionary containing the 411 headers. If not type 411,
		returns a (plaintext, sig_base64). No verification of signature
		is performed."""

		if not self.sym:
			self.fillPool()
			
		ciphersig_base64 = ''
		try:
			a = string.index(contents, header) + len(header)
			b = string.index(contents, footer)
			msg = contents[a:b]

			ciphersig_base64, ciphertext_base64 = msg.split('\n\n')
			ciphertext = base64.decodestring(ciphertext_base64)
		except:
			raise Error411, \
				"This file does not appear to be in 411 format."

		if not self.shared:
			self.readKeys()

		sessionkey = self.shared[:32]
		initialvalue = self.shared[-8:]

		self.sym.decryptInit(sessionkey, initialvalue)
		try:
			text = self.sym.update(ciphertext) + self.sym.final()
		except POW.SSLError:
			raise Error411, "Could not decrypt file, wrong key?"

		if type411:
			if not self.verify(text, ciphersig_base64):
				raise Error411, "Signature does not verify."
			return self.decode(text)
		else:
			return (text, ciphersig_base64)

	def decode(self, plaintext):
		meta = {}
		p = Parser(plaintext, self.attrs)
		meta = p.get_filtered_content()
		self.plugin = p.get_plugin()
		return meta['content'], meta
		
		
	def verify(self, msg, sig_base64):
		"""Verifies that the plaintext message was signed with the
		(base64 encoded) signature, and has not been altered since
		signing. Returns true if message verifies."""

		if not self.pub: self.readKeys()

		digest = POW.Digest(POW.MD5_DIGEST)
		digest.update(msg)

		try:
			sig = base64.decodestring(sig_base64)
		except:
			return 0

		return self.pub.verify(sig, digest.digest(), POW.MD5_DIGEST)


	def sign(self, plaintext):
		"""Sign the message with our private key. Returns the 
		base64 encoded signature."""

		if not self.priv: self.readKeys()

		digest = POW.Digest(POW.MD5_DIGEST)
		digest.update(plaintext)

		return base64.encodestring(
			self.priv.sign(digest.digest(), POW.MD5_DIGEST))


	def write(self, contents, meta, httpmeta=None):
		"""Writes a 411 file with the given plaintext contents, and
		meta information to the local filesystem. Respects the master
		file's owner, group, and permission bits. Contents and meta 
		arguments are in the format from get()."""

		try:
			# Get standard 411 headers - safe because they were
			# encrypted.
			filename = meta["name"]
			owner = meta["owner"]
			uid, gid = map(int, owner.split("."))
			mode_oct = meta["mode"]
		except ValueError:
			raise Error411, "File has malformed 411 headers."

		try:
			# This possibly could be done with an OO file class,
			# but not worth it if we only have two choices.
			mode = int(mode_oct, 8)
			if stat.S_ISDIR(mode):
				mkdir(filename)
			elif stat.S_ISREG(mode):
				path, name = os.path.split(filename)
				mkdir(path)
				(f, tmp_filename) = tempfile.mkstemp()
				os.write(f, contents)
				os.close(f)
				os.chown(tmp_filename, uid, gid)
				os.chmod(tmp_filename, stat.S_IMODE(mode))
				# mv temp file
				shutil.move(tmp_filename, filename)
				
			else:
				raise Error411, \
					"File %s is an unknown type" % filename
			# Set file meta data
			os.chown(filename, uid, gid)
			os.chmod(filename, stat.S_IMODE(mode))

		except (IOError, OSError), msg:
			raise Error411, \
				"Could not write %s: %s" % (filename, msg)
				
	def addMaster(self, arg):
		"""Adds a new master to the appropriate place in the
		self.masters structure. Can take either a URL or a master
		instance."""

		if isinstance(arg, Master):
			master = arg
		else:
			master = Master(arg)
		self.masters.append(master)


	def getMasters(self):
		"""Returns the list of master servers sorted by current score.
		Called every time we connect()."""

		self.masters.sort(byScore)
		return self.masters

class Plugin:
	def __init__(self, attrs = {}):
		self.attrs = attrs
		pass
	
class NodeFilter(xml.dom.NodeFilter.NodeFilter):
	def acceptNode(self, node):
		if node.nodeName == "service411":
			return self.FILTER_ACCEPT

		if node.nodeName in [
			'name',
			'mode',
			'owner',
			'content',
			'filter',
			]:
			return self.FILTER_ACCEPT
		else:
			return self.FILTER_SKIP

class Parser:
	"""
	This class acts as the parser for the 411 xml file.
	"""
	def __init__(self, content, attrs):
		
		# Dictionary of the Entire 411 file. This contains
		# everything, name, content, filter, mode, blah,
		# and any other XML tag that's made up
		self.dict411 = {}

		# Dictionary of attributes which are passed to
		# the filter, and can be used by the filter
		# to determine code paths.
		self.attrs = attrs

		self.plugin = None

		# Contains the output of the filtering process.
		self.filtered = {}
		
		# The 411 XML file
		self.xml_string = content

		# Parse the 411 file to populate the self.dict411
		# dictionary
		self.parse()

		# Apply the filter to the dictionary and populate
		# the self.filtered dictionary
		self.apply_filter()

	def parse(self):
		"""
		Function to parse the 411 XML file
		"""
		# Convert the XML string to an IO Buffer
		xml_buf = cStringIO.StringIO(self.xml_string.strip())
		doc = xml.dom.ext.reader.Sax2.FromXmlStream(xml_buf)
		filter = NodeFilter()
		iter = doc.createTreeWalker(doc, filter.SHOW_ELEMENT,
			filter, 0)
		node = iter.nextNode()
		while node:
			if node.nodeName == 'service411':
				child = iter.firstChild()
				while child:
					self.dict411[child.nodeName] = self.get_text(child)
					child = iter.nextSibling()
			node = iter.nextNode()


	def apply_filter(self):
		"""
		Function to filter the 411 content. The way this
		works is. The XML file contains the contents of
		the file, and a filter. The file contents are passed
		through the filter to obtain new content. This new
		content is then fed back up to the requesting process
		"""

		# If there's no filter, set content to
		# the original content, and return
		if not self.dict411.has_key('filter') \
			or not self.dict411['filter']:
			for i in self.dict411:
				self.filtered[i] = self.dict411[i]
			return

		# If not, then create a temporary directory
		# for the filter script. The filter script
		# always has to be a python script with 
		# a class called Plugin, whose superclass
		# and description are present in this file
		# below.
		dir = tempfile.mkdtemp()

		# Once the temp directory is created, copy
		# the contents of the filter into __init__.py
		# script.
		f = open('%s/__init__.py' % dir, 'w')
		f.write(self.dict411['filter'])
		f.close()
		
		# Import the module, and pass the original
		# content to the filter function in th Plugin class.
		base_dir = os.path.dirname(dir)
		mod_name = os.path.basename(dir)
		sys.path.append(base_dir)
		m = __import__(mod_name)
		self.plugin = m.Plugin(self.attrs)

		# Filter the original content, and set
		# the new content.
		for i in self.dict411:
			try:
				self.filtered[i] = eval('self.plugin.filter_%s(self.dict411[i])' % i)
			except AttributeError:
				self.filtered[i] = self.dict411[i]

		# Remove the plugin, and the temporary
		# directory
		os.unlink('%s/__init__.py' % dir)
		os.unlink('%s/__init__.pyc' % dir)
		os.rmdir(dir)
		

	def get_plugin(self):
		return self.plugin

	def get_text(self, node):
		# This function returns the base64 unencoded
		# text present inside an xml tag.
		text = ''
		for child in node.childNodes:
			if child.nodeType == child.TEXT_NODE or \
			   child.nodeType == child.CDATA_SECTION_NODE:
				text += child.nodeValue
		text = text.strip()
		if node.nodeName == 'content' or node.nodeName == 'filter':
			return base64.b64decode(text)	
		return text

	def get_filtered_content(self):
		return self.filtered

def byScore(a, b):
	"""A comparison function that will sort masters by score
	such that the highest score is first in list."""
	return cmp(b.getScore(), a.getScore())




class Master:
	"""A Master server in the 411 system. Each server has a score made by
	a saturating counter that allows dead masters to be ignored in a long
	running cluster."""

	def __init__(self, url, score=0):
		self.address = ''
		self.urldir = ''
		self.type = ''
		self.extends = ''
		self.score = score
		self.saturated = 3
		self.parseURL(url)


	def __repr__(self):
		return "%s (%s)" % (self.getUrl(), self.getScore())


	def parseURL(self, url):
		"""Splits a URL for http into three components: the server's
		address, the path, and the filename.  CGI vars are parsed as
		well."""

		if not url:
			return

		# Returns (addressing scheme, network location, path, 
		# query, fragment identifier).
		u = urlparse.urlsplit(url)
		
		if u[0] != "http":
			raise Error411, "Master URL is not well formed."
			
		self.address = u[1]

		# Requires that the  411 url directory end with a '/'.
		# Not acceptable: http://1.2.3.4/411.d
		# Ok: http://1.2.3.4/411.d/
		# Ok: http://1.2.3.4/411.d/etc.passwd
		self.urldir = os.path.dirname(u[2]) + "/"

		if u[3]:
			# Turn cgi vars into a dictionary.
			self.vars = cgi.parse_qs(u[3])

		# Reform url without a filename.
		self.url = urlparse.urlunsplit(
			(u[0], u[1], self.urldir, u[3], u[4]))


	def getAddress(self):
		return self.address

	def getDir(self):
		return self.urldir

	def getUrl(self):
		return self.url

	def getType(self):
		# Constrains the attribute to lower case. Perhaps bad.
		if "type" in self.vars:
			return self.vars["type"]
		else:
			return None

	def getScore(self):
		return self.score

	def setScore(self):
		self.score = score

	def incScore(self):
                """Increases the score of this server by one. A saturating
                addition."""
		self.score = self.score + 1
		if self.score > self.saturated:
			self.score = self.saturated

	def decScore(self):
		"""Decrements this servers score, saturating as well."""
		self.score = self.score - 1
		if self.score < -self.saturated:
			self.score = -self.saturated



class Conf:
	"""Updates the 411 service configuration file. Randomizes the
	order of the (same score) master servers to achieve a measure
	of load balancing in a large cluster. The old file is
	overwritten."""

	def __init__(self, app):
		self.file = None
		self.app = app
		self.conf = '/etc/411.conf'
		self.handler = ConfHandler
		self.parser = xml.sax.make_parser()

	def setFile(self, conf):
		self.conf = conf

	def getFile(self):
		return self.conf

	def setHandler(self, handler):
		self.handler = handler

	def write(self):
		self.header()
		self.body()
		self.footer()


	def header(self):
		if self.file:
			return
		
		now = time.strftime("%d-%b-%Y %H:%M")
		
		f = open(self.conf, 'w')
		f.write(
		'<!-- Configuration file for the 411 Information Service -->\n')
		f.write(
		'<!-- Written %s by the 411 service. Do not edit. -->\n' % now)
		f.write('<config>\n')

		self.file = f
		return


	def body(self):
		if not self.file:
			return
			
		f = self.file

		# Make a copy of our list of master servers before we shuffle
		# them.
		masters = self.app.masters[:]
		random.shuffle(masters)
		for m in masters:
			f.write(' <master url="%s" score="%s"/>\n' \
				% (m.getUrl(), m.getScore()))

		for g in self.groups:
			f.write(' <group>%s</group>\n' %
				string.join(g, '/'))

		f.write(' <urldir>%s</urldir>\n' % self.app.urldir)


	def footer(self):
		if not self.file:
			return

		self.file.write('</config>\n')
		self.file.close()

		self.file = None
		print "Updated config file"


	def parse(self):
		"""Parses the 411 XML configuration file. We ignore empty or
		malformed XML. Overwrites existing master list."""
		try:
			conffile = open(self.conf, 'r')
		except IOError, msg:
			# It is not an error to miss the conf file.
			return

		self.app.masters = []
		handler = self.handler(self.app)
		self.parser.setContentHandler(handler)
		try:
			self.parser.parse(conffile)
		except:
			pass
		conffile.close()



class ConfHandler(rocks.util.ParseXML):

	def __init__(self, app):
		rocks.util.ParseXML.__init__(self, app)
		self.app = app

	def startElement(self, name, attrs):
		try:
			f = getattr(self, "startElement_%s" % name)
			f(name, attrs)
		except AttributeError:
			self.app.attrs[name] = ''
			self.text = ''
			return

	def endElement(self, name):
		try:
			f = getattr(self, "endElement_%s" % name)
			f(name)
		except AttributeError:
			self.app.attrs[name] = string.strip(self.text)
			return
		
	def startElement_config(self, name, attrs):
		return

	def endElement_config(self, name):
		return

	def startElement_master(self, name, attrs):
		url = attrs.get('url', None)
		score = attrs.get('score', 0)
		m = Master(url, int(score))
		self.app.addMaster(m)

	def endElement_master(self, name):
		return

	def startElement_disable(self, name, attrs):
		self.app.disable = 1

	def endElement_disable(self, name):
		return

	def startElement_urldir(self, name, attrs):
		self.text = ''
		
	def endElement_urldir(self, name):
		self.app.urldir = os.path.normpath(self.text)
		self.text = ''

	def startElement_group(self, name, attrs):
		self.text = ''

	def endElement_group(self, name):
		"A group name has no leading or trailing slashes"

		g = os.path.normpath(self.text)
		while g[0] == '/':
			g = g[1:]
		self.app.groups.append(g.split('/'))
		self.text = ''
