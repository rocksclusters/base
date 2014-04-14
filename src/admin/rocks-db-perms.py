#!@PYTHON@

# $Id: rocks-db-perms.py,v 1.8 2012/11/27 00:48:08 phil Exp $

# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 6.1.1 (Sand Boa)
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

# $Log: rocks-db-perms.py,v $
# Revision 1.8  2012/11/27 00:48:08  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.7  2012/05/06 05:48:17  phil
# Copyright Storm for Mamba
#
# Revision 1.6  2011/08/25 19:31:24  anoop
# Revert back to using /root as root directory.
# Better to make a symlink on Solaris rather than
# changing the entire code base to use / as root directory
#
# Revision 1.5  2011/08/24 23:21:10  anoop
# Root directory is different on Linux and solaris
#
# Revision 1.4  2011/07/23 02:30:23  phil
# Viper Copyright
#
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
f = open('/root/.rocks.my.cnf' ,'r')
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
		
