#! @PYTHON@
#
# $Id: shoot-node.py,v 1.20 2012/11/27 00:48:08 phil Exp $
#
# Re-kickstart a node.
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.6 (Emerald Boa)
# 		         version 6.1 (Emerald Boa)
# 
# Copyright (c) 2000 - 2013 The Regents of the University of California.
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
# $Log: shoot-node.py,v $
# Revision 1.20  2012/11/27 00:48:08  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.19  2012/05/06 05:48:17  phil
# Copyright Storm for Mamba
#
# Revision 1.18  2011/07/23 02:30:23  phil
# Viper Copyright
#
# Revision 1.17  2010/09/07 23:52:48  bruno
# star power for gb
#
# Revision 1.16  2009/05/01 19:06:50  mjk
# chimi con queso
#
# Revision 1.15  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.14  2008/03/06 23:41:32  mjk
# copyright storm on
#
# Revision 1.13  2007/06/23 04:03:19  mjk
# mars hill copyright
#
# Revision 1.12  2006/09/11 22:47:02  mjk
# monkey face copyright
#
# Revision 1.11  2006/08/10 00:09:25  mjk
# 4.2 copyright
#
# Revision 1.10  2006/08/09 15:41:39  anoop
# Changes to shootnode and rocks-console. These changes were necessary to
# support shooting multiple nodes in one command. The threading in shoot-node
# would cause a lot of problems because multiple threads would try to manipulate
# stderr, and all would fail but one.
#
# Also race conditions are created by the presence of threads, and so sockets need
# to be released only at the last possible moment, to avoid multiple bindings.
#
# Revision 1.9  2006/07/06 21:21:23  anoop
# Minor bug fixes
#
# Revision 1.8  2006/07/03 19:30:06  anoop
# Shoot node now supports VNC based installs.
#
# Revision 1.7  2006/06/05 17:57:34  bruno
# first steps towards 4.2 beta
#
# Revision 1.6  2006/01/16 06:48:55  mjk
# fix python path for source built foundation python
#
# Revision 1.5  2005/10/12 18:08:32  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:02:11  mjk
# updated copyright
#
# Revision 1.3  2005/07/11 23:51:32  mjk
# use rocks version of python
#
# Revision 1.2  2005/05/24 21:21:48  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/01 02:02:41  mjk
# moved from core to base
#
# Revision 1.20  2004/09/04 16:00:51  bruno
# shoot-node now works with ssh on port 2200
#
# Revision 1.19  2004/05/06 06:59:28  bruno
# updated shoot-node to play with secure ekv
#
# Revision 1.18  2004/04/28 04:05:21  bruno
# ekv switched from telnet to ssh
#
# Revision 1.17  2004/03/25 03:15:14  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.16  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.15  2003/05/22 16:39:27  mjk
# copyright
#
# Revision 1.14  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.13  2002/10/18 21:33:25  mjk
# Rocks 2.3 Copyright
#
# Revision 1.12  2002/10/03 14:49:25  bruno
# sleep longer in wait loops
#
# Revision 1.11  2002/10/03 14:11:41  bruno
# removed sleep(30) -- it was never a good idea.
#
# Revision 1.10  2002/10/03 14:06:21  bruno
# added -w2 to ping -- otherwise ping hangs when node is dead
#
# Revision 1.9  2002/02/26 23:41:51  mjk
# Increase ekv delay from 10 to 30 seconds.  Still a bad idea, but no time to
# re-write this SC00 stunt.
#
# Revision 1.8  2002/02/21 21:33:27  bruno
# added new copyright
#
# Revision 1.7  2001/11/08 18:42:07  mjk
# NPACI Rocks 2.1.1 Release Copyright Notice
#
# Revision 1.6  2001/10/02 03:53:04  mjk
# - Added DISPLAY check for shoot-node
# - Moved over cluster-* suite of tools from cluster-config
#
# Revision 1.5  2001/05/09 20:17:11  bruno
# bumped copyright 2.1
#
# Revision 1.4  2001/04/10 14:16:27  bruno
# updated copyright
#
# Revision 1.3  2001/02/14 20:16:29  mjk
# Release 2.0 Copyright
#
# Revision 1.2  2000/11/16 22:01:00  mjk
# Can now shoot multiple hosts at the same time.  Shotgun approach.
#
# Revision 1.1  2000/11/06 23:22:44  mjk
# Added shoot-node
#

import sys
import string
import getopt
import os
import time
import popen2
from threading import *

usage_name    = 'Shoot Node'
usage_command = sys.argv[0]
usage_version = '@VERSION@'
usage_text    = "[-h] host ..."
usage_help    = \
"\t-h, --help      help\n"

class Shooter(Thread):
   kickstart = '/boot/kickstart/cluster-kickstart'
   ekvport = '2200'
   known_hosts = "/tmp/.known_hosts"
   ssh_flags = '-q -oStrictHostKeyChecking=no -oUserKnownHostsFile=%s' % known_hosts
   
   def __init__(self, host):
      self.host    = host
      Thread.__init__(self)
      
   def is_host_alive(self):
      return os.system('ping -c1 -w2 %s > /dev/null 2>&1' % (self.host)) == 0
   
   def kickstart_node(self):
      # Spank the node, and process the SSH complaints and passphrase
      # prompt run the script.
      os.system('ssh -f %s %s %s' % (self.ssh_flags, self.host, self.kickstart))
      
   def start_vnc(self):
      # Spawn the vnc window
      if os.environ.has_key('DISPLAY'):
	      print 'Launching rocks-console for %s' % (self.host)
	      os.system('rocks-console %s' % (self.host))
      else:
	     print "DISPLAY variable not set"
	     print "Cannot start VNC console"
	     return(1)
   	
   def wait_for_vnc(self):
      # Wait for VNC server to start. The way we do this
      # is by trying to see is the vnc port is open on the compute node
      # after establishing a secure tunnel
      ssh_args = ['ssh',"%s" % self.host,"-p %s" % self.ekvport,"-o UserKnownHostsFile=%s" % self.known_hosts,"/tmp/updates/rocks/bin/check_port --port 5901 --node localhost"]
      # Close stderr while waiting for vnc to start
      try:
      	fd_temp = os.dup(2)
      	os.close(2)
      except:
      	pass
      count = 0
      while ( os.spawnvp(os.P_WAIT,'ssh',ssh_args) != 0 ):
	      time.sleep(1)
	      if ( count%3 == 0 ):
		      print "Waiting for VNC server on [%s] to start" % self.host
	      count = count+1
	      if (count > 120):
		      print "Can't connect to VNC server after 2 minutes"
		      try:
		      	os.dup2(fd_temp,2)
		      except:
		      	pass
      		      sys.stderr.flush()
	      if (count > 180):
		      print "Cannot connect to VNC server. Bailing out...."
		      break
      try:
      	os.dup2(fd_temp,2)
      except:
      	pass
	
      sys.stderr.flush()


   def wait_for_ssh(self):
      # Wait for ssh setup to complete. This includes the authorized_keys
      # file to be setup. We do this by checking if we can connect to the compute host
      # using ssh
      print "Waiting for ssh setup to complete..."
      self.known_hosts  = "%s_%s" % (self.known_hosts,self.host)
      if os.path.exists(self.known_hosts):
	      os.unlink(self.known_hosts)
	      
      ssh_args = ['ssh','%s' % self.host, '-p %s' % self.ekvport, '-o UserKnownHostsFile=%s' % self.known_hosts,"/usr/bin/echo -n","1>/dev/null","2>&1"]

      try:
      	fd_temp = os.dup(2)
      	os.close(2)
      except:
      	pass
      count = 0
      while ( os.spawnvp(os.P_WAIT,'ssh',ssh_args) != 0 ):
	      time.sleep(1)
	      if ( count%3 == 0 ):
		      print "Waiting for ssh server on [%s] to start" % self.host
	      count = count+1
	      if (count > 120):
		      print "Can't connect to ssh server after 2 minutes"
		      try:
		      	os.dup2(fd_temp,2)
		      except:
		      	pass
      		      sys.stderr.flush()
	      if (count > 180):
		      print "Cannot connect to ssh server. Bailing out...."
		      break
      try:
      	os.dup2(fd_temp,2)
      except:
      	pass
      sys.stderr.flush()



   def wait_for_reboot(self):
      while self.is_host_alive():
         time.sleep(5)
         print '[%s] waiting for machine to go down' % (self.host)

   def wait_for_post(self):
      while not self.is_host_alive():
         print '[%s] waiting for machine to come up' % (self.host)
         time.sleep(5)

   def run(self) :
      if not self.is_host_alive():
         print '[%s] is not alive, cannot kickstart' % (self.host)
         return 0
      start = time.time()
      self.kickstart_node()

      self.wait_for_reboot()
      self.wait_for_post()
      
      self.wait_for_ssh()
      self.wait_for_vnc()
      self.start_vnc()

      os.unlink(self.known_hosts)
      self.wait_for_reboot()
      self.wait_for_post()
      stop = time.time()
      
      print '[%s] done. (%f minutes)' % (self.host, (stop - start) / 60)
      return 1


def help():
   usage()
   print usage_help

def usage():
   print usage_name, '- version', usage_version
   print 'Usage: ', usage_command, usage_text



try:
   opts, args =  getopt.getopt(sys.argv[1:], 'h', ["help"])
except:
   usage()
   sys.exit(-1)
   
for c in opts:
   if c[0] == '-h' or c[0] == '--help':
      help()
      sys.exit(0)

if not len(args):
   usage()
   sys.exit(-1)

if not os.environ.has_key('SSH_AGENT_PID') \
   and not os.environ.has_key('SSH_AUTH_SOCK') \
   and not os.environ.has_key('SSH_NO_PASSWD'):
   usage()
   print 'Requires ssh-agent to launch'
   sys.exit(-1)

# Fire off a bunch of threads to kickstart all the nodes specified,
# and wait for all of them to complete.

pids = []
for host in args:
   j = Shooter(host)
   if j:
      pids.append(j)
      j.start()

for j in pids:
   j.join()
   
