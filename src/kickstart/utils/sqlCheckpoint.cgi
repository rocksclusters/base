#!/usr/bin/python
#
# CGI script to read data from a frontend sent by HTTP POST. Study.
#
# @COPYRIGHT@
# @COPYRIGHT@
#
# Authors: Federico Sacerdoti 2005
#
# $Log: sqlCheckpoint.cgi,v $
# Revision 1.1  2005/05/23 23:59:24  fds
# Frontend Restore
#
#

import cgi
import sys
import os
import rocks.sql


class App(rocks.sql.Application):
	"""A CGI script that reads data about a cluster checkpoint,
	sent in HTTP POST format.
	Assumes that if you were able to call this script, you are
	authorized to alter the database."""
	
	def __init__(self):
		rocks.sql.Application.__init__(self)
		self.site = 0
		self.client = ''
		self.columns = {}
		self.inserted = 0
		return


	def insertSiteId(self, client):
		"Adds or queries a site ID in the Sites table. Returns the id"

		rows = self.execute('select id from sites where address="%s"' 
				% client)
		if rows:
			id = self.fetchone()[0]
		else:
			self.execute('insert into sites (address) values ("%s")' 
				% client)
			id = self.insertId()
		return int(id)


	def insertRow(self, table, row):
		"""Inserts a row in the cluster database. Used for simple
		table updates."""

		# Construct an SQL insert value list. Not quite
		# like a Python tuple (NULL particularly).

		cleanrow = '('
		i = 0
		for col in row:
			if i:
				cleanrow += ', '
			if col is None:
				cleanrow += 'NULL'
			else:
				# Important to escape single quotes in
				# the field.
				cleanrow += self.link.escape(col)
			i += 1
		cleanrow += ', %d)' % self.site

		insert = 'insert into %s (%s) values %s' \
			% (table, self.columns[table], cleanrow)
		#print insert
		self.execute(insert)


	def insertCmd(self, cmd):
		"Command is like insert-ethers or add-extra-nic"
		
		#
		# Add --site flag
		#
		tok = cmd.split()
		cmd = "%s --site=%s %s > /dev/null 2>&1" % (tok[0], self.client, 
			" ".join(tok[1:]))
		#print "Running cmd '%s'" % cmd
		rc = os.system(cmd)
		if rc == 256:
			raise Exception, "Could not insert with %s" % cmd
		self.inserted += 1


	def deleteSite(self, table):
		"""Deletes all rows for a site from the database"""

		delete = 'delete from %s where site=%s' \
			% (table, self.site)
		self.execute(delete)
		print " Cleaned table", table


	def deleteSiteNodes(self):
		
		self.execute('select id from nodes where site=%d' % self.site)
		for row in self.fetchall():
			nodeid = row[0]
			self.execute('delete from networks where node=%d' 
				% nodeid)
			self.execute('delete from nodes where id=%d' % nodeid)
		print " Cleaned Nodes and Networks"


	def run(self):
		self.connect()

		print "Content-Type: text/html"
		print

		self.client=os.environ['REMOTE_ADDR']
		self.site = self.insertSiteId(self.client)

		if 'CONTENT_LENGTH' not in os.environ:
			print "error - Did not find any input from you (%s)" \
				% self.client
			return
		bytes = int(os.environ['CONTENT_LENGTH'])
		data = cgi.parse_qs(sys.stdin.read(bytes))

		#
		# First pass to get table column names (according to client)
		#
		self.columns = {}
		cleanme = []
		for key in data:
			table, id = key.split('-')
			if id == 'columns':
				self.columns[table] = data[key][0] + ', site'
				cleanme.append(key)

		print "Checkpointing site %d (%s):" % (self.site, self.client)
		#
		# Clean POST data
		#
		for key in cleanme:
			del data[key]
			table, id = key.split('-')
			self.deleteSite(table)

		#
		# Clean nodes from this site
		#
		self.deleteSiteNodes()

		#
		# Insert and run commands
		#
		commands = {}
		for key, val in data.items():
			table, id = key.split('-')
			if table=='command':
				commands[int(id)] = val[0][:-1]
			else:
				try:
					self.insertRow(table, eval(val[0]))
				except Exception, msg:
					print "error - %s" % msg

		# 
		# Need to order the commands
		#
		seq = commands.keys()
		seq.sort()
		for id in seq:
			try:
				self.insertCmd(commands[id])
			except Exception, msg:
				print "error - %s" % msg


		print " Inserted %d Rows in tables %s" % (len(data), 
			self.columns.keys())
		print " Inserted %d nodes" % self.inserted
		print " Finished cluster sql checkpoint"

#
# My Main
#
app=App()
app.run()
