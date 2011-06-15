#!@PYTHON@

# $Id: rocks-db-perms.py,v 1.3 2011/06/15 16:50:58 phil Exp $

# @Copyright@
# @Copyright@

# $Log: rocks-db-perms.py,v $
# Revision 1.3  2011/06/15 16:50:58  phil
# Different way to grant permissions on temporary tables.
#
# Revision 1.2  2011/06/10 19:30:29  anoop
# -All grants now moved to rocks-db-perms.py
# -Changed ordering so that database-security
#  is setup before any database accesses
# -Bug fixes
#
# Revision 1.1  2011/06/08 19:47:23  anoop
# Moved script for setting up rocks db table access to
# admin scripts from node XML files
#

import os
import sys
import re
import string
import base64

import MySQLdb

# Set access permissions to the database tables

# Get password
f = open('/root/.rocks.my.cnf','r')
password = ''
for line in f.readlines():
	if line.split('=')[0].strip() == 'password':
		password = line.split('=')[1].strip()
		break
f.close()

# Get all the local hostname that apache is
# allowed to connect from.
d = MySQLdb.connect(user='root',
	db='mysql',
	passwd=password,
	unix_socket='/var/opt/rocks/mysql/mysql.sock')

try:
	db = d.cursor()
except:
	sys.exit(-1)

db.execute('select host from user where user="apache" ' +\
	'and host!="localhost"')
(priv_host,) = db.fetchone()

# Connect to the database
d = MySQLdb.connect(user='root',
	db='cluster',
	passwd=password,
	unix_socket='/var/opt/rocks/mysql/mysql.sock')

try:
	db = d.cursor()
except:
	sys.exit(-1)

# Get a list of all tables in the database
db.execute('show tables')
tables = db.fetchall()

# Reg-exp to match secure attributes tables
sec_re = re.compile('sec_[a-zA-Z]*_attributes')

# Set of commands that will set db permissions
cmd_set = []

# For each table set permissions
for (tab_name,) in tables:
	# If the table is a secure attributes table, move on
	if sec_re.match(tab_name):
		continue
	# Otherwise explicitly grant some privileges
	else:
		cmd_set.append('grant select on cluster.%s to ""@"localhost"' % tab_name)
		cmd_set.append('grant select on cluster.%s to ""@"%%.local"' % tab_name)
		cmd_set.append('grant select,insert,update,delete on cluster.%s to "apache"@"localhost"' % tab_name)
		cmd_set.append('grant select,insert,update,delete on cluster.%s to "apache"@"%s"' % (tab_name, priv_host))

# Finally grant apache the ability to lock a table if necessary
cmd_set.append('grant lock tables on cluster.* to "apache"@"localhost"')
cmd_set.append('grant lock tables on cluster.* to "apache"@"%s"' % priv_host)

# Do the same for procedures and functions;
db.execute('show procedure status')
for row in db.fetchall():
	cmd_set.append('grant execute on procedure cluster.%s to "apache"@"localhost"' % row[1])
	cmd_set.append('grant execute on procedure cluster.%s to ""@"localhost"' % row[1])
	cmd_set.append('grant execute on procedure cluster.%s to ""@"%%.local"' % row[1])

db.execute('show function status')
for row in db.fetchall():
	cmd_set.append('grant execute on function cluster.%s to "apache"@"localhost"' % row[1])
	cmd_set.append('grant execute on function cluster.%s to ""@"localhost"' % row[1])
	cmd_set.append('grant execute on function cluster.%s to ""@"%%.local"' % row[1])

# Grant all access to temporary tables
cmd_set.append('GRANT CREATE TEMPORARY TABLES ' +\
	'on TEMPTABLES.* to ""@"localhost","apache"@"localhost",""@"%%.local"') 
cmd_set.append('GRANT SELECT, INSERT, UPDATE, DELETE, DROP, ALTER ' +\
	'on TEMPTABLES.* to ""@"localhost","apache"@"localhost",""@"%%.local"') 

# Run through the command set
for cmd in cmd_set:
	try:
		db.execute(cmd)
	except:
		sys.stderr.write('Could not execute "%s"\n' % cmd)
		
