#! @PYTHON@
#
# $Id: snmp-gather-ps.py,v 1.10 2008/03/06 23:41:45 mjk Exp $
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
# $Log: snmp-gather-ps.py,v $
# Revision 1.10  2008/03/06 23:41:45  mjk
# copyright storm on
#
# Revision 1.9  2007/06/23 04:03:25  mjk
# mars hill copyright
#
# Revision 1.8  2006/09/11 22:47:27  mjk
# monkey face copyright
#
# Revision 1.7  2006/08/10 00:09:45  mjk
# 4.2 copyright
#
# Revision 1.6  2005/12/31 07:35:47  mjk
# - sed replace the python path
# - added os makefiles
#
# Revision 1.5  2005/10/12 18:08:46  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:02:25  mjk
# updated copyright
#
# Revision 1.3  2005/08/08 21:24:56  mjk
# foundation
#
# Revision 1.2  2005/05/24 21:22:00  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/01 02:03:16  mjk
# moved from core to base
#
# Revision 1.12  2004/03/25 03:15:51  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.11  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.10  2003/05/22 16:39:28  mjk
# copyright
#
# Revision 1.9  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.8  2002/10/18 21:33:26  mjk
# Rocks 2.3 Copyright
#
# Revision 1.7  2002/02/21 21:33:28  bruno
# added new copyright
#
# Revision 1.6  2001/05/09 20:17:22  bruno
# bumped copyright 2.1
#
# Revision 1.5  2001/04/10 14:16:32  bruno
# updated copyright
#
# Revision 1.4  2001/02/14 20:16:36  mjk
# Release 2.0 Copyright
#
# Revision 1.3  2000/11/02 05:13:51  mjk
# Added Copyright
#

# Gather-ps will get process data from all compute nodes using snmp
# and insert it into the 'ps' table in the database. It uses the
# snmp-status.py script to actually obtain process data.

import sys
import string
import getopt
import os
from MySQLdb import *

usage_name    = 'SNMP Gather ps'
usage_command = sys.argv[0]
usage_version = '@VERSION@'
usage_text    = "[-hv] [--db=database] database_user [host]"
usage_help    = \
"\t--help,-h          help\n"\
"\t--verbose,-v		verbose output\n"\
"\t--db=database		optional database name\n"

def help():
   usage()
   print usage_help
 
def usage():
   print usage_name, '- version', usage_version
   print 'Usage: ', usage_command, usage_text

user=None
host='localhost'
db='cluster'
do_verbose=0

try:
	opts, args = getopt.getopt(sys.argv[1:], 'hv', ['help','verbose','db='])
except getopt.GetOptError:
	usage()
	sys.exit(0)

for key, val in opts:
	if key=='--db':
		db=val
	elif key in ("-v", "--verbose"):
		do_verbose=1
	elif key in ("-h", "--help"):
		help()
		sys.exit(0)

if not args:
	usage()
	sys.exit(1)
elif len(args)==1:
	user=args[0]
elif len(args)==2:
	user=args[0]
	host=args[1]

if not os.path.isfile("./snmp-status.py"):
	print "I need to be in the same directory as 'snmp-status.py'."
	print "May I suggest a kickstart :)"
	sys.exit(1)

mylink=connect(host='%s'%(host), user='%s'%(user), db='%s'%(db))

mycursor=mylink.cursor()

# Get timestamp for all processes from database
query="select now()"
mycursor.execute(query)
timestamp=mycursor.fetchone()[0]		# fetchone() returns a list, we want a string

query="select id, name from nodes where name like 'compute%'"
mycursor.execute(query)

nodes={}
for row in mycursor.fetchall():
	nodes[row[1]]=row[0]		# Make dictionary 'compute-n: id'

def mysort(x,y):
	"Sort a list of 'compute-n' elements correctly"
	X=string.atoi(string.replace(x,'compute-',''))
	Y=string.atoi(string.replace(y,'compute-',''))
	return X-Y

def addslashes (line):
	"Escapes all ' symbols with a backslash. MySQL database inserts need to use this."
	return string.replace(line,"'","\'")

def stripslashes (line):
	"The complement to addslashes. Needed when pulling data from a mysql database"
	return string.replace(line,"\'","'")

nodelist=nodes.keys()
nodelist.sort(mysort)

for node in nodelist:
	cmd="./snmp-status.py --ps %s" % node
	id=nodes[node]

	if do_verbose: print 'Processes for %s' % node
	for line in os.popen(cmd).readlines():
		line=string.split(line)
		PID, TIME, MEM = line[:3]
		PROCESS=string.join(line[3:])
		if do_verbose: print "%s, %s, %s, %s" % (PID,TIME,MEM,PROCESS)
		insert="insert into ps values ('%s','%s','%s','%s','%s','%s')" % \
			(timestamp,PID,id,addslashes(PROCESS),TIME,MEM)
		mycursor.execute(insert)
