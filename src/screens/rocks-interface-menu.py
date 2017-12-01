#! @PYTHON@
# $Id: rocks-interface-menu.py,v 1.3 2012/11/27 00:48:42 phil Exp $
# Emit XML code suitable as selection information for 
# interfaces. Interprets the /tmp/interfaces file written by
# Rocks mods to loader
# loader.
#
# Summary:
# rock-interface-menu public|private [default interface]
#       public|private  - Interpret /tmp/interfaces suitable for public 
#                         or private listing. 
#       default interface - e.g., eth1, p2p1.  Specify which should be the
#                           default. Generally provided by a restore roll.
#                           If missing, make a guess.
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
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
# $Log: rocks-interface-menu.py,v $
# Revision 1.3  2012/11/27 00:48:42  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.2  2012/05/06 05:48:48  phil
# Copyright Storm for Mamba
#
# Revision 1.1  2012/03/13 06:05:58  phil
# Look at /tmp/interfaces and create list of interfaces so that user can
# select public and private interfaces.   On single physical interface frontends,
# create a virtual interface for the private.
#
import sys
import os
import string

def emitstr(iface,matchstr,default): 
	global found
	print "<option>%s</option>" % iface[0] 
	if iface[0] == default or \
		(iface[2] == matchstr and not found):
		print "<default>%s</default>" % iface[0]
		found = True 
#
# Main 
#
network="public"
defaultIface=''

if len(sys.argv) >= 3:
	# force the default selection
	defaultIface = sys.argv[2]
if len(sys.argv) >= 2:
	network = sys.argv[1]

ifaces = []
nifs = 0
found = False

file = open('/tmp/interfaces', 'r')

macstr = 'X-RHN-Provisioning'
for line in file.readlines():
	l = string.split(line)

	if len(l) > 3 and l[0][0:len(macstr)] == macstr:
		tag = l[0][:-1]
		iface = l[1]
		macaddr = l[2]
		# ks in the fourth field?
		if len(l) > 4:
			# Frontend /tmp/interfaces file, ks indicates public
			# public network
		 	iftype='public'	
		else:
			iftype='private'
                
		ifaces.append([iface,macaddr,iftype])
		nifs = nifs + 1
file.close()

# Special handling for private 
for iface in ifaces:
	if nifs == 1 and network == "private":
		# We have only one physical interface
		# Define a virtual interface for private networks
		iface[0] = "%s:0" % iface[0]
		iface[2] = 'private'
	emitstr(iface,network,defaultIface)
