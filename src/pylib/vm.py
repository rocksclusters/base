#!/opt/rocks/bin/python
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
# $Log: vm.py,v $
# Revision 1.22  2012/11/27 00:48:40  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.21  2012/05/06 05:48:47  phil
# Copyright Storm for Mamba
#
# Revision 1.20  2012/02/29 18:33:47  clem
# Support both python2.4 and python2.6
#
# Revision 1.19  2012/02/15 22:33:31  clem
# moved from import sha to import hashlib
#
# Revision 1.18  2011/07/23 02:30:49  phil
# Viper Copyright
#
# Revision 1.17  2010/09/07 23:53:08  bruno
# star power for gb
#
# Revision 1.16  2010/08/05 22:21:51  bruno
# optionally get the status of the VMs
#
# Revision 1.15  2010/07/12 17:44:57  bruno
# move private key reading out to the commands.
#
# support for the 'power on and install' command.
#
# Revision 1.14  2010/06/30 18:01:12  bruno
# can now route error messages back to the terminal that issued the command.
#
# Revision 1.13  2010/06/29 00:25:14  bruno
# a little code restructuring and now the console can handle reboots
#
# Revision 1.12  2010/06/28 17:42:48  bruno
# list macs command
#
# Revision 1.11  2010/06/24 23:43:22  bruno
# don't allow vncviewer to auto select its settings. just go full on.
#
# Revision 1.10  2010/06/23 22:23:30  bruno
# tweak
#
# Revision 1.9  2010/06/22 21:42:36  bruno
# power control and console access for VMs
#
# Revision 1.8  2009/05/01 19:07:08  mjk
# chimi con queso
#
# Revision 1.7  2008/10/18 00:56:02  mjk
# copyright 5.1
#
# Revision 1.6  2008/08/22 23:26:38  bruno
# closer
#
# Revision 1.5  2008/04/16 19:11:31  bruno
# only get partition info for partitions that are mountable (i.e., they
# have a leading '/' in the mountpoint field).
#
# Revision 1.4  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.3  2008/02/12 00:15:39  bruno
# partition sizes can be reported as floats
#
# Revision 1.2  2008/02/07 20:10:32  bruno
# added some global functions for VM management
#
# Revision 1.1  2008/01/31 20:05:32  bruno
# needed a helper function for the VM configuration rocks command line
#
#

import cStringIO
import os
import re
import struct
import sys
import socket
import ssl
import select
import M2Crypto

class VM:

	def __init__(self, db):
		self.db = db
		return


	def partsizeCompare(self, x, y):
		xsize = x[0]
		ysize = y[0]

		suffixes = [ 'KB', 'MB', 'GB', 'TB', 'PB' ]

		xsuffix = xsize[-2:].upper()
		ysuffix = ysize[-2:].upper()

		try:
			xindex = suffixes.index(xsuffix)
		except:
			xindex = -1

		try:
			yindex = suffixes.index(ysuffix)
		except:
			yindex = -1

		if xindex < yindex:
			return 1
		elif xindex > yindex:
			return -1
		else:
			try:
				xx = float(xsize[:-2])
				yy = float(ysize[:-2])

				if xx < yy:
					return 1
				elif xx > yy:
					return -1
			except:
				pass

		return 0


	def getPartitions(self, host):
		partitions = []

		rows = self.db.execute("""select p.mountpoint, p.partitionsize
			from partitions p, nodes n where p.node = n.id and
			n.name = '%s'""" % (host))

		if rows > 0:
			for (mnt, size) in self.db.fetchall():
				if mnt in [ '', 'swap' ]:
					continue
				if len(mnt) > 0 and mnt[0] != '/':
					continue

				partitions.append((size, mnt))

		return partitions


	def getLargestPartition(self, host):
		#
		# get the mountpoint for the largest partition for a host
		#
		maxmnt = None

		sizelist = self.getPartitions(host)
		if len(sizelist) > 0:
			sizelist.sort(self.partsizeCompare)
			(maxsize, maxmnt) = sizelist[0]

		return maxmnt


	def getPhysHost(self, vm_host):
		#
		# get the physical host that controls this VM host
		#
		host = None

		rows = self.db.execute("""select vn.physnode from vm_nodes vn,
			nodes n where n.name = '%s' and n.id = vn.node"""
			% (vm_host))

		if rows == 1:
			physnodeid, = self.db.fetchone()
			rows = self.db.execute("""select name from nodes where
				id = %s""" % (physnodeid))

			if rows == 1:
				host, = self.db.fetchone()

		return host


	def isVM(self, host):
		#
		# a node is a VM if it is in the vm_nodes table
		#
		try:
			rows = self.db.execute("""select n.name from
				nodes n, vm_nodes vn where
				n.name = '%s' and n.id = vn.node""" % host)
		except:
			rows = 0

		return rows


#code specific to ssh-agent
SSH2_AGENTC_REQUEST_IDENTITIES = 11
SSH2_AGENT_IDENTITIES_ANSWER = 12
SSH2_AGENTC_SIGN_REQUEST = 13
SSH2_AGENT_SIGN_RESPONSE = 14
SSH_AGENT_FAILURE = 5


class VMControl:
	"""this class is used to comunicate with airboss
	It encapsulate most of the method needed"""

	def __init__(self, db, controller, flags=''):
		self.db = db
		self.controller = controller
		self.key = None
		self.agent_key = None
		self.agent_socket = None
		self.port = 8677
		self.flags = flags
		return



	def setKey(self, key):
		"""set the rsa private key value
		return true if successful false if there is a problem"""


		ssh_auth_sock = os.getenv('SSH_AUTH_SOCK')
		if ssh_auth_sock:
			# we have ssh agent let's try to use it
			try:
				self.agent_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
				self.agent_socket.connect(ssh_auth_sock)

				# Get list of public keys, and find our key.
				self.agent_socket.sendall('\0\0\0\1\v') # SSH2_AGENTC_REQUEST_IDENTITIES
				response = RecvStr(self.agent_socket)
				resf = cStringIO.StringIO(response)
				assert RecvAll(resf, 1) == chr(SSH2_AGENT_IDENTITIES_ANSWER)
				num_keys = RecvU32(resf)
				assert num_keys < 2000  # A quick sanity check.

				if num_keys:
					# if there are not keys no point in going on
					# we are going to use either the first one
					# or the matching with slef.key

					list_keys = []
					list_comment = []
					for i in xrange(num_keys):
						list_keys.append(RecvStr(resf))
						list_comment.append(RecvStr(resf))
					if key in list_comment:
						self.agent_key = list_keys[list_comment.index(key)]
						comment = list_comment[list_comment.index(key)]
					else:
						self.agent_key = list_keys[0]
						comment = list_comment[0]
					assert '' == resf.read(1), 'EOF expected in resf'
					assert self.agent_key.startswith('\x00\x00\x00\x07ssh-rsa\x00\x00'),\
						('non-RSA key in ssh-agent (%s) only '
							'dsa is supported' % comment)

					# these are useless but I need to read all the data from the agent
					keyf = cStringIO.StringIO(self.agent_key[11:])
					public_exponent = int(RecvStr(keyf).encode('hex'), 16)
					modulus_str = RecvStr(keyf)
					modulus = int(modulus_str.encode('hex'), 16)
					assert '' == keyf.read(1), 'EOF expected in keyf'

					# we have a matching key in our ssh-agent
					print "Using key: ", comment #, "agent key is: ", self.agent_key
					return True

			except socket.error, e:
				# probably a dead ssh-agent or similar problem
				# do not crash, just report the problem
				print "Error connecting to ssh-agent: ", e

		if not key:
			#
			# let's try to pick a default key
			#
			home_folder = os.getenv("HOME")
			if not home_folder:
				return False

			ssh_folder = os.path.join(home_folder, '.ssh')
			key = os.path.join(ssh_folder, 'id_rsa')

		if not os.path.exists(key):
			return False

		self.key = M2Crypto.RSA.load_key(key)

		return True







	def closeconnection(self, sock, s):
		try:
			s.shutdown(socket.SHUT_RDWR)
		except:
			pass

		try:
			sock.shutdown(socket.SHUT_RDWR)
		except:
			pass

		s.close()
		sock.close()


	def launchconsole(self, sock, s):
		reason = ''

		#
		# setup an endpoint that VNC will use to talk to us
		#
		vnc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		#
		# find a free port
		#
		success = 0
		for i in range(1, 100):
			vncport = 5900 + i
			try:
				vnc.bind(('localhost', vncport))
				success = 1
				break
			except:
				pass

		if not success:
			return 'failed'

		vnc.listen(1)

		pid = os.fork()
		if pid == 0:
			os.system('vncviewer %s localhost:%d' %
				(self.flags, vncport))
			os._exit(0)

		#
		# parent
		#
		conn, addr = vnc.accept()

		done = 0
		while not done:
			#
			# read from the VM controller
			#
			(i, o, e) = select.select([sock.fileno()], [], [],
				0.00001)
			if sock.fileno() in i:
				try:
					(status, output) = self.recvresponse(s)

					if len(output) == 0:
						# 
						# EOF. the VM controller
						# shutdown the connection.
						# let's see if the remote
						# machine rebooted
						# 
						reason = 'retry'
						done = 1
						continue
						
					bytes = conn.send(output)
					while bytes != len(output):
						bytes += conn.send(
							output[bytes:])
				except:
					done = 1
					continue

			#
			# read from the VNC client
			#
			(i, o, e) = select.select([conn.fileno()], [], [],
				0.00001)
			if conn.fileno() in i:
				try:
					input = conn.recv(1024)

					bytes = s.write(input)
					while bytes != len(input):
						bytes += s.write(
							input[bytes:])
				except:
					done = 1
					continue

		try:
			conn.shutdown(socket.SHUT_RDWR)
		except:
			pass
		try:
			conn.close()
		except:
			pass
		try:
			vnc.shutdown(socket.SHUT_RDWR)
		except:
			pass
		try:
			vnc.close()
		except:
			pass

		return reason


	def connect_send_command(self, op, dst_mac, launch_console=False):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s = ssl.wrap_socket(sock)
		s.connect((self.controller, self.port))

		#
		# start the connection by sending a command to the VM
		# controller
		#
		self.sendcommand(s, op, dst_mac)

		#
		# read the status code from the VM controller
		#
		(status, reason) = self.recvresponse(s)

		if status == 0 and launch_console:
			reason = self.launchconsole(sock, s)

		self.closeconnection(sock, s)

		return (status, reason)


	def sendcommand(self, s, op, dst_mac):
		msg = '%s\n' % op

		#
		# destination MAC
		#
		msg += '%s\n' % dst_mac

		#
		# send the size of the clear text and send the clear text
		# message
		#
		msgsize = '%08d\n' % len(msg)
		bytes = 0
		while bytes != len(msgsize):
			bytes = s.write(msgsize[bytes:])

		bytes = 0
		while bytes != len(msg):
			bytes = s.write(msg[bytes:])


		if self.agent_key:

			# we have a ssh-agent let's ask him to make the signature
			# agent will make sha1 digest for us so we send only the message

			# build request message
			request_output = [chr(SSH2_AGENTC_SIGN_REQUEST)]
			AppendStr(request_output, self.agent_key)
			AppendStr(request_output, msg)
			request_output.append(struct.pack('>L', 0))  # flags == 0
			full_request_output = []
			AppendStr(full_request_output, ''.join(request_output))
			full_request_str = ''.join(full_request_output)

			# send it
			self.agent_socket.sendall(full_request_str)

			#
			# parse response
			response = RecvStr(self.agent_socket)
			resf = cStringIO.StringIO(response)
			if RecvAll(resf, 1) != chr(SSH2_AGENT_SIGN_RESPONSE):
				raise RuntimeError("Comunication problem with ssh-agent"
						" (SSH2_AGENT_SIGN_RESPONSE)")
			signature = RecvStr(resf)
			if '' != resf.read(1):
				raise RuntimeError("Comunication problem with "
						"ssh-agent (EOF not present)")
			if not signature.startswith('\0\0\0\7ssh-rsa\0\0'):
				raise RuntimeError("Comunication problem with ssh-agent"
						"(singing algorithm is no ssh-rsa)")
			sigf = cStringIO.StringIO(signature[11:])
			signature = RecvStr(sigf)


		else:
			#
			# no ssh-agent. Let's use m2crytp routine
			#
			try:
				import hashlib
				digest = hashlib.sha1(msg).digest()
			except ImportError:
				#support python2.4 and python2.6
				import sha
				digest = sha.sha(msg).digest()

			signature = self.key.sign(digest)

		#
		# send the length of the signature
		#
		msgsize = '%08d\n' % len(signature)
		bytes = 0
		while bytes != len(msgsize):
			bytes += s.write(msgsize[bytes:])

		bytes = 0
		while bytes != len(signature):
			bytes += s.write(signature)


	def recvresponse(self, s):
		#
		# pick up response
		#
		buf = ''
		while len(buf) != 9:
			buf += s.read(1)

		try:
			msg_len = int(buf)
		except:
			msg_len = 0

		buf = ''
		while len(buf) != msg_len:
			buf += s.read(msg_len - len(buf))

		status = 0

		#
		# check if the message has a status code in it
		#
		a = re.match('^status:[0-9-]+\n', buf)
		if a:
			s = a.group(0).split(':')
			if len(s) > 1:
				try:
					status = int(s[1])
					response = buf[len(a.group(0)):]
				except:
					response = buf
		else:
			response = buf

		return (status, response)


	def cmd(self, op, host):
		#
		# the list of valid commands:
		#
		#	power off
		#	power on
		#	power on + install
		#	list macs
		#	console
		#

		if ':' in host:
			dst_mac = host
		else:
			#
			# if 'host' doesn't look like a MAC address, then try
			# to look up the destination MAC address in the
			# database
			#
			rows = self.db.execute("""select mac from networks where
				node = (select id from nodes where name = '%s')
				and mac is not NULL""" % host)

			if rows > 0:
				dst_mac, = self.db.fetchone()
			else:
				return (-1, 'could not find host "%s"' % host)

		retval = ''

		if op in [ 'power off', 'power on', 'power on + install' ]:
			(status, msg) = self.connect_send_command(op, dst_mac)
		elif op == 'list macs' or op == 'list macs + status':
			(status, msg) = self.connect_send_command(op, dst_mac)
		elif op == 'console':
			msg = 'retry'
			while msg == 'retry':
				(status, msg) = self.console(op, dst_mac)
				if msg == 'retry':
					print ''
					print 'Attempting to reestablish ' + \
						'the console connection. ' + \
						'Standby...'

		return (status, msg)



#
# ssh agent code ispired by
# http://ptspts.blogspot.com/2010/06/how-to-use-ssh-agent-programmatically.html
# http://blog.oddbit.com/2011/05/09/signing-data-with-ssh-agent/
#
def RecvAll(sock, size):
	"""receive a binary stream and convert to string"""
	if size == 0:
		return ''
	assert size >= 0
	if hasattr(sock, 'recv'):
		recv = sock.recv
	else:
		recv = sock.read
	data = recv(size)
	if len(data) >= size:
		return data
	assert data, 'unexpected EOF'
	output = [data]
	size -= len(data)
	while size > 0:
		output.append(recv(size))
		assert output[-1], 'unexpected EOF'
		size -= len(output[-1])
	return ''.join(output)


def RecvU32(sock):
	"""receive a 4 bytes integer"""
	return struct.unpack('>L', RecvAll(sock, 4))[0]


def RecvStr(sock):
	"""receive a string"""
	return RecvAll(sock, RecvU32(sock))


def AppendStr(ary, data):
	"""append a string"""
	assert isinstance(data, str)
	ary.append(struct.pack('>L', len(data)))
	ary.append(data)


