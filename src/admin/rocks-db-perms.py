#!@PYTHON@

# $Id: rocks-db-perms.py,v 1.1 2011/06/08 19:47:23 anoop Exp $

# @Copyright@
# @Copyright@

# $Log: rocks-db-perms.py,v $
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

# Connect to the database
d = MySQLdb.connect(user='root',
	db='cluster',
	passwd=password,
	unix_socket='/var/opt/rocks/mysql/mysql.sock')

try:
	db = d.cursor()
except:
	sys.exit(-1)

# Get the private hostname either from the database
# or from the /tmp/site.attrs file
if db.execute('select value from global_attributes where ' +\
	'attr="Kickstart_PrivateHostname"') != 0:
	(priv_hostname,) = db.fetchone()

else:
	f = open('/tmp/site.attrs')
	for line in f.readlines():
		if line.split(':')[0].strip() == 'Kickstart_PrivateHostname':
			priv_hostname = line.split(':')[1].strip() 
			break

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
		cmd_set.append('grant select,insert,update,delete on cluster.%s to "apache"@"%s"' % (tab_name, priv_hostname))

# Finally grant apache the ability to lock a table if necessary
cmd_set.append('grant lock tables on cluster.* to "apache"@"localhost"')
cmd_set.append('grant lock tables on cluster.* to "apache"@"%s"' % priv_hostname)

# Run through the command set
for cmd in cmd_set:
	db.execute(cmd)

