#! /opt/rocks/bin/python
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

import os
import pwd
import sys
import string
import getopt
import types
import subprocess

from sqlalchemy import create_engine
import sqlalchemy
import mappings.base
import rocks.db.mappings.base

from rocks.db.mappings.base import *




class Database():

	def __init__(self, argv=None):
		pass

	def getPasswd(self):
		filename = None
		username = self.getUsername()
		if username == 'root':
			filename = '/root/.rocks.my.cnf'
		if username == 'apache':
			filename = '/opt/rocks/etc/my.cnf'
		try:
			if filename is not None:
				file = open(filename, 'r')
				for line in file.readlines():
					l=line.split('=')
					if len(l) > 1 and l[0].strip() == "password" :
						rval=l[1].strip()
						break
				file.close()
		except:
			pass
		return rval 


	def getUsername(self):
		return pwd.getpwuid(os.geteuid())[0].strip()

	def getHostname(self):
		try:
		        host = rocks.DatabaseHost
		except:
		        host = 'localhost'
		return host


	def connect(self):
		engine = create_engine('mysql://' + self.getUsername() + 
			':' + self.getPasswd() + '@' + self.getHostname() + 
			'/cluster', echo=True)
		self.conn = engine.connect()
		self.Session = sqlalchemy.orm.sessionmaker(bind=engine)
		session = self.Session()

		#for node in session.query(Node).filter(Node.Name=='compute-0-0-0'):
		#	print "Node ", node
		#	for interface in node.Networks:
		#		print " > ", interface
		#for node in session.query(Node).join(Network).filter(Node.Name=='compute-0-0-0').filter(Network.Device=='eth0'):
		#	print "node ", node
		#for network in session.query(Network).join(Node).filter(Node.Name=='compute-0-0-0').filter(Network.Device=='eth0'):
		#	print "netowrk ", network
		#	#print network

		#node = session.query(Node).filter(Node.Name=='compute-0-0-0').first()
		#new_interface = Network(Device="eth15", MAC="00:13:ff:3e:2a:1d", Name="test-interface")
		#print "adding an interface ", new_interface, " to ", node
		#node.Networks.append(new_interface)
		#session.add(new_interface)
		#interface = session.query(Network).join(Node).filter(Node.Name=='compute-0-0-0').filter(Network.Device=='eth15').first()
		#print "interface ", interface
		#interface.Name = "eth7"
		# not necessary but if you want to force it
		#session.commit()

		#to run pure query
		results = session.query().from_statement('select * from Networks')



		
		

	def execute(self, command):
	    if hasSQL:
	        return self.cursor.execute(command)
	    return None
	
	def fetchone(self):
	    if hasSQL:
	        return self.cursor.fetchone()
	    return None
	
	def fetchall(self):
	    if hasSQL:
	        return self.cursor.fetchall()
	    return None
	
	def insertId(self):
	    "Returns the last inserted id. Useful for auto_incremented columns"
	    id = None
	    if hasSQL:
	        id = self.cursor.lastrowid
	    return id
	
	def close(self):
	    if hasSQL:
	        if self.link:
	           return self.link.close()
	    return None
	
	def __repr__(self):
	    return string.join(self.report, '\n')
	
	def getGlobalVar(self, service, component, node=0):
		cmd = '/opt/rocks/bin/rocks report host attr localhost '
		cmd += 'attr=%s_%s' % (service, component)
		
		p = subprocess.Popen(cmd, shell=True, 
		        stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
		w, r =  (p.stdin, p.stdout)
		value = r.readline()
		
		return value.strip()
	
	    
	def getNodeId(self, host):
		"""Lookup hostname in nodes table. Host may be a name
		or an IP address. Returns None if not found."""
		
		# Is host already an ID?
		
		try:
			return int(host)
		except Exception:
			pass
		
		# Try by name
		
		self.execute("""select networks.node from nodes,networks where
			networks.node = nodes.id and networks.name = "%s" and
			(networks.device is NULL or
			networks.device not like 'vlan%%') """ % (host))
		try:
			nodeid, = self.fetchone()
			return nodeid
		except TypeError:
			nodeid = None
		
		# Try by IP
		
		self.execute("""select networks.node from nodes,networks where
			networks.node = nodes.id and networks.ip ="%s" and
			(networks.device is NULL or
			networks.device not like 'vlan%%') """ % (host))
		try:
			nodeid, = self.fetchone()
			return nodeid
		except TypeError:
			nodeid = None
		
		return nodeid





if __name__ == "__main__":
	d = Database()
	d.connect()


