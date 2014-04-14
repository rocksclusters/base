#! @PYTHON@
#
# $Id: snmp-get-ports.py,v 1.16 2012/11/27 00:48:44 phil Exp $
#
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
#
# $Log: snmp-get-ports.py,v $
# Revision 1.16  2012/11/27 00:48:44  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.15  2012/05/06 05:48:49  phil
# Copyright Storm for Mamba
#
# Revision 1.14  2011/07/23 02:30:50  phil
# Viper Copyright
#
# Revision 1.13  2010/09/07 23:53:09  bruno
# star power for gb
#
# Revision 1.12  2009/05/01 19:07:09  mjk
# chimi con queso
#
# Revision 1.11  2008/10/18 00:56:02  mjk
# copyright 5.1
#
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
# Revision 1.14  2004/03/25 03:15:51  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.13  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.12  2003/05/22 16:39:28  mjk
# copyright
#
# Revision 1.11  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.10  2002/10/18 21:33:26  mjk
# Rocks 2.3 Copyright
#
# Revision 1.9  2002/02/21 21:33:28  bruno
# added new copyright
#
# Revision 1.8  2001/05/09 20:17:22  bruno
# bumped copyright 2.1
#
# Revision 1.7  2001/04/10 14:16:32  bruno
# updated copyright
#
# Revision 1.6  2001/02/14 20:16:36  mjk
# Release 2.0 Copyright
#
# Revision 1.5  2000/11/02 05:13:51  mjk
# Added Copyright
#

# Queries a Cisco Catalyst 2900 series ethernet switch
# for the MAC addresses associated with its ports. Used
# to see what the switch sees.

import sys
import string
import getopt
import os
 
usage_name    = 'Get MACs from Switch'
usage_command = sys.argv[0]
usage_version = '@VERSION@'
usage_text    = "[-hv] [switch_address]"
usage_help    = \
" --help,-h          help\n"\
" --verbose,-v       verbose output\n" 

def help():
   usage()
   print usage_help
 
def usage():
   print usage_name, '- version', usage_version
   print 'Usage: ', usage_command, usage_text  

switch='switch'
do_verbose=1
 
fulloptions= ['help','verbose']
try:
   opts, args = getopt.getopt(sys.argv[1:], 'hv', fulloptions)
except getopt.error:
   usage()
   sys.exit(0)

for key, val in opts:
   if key in ("-v", "--verbose"):
      do_verbose=1
   elif key in ("-h", "--help"):
      help()
      sys.exit(0)
 
if len(args)==1:
   switch=args[0]

print "** Querying the switch for a list of MACs on its ports..."
ports={}

# Get the do1dTpFdbPort SNMP resource from the BRIDGE-MIB (RFC-1286)
cmd="snmpwalk switch public 17.4.3.1.2"
for line in os.popen(cmd).readlines():
	line=line[:-1]
	line=string.replace(line,'17.4.3.1.2.','')
	line=string.split(line,' = ')
	mac=string.split(line[0],'.')

   # A bit tricky: converting a list of decimals in to a MAC address with a
	# map and a labmda function.
	MAC=map((lambda x: "%X" % string.atoi(x)), mac)
	MAC=string.join(MAC,':')

	# There may be multiple MACs on a particular port.
	maclist=ports.get(line[1], [])
	maclist.append(MAC)
	ports[line[1]]=maclist


portlist=ports.keys()
portlist.sort()
for key in portlist:
	print "Port %s (%s) => %s" \
		% (key,len(ports[key]),string.join(ports[key],', '))

print "** Done."
