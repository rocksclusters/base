#! /opt/rocks/bin/python
#
# $Id: rocks-unannounce.py,v 1.4 2006/03/30 18:15:02 bruno Exp $
#
# @COPYRIGHT@
# @COPYRIGHT@
#
# $Log: rocks-unannounce.py,v $
# Revision 1.4  2006/03/30 18:15:02  bruno
# look in two places for wget
#
# Revision 1.3  2006/01/25 19:15:00  mjk
# correct python path
#
# Revision 1.2  2006/01/16 06:48:56  mjk
# fix python path for source built foundation python
#
# Revision 1.1  2005/08/17 20:29:19  bruno
# added a rocks library to the BitTorrent library
#
# Revision 1.2  2005/08/10 01:34:25  bruno
# faster bittorrent download client
#
# Revision 1.1  2005/07/27 01:54:36  bruno
# checkpoint
#
#

import sys
import os
import os.path

import sha
import BitTorrent.bencode
import BitTorrent.rocks

if os.path.exists('/tmp/updates/rocks/bin/wget'):
	wget = '/tmp/updates/rocks/bin/wget'
else:
	wget = '/usr/bin/wget'

if len(sys.argv) != 2:
	sys.exit(-1)

filename = sys.argv[1]

#
# construct a peerid that will be used to talk to the tracker
#
mypeerid = BitTorrent.rocks.getPeerId()

#
# get the torrent file for this file
#
torrentfile = open(filename, 'r')
torrentinfo = BitTorrent.bencode.bdecode(torrentfile.read())
torrentfile.close()

#
# before asking for the file, make sure this host is not listed as a
# possible peer. this may happen when bttrack starts up with stale data
# regarding this file
#
BitTorrent.rocks.sendToTracker(torrentinfo, mypeerid, 'stopped')

