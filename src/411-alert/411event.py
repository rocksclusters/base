#!/opt/rocks/bin/python
# This handles a 411Alert event sent through serf
# if no specific url is given, get everything 
#
import os
import sys
import subprocess
from rocks.four11handler import Handle411

# check if this is a 411Alert event
try:
	ename = os.environ["SERF_USER_EVENT"]
	if ename != "411Alert":
		# not for us
		os.exit(0)
	# fork off a child process because the 411 event handling might take
	# a while
	pid = os.fork()
	if pid != 0:
		sys.exit(0)

	# Child
	url = sys.stdin.read()
	if len(url) >  0:
		H = Handle411()
		H.apply(url.strip(),None)
	else:
		subprocess.call(["/opt/rocks/bin/411get","--all"])
	os._exit(0)
except:
	# This serf event is not for us 
	pass
		 
