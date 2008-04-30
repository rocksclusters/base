#! /opt/rocks/bin/python
#
# $Id: rocks.py,v 1.6 2007/12/10 21:28:34 bruno Exp $
#
# library routines to interact with a BitTorrent infrastructure
#
#
# @COPYRIGHT@
# @COPYRIGHT@
#
# $Log: rocks.py,v $
# Revision 1.6  2007/12/10 21:28:34  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.5  2006/03/30 18:15:02  bruno
# look in two places for wget
#
# Revision 1.4  2006/01/25 19:15:00  mjk
# correct python path
#
# Revision 1.3  2006/01/16 06:48:56  mjk
# fix python path for source built foundation python
#
# Revision 1.2  2005/08/24 01:23:10  bruno
# added 'done' command
#
# Revision 1.1  2005/08/17 20:29:19  bruno
# added a rocks library to the BitTorrent library
#
#
#

import sys
import os
import os.path
import string

import sha
import BitTorrent.bencode


def getInfoHash(metainfo):
	#
	# calculate the 'info hash' on the torrent file
	#
	hash = ''

	try:
		info = metainfo['info']
		infohash = sha.sha(BitTorrent.bencode.bencode(info))
		for i in infohash.digest():
			 hash += '%%%02x' % (ord(i))
	except:
		pass

	return hash


def getPeerId():
	#
	# construct a peerid, that is 20 characters long
	#
	cmd = 'PATH=/sbin:/usr/sbin ifconfig eth0'
	stdout = os.popen(cmd)

	for line in stdout.readlines():
		l = string.split(line)

		if len(l) > 3 and l[0] == 'eth0' and l[3] == 'HWaddr':
			p = l[4]
			break

	p += '-'
	for i in range(len(p),20):
		p += 'x'
	return p[:20]


def sendToTracker(metainfo, peerid, msg, outputfile='/dev/null'):
	#
	# build up the URL
	#
	buf = ''

	url = '%s?info_hash=%s&peer_id=%s&port=6881&left=0' % \
		(metainfo['announce'], getInfoHash(metainfo), peerid)

	if msg == 'stopped' or msg == 'started':
		url += '&uploaded=0&downloaded=0&compact=1'
		url += '&event=%s' % (msg)
	elif msg == 'snooped' or msg == 'done':
		url += '&event=%s' % (msg)

	if os.path.exists('/tmp/updates/rocks/bin/wget'):
		wget = '/tmp/updates/rocks/bin/wget'
	else:
		wget = '/usr/bin/wget'

	cmd = '%s "%s" --output-document=%s 2> /dev/null' % \
		(wget, url, outputfile)

	file = os.popen(cmd, 'r')
	if outputfile == '-':
		buf = file.read()
	file.close()

	return buf


def getPeers(metainfo, peerid):
	#
	# extract the list of hosts that are currently serving the file
	#
	try:
		i = sendToTracker(metainfo, peerid, 'snooped', '-')
		trackerinfo = BitTorrent.bencode.bdecode(i)
	except:
		trackerinfo = {}
		trackerinfo['peers'] = []
		pass

	if not trackerinfo.has_key('peers'): 
		trackerinfo = {}
		trackerinfo['peers'] = []

	return trackerinfo['peers']

