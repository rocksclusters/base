#!/opt/rocks/bin/python
#
# $Id: setPxeboot.cgi,v 1.14 2012/11/27 00:48:40 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWindwer)
# 		         version 7.0 (Manzanita)
# 
# Copyright (c) 2000 - 2017 The Regents of the University of California.
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
# $Log: setPxeboot.cgi,v $
# Revision 1.14  2012/11/27 00:48:40  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.13  2012/05/06 05:48:46  phil
# Copyright Storm for Mamba
#
# Revision 1.12  2011/07/23 02:30:48  phil
# Viper Copyright
#
# Revision 1.11  2010/09/07 23:53:08  bruno
# star power for gb
#
# Revision 1.10  2009/05/01 19:07:08  mjk
# chimi con queso
#
# Revision 1.9  2008/12/15 22:27:21  bruno
# convert pxeboot and pxeaction tables to boot and bootaction tables.
#
# this enables merging the pxeaction and vm_profiles tables
#
# Revision 1.8  2008/10/18 00:56:01  mjk
# copyright 5.1
#
# Revision 1.7  2008/09/08 22:37:51  bruno
# nuke runRocksCommand.cgi
#
# Revision 1.6  2008/08/20 22:52:58  bruno
# install a virtual cluster of any size in 6 simple steps!
#
# Revision 1.5  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.4  2007/06/23 04:03:24  mjk
# mars hill copyright
#
# Revision 1.3  2007/05/02 20:20:53  bruno
# added 'pxeaction' table -- allows for adding and removing pxeboot actions
#
# Revision 1.2  2007/05/01 22:48:26  bruno
# pxeboot works for pxe first and pxe last nodes
#
# Revision 1.1  2007/04/30 22:02:12  bruno
# first pass at rocks-pxeboot package
#
#

import os
import socket
import string
import cgi
import re

#
# get the name of the node that is issuing the request
#
ipaddr = ''
if os.environ.has_key('REMOTE_ADDR'):
	ipaddr = os.environ['REMOTE_ADDR']

#
# see if an action was set
#
form = cgi.FieldStorage()
if form.has_key('action'):
	testaction = form['action'].value
else:
	testaction = 'os'


# Sanitize the action sent to us. Only allow alphanumeric
unallowed = re.compile('[^a-zA-Z0-9 ]+')
if unallowed.search(testaction):
	action = 'os'
else:
	action = testaction

#
# convert the requesting IP address into a simple hostname (only the hostname
# and not a FQDN)
#
(name, aliaslist, ipaddrlist) = socket.gethostbyaddr(ipaddr)
host = string.split(name, '.')[0]

#
# set the host boot off its local disk
#
os.system('/opt/rocks/bin/rocks set host boot %s ' % (host) + \
	'action="%s" > /dev/null 2>&1' % (action))

#
# send a web response back to the node
#
print 'Content-type: application/octet-stream'
print 'Content-length: %d' % (len(''))
print ''
print ''

