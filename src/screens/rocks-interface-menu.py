#! @PYTHON@
# $Id: rocks-interface-menu.py,v 1.1 2012/03/13 06:05:58 phil Exp $
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
# @Copyright@
# $Log: rocks-interface-menu.py,v $
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
