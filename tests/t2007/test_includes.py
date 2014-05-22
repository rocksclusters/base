#!/opt/rocks/bin/python
#
# not used at the moment

import os
import string
import sys
import syslog


currentdir = os.path.dirname(os.path.realpath(__file__))
newdir = os.path.realpath(currentdir + '/../../include/applets/')

sys.path.append(newdir)	

import socket
hostname = socket.gethostname()

import ConfigPartitions
app = ConfigPartitions.App()
app.setHostname(hostname)
app.run()

