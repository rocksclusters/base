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




class Database(object):
	""" This class should proxy all the connection to the database
	
	Usage Example:
	db = Database()
	db.setVerbose()
	db.connect()
	"""

	def __init__(self):
		# this field are used to change the default behaviour for 
		# connecting to the database
		self._dbUser = None
		self._dbPasswd = None
		self._dbHost = None
		self._dbName = None
		self.verbose = False
		#temporary holds results from self.conn.execute(sql)
		self.results = False
		self.session = None
		self.conn = None
		self.engine = None


	def setDBPasswd(self, passwd):
		self._dbPasswd = passwd

	def getDBPasswd(self):
		if self._dbPasswd:
			return self._dbPasswd
		passwd = ''
		filename = None
		username = self.getDBUsername()
		if username == 'root':
			filename = '/root/.rocks.my.cnf'
		if username == 'apache':
			filename = '/opt/rocks/mysql/my.cnf'
		try:
			if filename is not None:
				file = open(filename, 'r')
				for line in file.readlines():
					l=line.split('=')
					if len(l) > 1 and l[0].strip() == "password" :
						passwd=l[1].strip()
						break
				file.close()
		except:
			pass
		return passwd


	def setDBUsername(self, name):
		self._dbUser = name

	def getDBUsername(self):
		if self._dbUser:
			return self._dbUser
		return pwd.getpwuid(os.geteuid())[0].strip()


	def setDBHostname(self, host):
		self._dbHost = host

	def getDBHostname(self):
		if self._dbHost:
			return self._dbHost
		try:
		        host = rocks.DatabaseHost
		except:
		        host = 'localhost'
		return host

	def setDBName(self, name):
		self._dbName = name

	def getDBName(self):
		if self._dbName:
			return self._dbName
		return 'cluster'


	def setVerbose(self, verbose):
		"""If the verbose is true all the sql will be printed to 
		stdout 

		This function must be called before the connect"""
		self.verbose = verbose


	def connect(self):

		if os.environ.has_key('ROCKSDEBUG'):
			self.setVerbose(True)

		mysql_socket = '/var/opt/rocks/mysql/mysql.sock'

		url = 'mysql+mysqldb://' + self.getDBUsername() + ':' + self.getDBPasswd() \
			 + '@' + self.getDBHostname() + '/' + self.getDBName()
		if os.path.exists(mysql_socket):
			# we can use a unix socket
			url += "?unix_socket=" + mysql_socket

		if self.verbose:
			import logging
			logging.basicConfig()
			logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

		if self.verbose:
			# TODO move this to the logger
			print "Database connection URL: ", url

		self.engine = create_engine(url)

		self.conn = self.engine.connect()
		#results = self.conn.execute("select * from networks")

		#for (ID, Node, MAC, IP, Netmask, Gateway, Name, Device, Subnet, Module, VlanID, Options, Channel) in results:
		#	print ID, Node, MAC, IP, Netmask, Gateway, Name, Device, Subnet
		#self.conn.close()	

		
		# ORM
		#self.Session = sqlalchemy.orm.sessionmaker(bind=engine)
		#session = self.Session()
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
		#results = session.query().from_statement('select * from Networks')

		
	def getSession(self):
		"""return the current session. If it does not exist it creates one.

		the session is a singleton, you can call this method many time it 
		returns always the same object"""
		if self.session:
			return self.session
		elif self.engine:
			Session = sqlalchemy.orm.sessionmaker(bind=self.engine)
			self.session = Session()
			return self.session
		else:
			return None

	def commit(self):
		"""Commit the current session if it exists"""
		if self.session:
			self.session.commit()
		else:
			# no need to manually commit with sqlalchemy if using execute
			# http://docs.sqlalchemy.org/en/rel_0_9/core/connections.html#understanding-autocommit
			pass

	def execute(self, command):
		if self.conn:
			if '%' in command:
				command = string.replace(command, '%', '%%')
			self.results = self.conn.execute(command)
			# rowcont should not be used it is not portable
			# http://docs.sqlalchemy.org/en/rel_0_9/core/connections.html#sqlalchemy.engine.ResultProxy.rowcount
			return self.results.rowcount
		else:
			return None
	
	def fetchone(self):
		if self.results:
			return self.results.fetchone()
		return ()
	
	def fetchall(self):
		if self.results:
			return self.results.fetchall()
		return ()
	
	def close(self):
		if self.conn:
			self.conn.close()


if __name__ == "__main__":
	d = Database()
	d.connect()


