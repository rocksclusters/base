#! /opt/rocks/bin/python
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
# 
# Copyright (c) 2000 - 2014 The Regents of the University of California.
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
import threading

from sqlalchemy import create_engine
import sqlalchemy
import sqlalchemy.exc

import rocks
from rocks.db.mappings.base import *

threadlocal = threading.local()


class Database(object):
	"""
	This class should proxy all the connection to the database.

	There are two main internal objects inside this class which come from
	sqlalchemy:

	- session: this is used by the ORM layer
	- connection: this is used by the execute statement, so every time
		      you use pure sql

	These two objects have two separate DB connections, which means
	that DB status can be different when queried through them.
	
	Usage Example::

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
		self.conn = None
		self.engine = None


	def setDBPasswd(self, passwd):
		"""
		set the password for the DB

		:type passwd: string
		:param passwd: the password to be set
		"""
		self._dbPasswd = passwd

	def getDBPasswd(self):
		"""
		return the passowrd for the DB connection

		:rtype: string
		:return: a string containing the password for the connection to the 
			 DB. By defualt it is read from /root/.rocks.my.cnf for root
			 and from /opt/rocks/mysql/my.cnf for apache
		"""
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
		except AttributeError:
		        host = 'localhost'
		return host

	def setDBName(self, name):
		self._dbName = name

	def getDBName(self):
		if self._dbName:
			return self._dbName
		return 'cluster'


	def setVerbose(self, verbose):
		"""
		If the verbose is true all the sql will be printed to 
		stdout. This function must be called before the connect

		:type verbose: bool
		:param verbose: if verbose should be set to True

		"""
		self.verbose = verbose


	def connect(self):
		"""
		It start the connection to the DB and create all the internal
		data structure
		"""

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

		self.engine = create_engine(url, pool_recycle=3600)
		# TODO: do not keep a connection active here it not needed
		self.conn = self.engine.connect()


	def reconnect(self):
		"""
		Try to re-establish a connection after a process demonization
		(which closes all open file descriptor).
		"""
		self.engine.dispose()
		self.conn = self.engine.connect()

		
	def getSession(self):
		"""
                Return the current session. If it does not exist it creates one.
		The session is a singleton, you can call this method many time it 
		returns always the same object

		TODO: this should be changed, 
		"""

		session = getattr(threadlocal, "session", None)
		if session:
			return session
		elif self.engine:
			Session = sqlalchemy.orm.sessionmaker(bind=self.engine)
			session = Session()
			setattr(threadlocal, "session", session)
			return session
		else:
			return None

	def closeSession(self):
		"""
		It closes the session and release all its resources. This
		does not close or release the connection (see :meth:`close`)
		"""
		session = getattr(threadlocal, "session", None)
		if session:
			session.close()
			setattr(threadlocal, "session", None)
			return
		return


	def commit(self):
		"""
		Commit the current session if it existsi. *It does not touch the
		connection.*
		"""
		session = self.getSession()
		if session:
			session.commit()
		else:
			# no need to manually commit with sqlalchemy if using execute
			# http://docs.sqlalchemy.org/en/rel_0_9/core/connections.html#understanding-autocommit
			pass

	def execute(self, command):
		"""
		Given a SQL string it run the query and returns the rowcount.
		To get the result use :meth:`fetchone` or :meth:`fetchall`.

		:type command: string
		:param command: if verbose should be set to True

		:rtype: int
		:return: the rowconunt of the query or None if there is not
                         connection
		"""
		if self.conn:
			if '%' in command:
				command = string.replace(command, '%', '%%')
			try:
				self.results = self.conn.execute(command)
			except sqlalchemy.exc.OperationalError as e:
				# the database disconnected us, let's try to reconnect once
				self.renewConnection()
				self.results = self.conn.execute(command)
			# rowcont should not be used it is not portable
			# http://docs.sqlalchemy.org/en/rel_0_9/core/connections.html#sqlalchemy.engine.ResultProxy.rowcount
			return self.results.rowcount
		else:
			return None
	
	def fetchone(self):
		"""
		Fetch one row from the results of the previous query

		:rtype: tuple
		:return: a tuple containing the values of the fetched row.
                         It really returns a :class:`sqlalchemy.engine.result.RowProxy`
                         but it can be treated as a tuple
		"""
		if self.results:
			return self.results.fetchone()
		return ()
	
	def fetchall(self):
		"""
		Fetch all rows from the results of the previous query

		:rtype: list
		:return: a list of tuples containing the values of the fetched rows
		"""
		if self.results:
			return self.results.fetchall()
		return ()
	
	def close(self):
		"""
		It closes the connection only. You also need to close the
		session, if you want to release all the DB resources 
		:meth:`closeSession`
		"""
		if self.results:
			self.results.close()
			self.results = None
		if self.conn:
			self.conn.close()

	def renewConnection(self):
		"""
		It renews the connection, if inactive for few hours mysql
		closes down the connection, so you might need to renew it.
		"""
		self.close()
		self.conn = self.engine.connect()


if __name__ == "__main__":
	d = Database()
	d.connect()


