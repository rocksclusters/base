#!/opt/rocks/bin/python
#
# $Id: rocks-bt.py,v 1.20 2009/08/24 19:15:01 bruno Exp $
#
# @Copyright@
# @Copyright@
#
# $Log: rocks-bt.py,v $
# Revision 1.20  2009/08/24 19:15:01  bruno
# more
#
# Revision 1.19  2009/08/24 16:40:23  bruno
# lots o' loggin'
#
# Revision 1.18  2009/08/24 14:53:58  bruno
# more
#
# Revision 1.17  2009/08/24 14:23:33  mjk
# log with timestamp
#
# Revision 1.16  2009/08/23 20:19:22  mjk
# might be better
#
# Revision 1.15  2009/08/19 18:45:29  bruno
# add support for 'avalanche groups'.
#
# if there are multiple peers that are caching a requested package, then
# attempt to get the package from a peer that has the same group id as you.
#
# group ids are set with the 'avalanche-group' attribute.
#
# Revision 1.14  2008/10/28 20:16:42  bruno
# check if anancoda has asked for a package two times in a row. if so, we
# assume the package is corrupted and we instruct the node to get the package
# from the frontend.
#
# Revision 1.13  2008/06/20 20:42:43  bruno
# reworked to handle:
#
#  1) http 'range' requests when an RPM is partially downloaded and lighttpd
#    asks for the last part of the file (the http_range starts at a non-zero
#    offset)
#
#  2) try to get the requested file from the local disk
#
# #1 fixes an error and #2 speeds up installs.
#
# Revision 1.12  2007/12/10 21:28:34  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.11  2006/12/14 21:54:09  bruno
# just tweak the flags -- like i should of done 3 days ago.
#
# Revision 1.10  2006/06/05 17:57:35  bruno
# first steps towards 4.2 beta
#
# Revision 1.9  2006/03/30 18:15:02  bruno
# look in two places for wget
#
# Revision 1.8  2006/03/09 01:26:55  bruno
# harden the BitTorrent downloader that runs on an installing node.
#
# first, lower the timeout and retries for wget
#
# next, if wget reports a failed download from a peer, mark that peer as 'bad'.
# that way, the bad peer won't be considered in future downloads
#
# Revision 1.7  2006/01/25 19:15:00  mjk
# correct python path
#
# Revision 1.6  2006/01/16 06:48:56  mjk
# fix python path for source built foundation python
#
# Revision 1.5  2005/08/25 16:41:10  bruno
# reduce messages from installing node back to tracker
#
# Revision 1.4  2005/08/18 22:08:08  bruno
# ensure when wget fails to get a file, it doesn't leave a zero-length file
# laying around in the file system
#
# Revision 1.3  2005/08/17 20:29:19  bruno
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
import stat
import os.path
import getopt
import cgi
import string
import time

import sha
import BitTorrent.bencode
import BitTorrent.rocks

def HasTorrent(filename):
	files = [ 
		'images/product.img',
		'images/stage2.img',
		'images/updates.img',
		'repodata/comps.xml',
		'repodata/filelists.xml.gz',
		'repodata/other.xml.gz',
		'repodata/primary.xml.gz',
		'repodata/repomd.xml',
		'.rpm'
		]
	for file in files:
		if filename.rfind(file) != -1:
			return True
	return False

def Log(file, s):
	tm = time.strftime('%d/%b/%Y:%H:%M:%S', time.gmtime())
	file.write('%s - %s\n' % (tm, s))

	
#
# open log file
#
file = open('/tmp/rocks-bt.log', 'a')
Log(file, 'STARTED')

if os.path.exists('/tmp/updates/rocks/bin/wget'):
	wget = '/tmp/updates/rocks/bin/wget'
else:
	wget = '/usr/bin/wget'

#
# set some wget flags
#
wget += ' --dns-timeout=3 --connect-timeout=3 ' \
	'--read-timeout=10 --tries=1 -nv -a/tmp/wget.log'

form = cgi.FieldStorage()
if form.has_key('filename'):
	filename = form['filename'].value
if form.has_key('serverip'):
	host = form['serverip'].value

#
#
#
if os.path.exists('/mnt/sysimage'):
	savefile = '/mnt/sysimage/'
	
	#if not os.path.exists('/mnt/sysimage/install'):
		#cmd = 'rm -rf /install'
		#os.system(cmd)
		#cmd = 'mkdir -p /mnt/sysimage/install'
		#os.system(cmd)
		#cmd = 'ln -s /mnt/sysimage/install /install'
		#os.system(cmd)
else:
	savefile = '/'

#
# if present, peel off the first '/' from filename. otherwise, os.path.join
# will not include 'savefile' as the prefix
#
filename = os.path.normpath(filename)
if filename[0] == '/':
	filename = filename[1:]

savefile = os.path.join(savefile, filename)

dir = os.path.dirname(savefile)
if not os.path.exists(dir):
	os.system('mkdir -p %s' % (dir))
	
Log(file, 'getPeerId:before')

#
# construct a peerid that will be used to talk to the tracker
#
mypeerid = BitTorrent.rocks.getPeerId()

Log(file, 'getPeerId:after')

#
# optimization -- if mypeerid is in the list of peers, that means we already
# have the RPM, just serve it from the local copy
#
Log(file, 'filename: %s' % filename)
havefile = 0
havetorrent = 0
if os.path.exists(os.path.join('/', filename)):
	havefile = 1
	Log(file, 'havefile: %s' % filename)
else:
	torrent_filename = os.path.join('/', filename + '.torrent')
	if os.path.exists(torrent_filename):
		havetorrent = 1
		os.system('cp %s /tmp/torrent' % torrent_filename)
		status = 0
	else:
		#
		# get the torrent file for this file
		#
		cmd = '%s http://%s/%s.torrent --output-document=/tmp/torrent 2> /dev/null' % \
			(wget, host, filename)
	
		backoff = 1
		if HasTorrent(filename):
			tries = 10
			Log(file, 'assume torrent exist for file (%s)' % (filename))
		else:
			tries = 1
	
		while True:
			Log(file, 'attempt to get torrent file for file (%s)' % (filename))
			status = os.system(cmd)
			Log(file, 'torrent file attempt done')
		
			if status == 0:
				break # got the file
			tries -= 1
			if tries:
				sleep(backoff)
				backoff += 1
			else:
				break
	
	if status != 0:
	        Log(file, 'failed to get torrent file for file (%s)' % (filename))
	
		#
		# failed to get the torrent file. just set the peers to the empty
		# list and let the loop below append the name of the frontend to
		# the list. that is, we'll just go to the frontend for the file
		#
		peers = []
		torrentinfo = None
	else:
		Log(file, 'torrent decode start')
	
		torrentfile = open('/tmp/torrent', 'r')
		torrentinfo = BitTorrent.bencode.bdecode(torrentfile.read())
		torrentfile.close()
	
		Log(file, 'torrent decode done')
	
		#
		# peer_id, event, port and left are phony values in order to fake out
		# the tracker
		#
		bogus = mypeerid[0:13] + 'snooped'
		Log(file, 'bogus start')
		peers = BitTorrent.rocks.getPeers(torrentinfo, bogus)
		Log(file, 'bogus middle')
		BitTorrent.rocks.sendToTracker(torrentinfo, bogus, 'done')
		Log(file, 'bogus done')
	
	#
	# if the same file is asked for two times in a row, we assume that anaconda
	# found something wrong with the file (e.g., checksum error).
	#
	# we will tell the tracker that we are no longer a peer for the file and
	# we'll ask for the file directly from the frontend -- we'll do that by
	# clearing out the list of peers.
	#
	if os.path.exists('/tmp/rocks-bt-last-request'):
		f = open('/tmp/rocks-bt-last-request', 'r')
		last_request = f.readline()
		f.close()
	else:
		last_request = ''
	
	if last_request == filename:
		Log(file, 'corner case 1 start')
		BitTorrent.rocks.sendToTracker(torrentinfo, mypeerid, 'done')
		Log(file, 'corner case 1 end')
		peers = []
	
	#
	# save the name of the current requested file.
	#
	f = open('/tmp/rocks-bt-last-request', 'w')
	f.write('%s' % filename)
	f.close()
	
	#
	# put the peers that are from the same avalanche group as this node in
	# the front of the list
	#
	mygroupid = BitTorrent.rocks.getGroupId(mypeerid)
	
	Log(file, 'peers before: %s' % peers)
	
	group = []
	notgroup = []
	for peer in peers:
		if peer.has_key('peer id'):
			if peer['peer id'][13:] == 'snooped':
				continue
	
			elif mygroupid == BitTorrent.rocks.getGroupId(peer['peer id']):
				group.append(peer)
			else:
				notgroup.append(peer)
		
	#
	# put the two groups together and append the kickstart host ip to the
	# end of the list
	#
	peers = group + notgroup + [ {'ip' : host} ]
	
	Log(file, 'peers after: %s' % peers)

if havefile:
	status = 0

if havefile == 0:
	for peer in peers:
		#
		# get the RPM
		#
		tempfile = '/install/' + os.path.basename(savefile)

		Log(file, 'getting RPM start')

		cmd = '%s http://%s/%s -O %s' % (wget, peer['ip'], filename,
			tempfile)

		status = os.system(cmd)

		Log(file, 'getting RPM end')

		#
		# output the request to a log file
		#
		Log(file, 'http://%s/%s : status %d' %
						(peer['ip'], filename, status))

		if status == 0:
			#
			# save the file so another installing node can
			# download it from us
			#
			Log(file, 'mv start')
			cmd = 'mv %s %s' % (tempfile, savefile)
			os.system(cmd)
			Log(file, 'mv end')
			break
		else:
			#
			# if the download fails, then tell the tracker that
			# this 'peer' is bad
			#
			#if peer.has_key('peer id'):
				#BitTorrent.rocks.sendToTracker(torrentinfo,
					#peer['peer id'], 'done')

			#
			# wget has a bad side effect -- if the file doesn't
			# exist and if you use the '-O' flag, it will create a
			# zero-length file.
			#
			# in this case, remove the zero-length file
			#
			Log(file, 'status non-zero start')
			cmd = 'rm -f %s' % (tempfile)
			os.system(cmd)
			Log(file, 'status non-zero end')

if status == 0:
	#
	# after downloading, output the file to the requesting server
	#
	# if this is a 'byte range' request, then only output the requested
	# bytes
	#
	if os.environ.has_key('HTTP_RANGE'):
		Log(file, 'HTTP_RANGE start')
		bytes = string.split(os.environ['HTTP_RANGE'], '=')
		if len(bytes) > 1:
			range = string.split(bytes[1], '-')
			if len(range) > 1:	
				if len(range[0]) > 0:
					offset = int(range[0])
				else:
					offset = 0

				if len(range[1]) > 0:
					last = int(range[1])
				else:
					last = os.stat(savefile)[stat.ST_SIZE]

				filesize = last - offset + 1
		Log(file, 'HTTP_RANGE end')

	else:
		Log(file, 'full file start')
		filesize = os.stat(savefile)[stat.ST_SIZE]
		Log(file, 'full file end')

	#
	# output the file to the requesting local web server
	#
	# send an HTTP header
	#
	print 'Content-type: application/octet-stream'
	print 'Content-length: %d' % (filesize)
	print ''
	
	fd = os.open(savefile, os.O_RDONLY)

	if os.environ.has_key('HTTP_RANGE'):
		Log(file, 'HTTP_RANGE file output start')
		os.lseek(fd, offset, 0)
		buf = os.read(fd, filesize)
		sys.stdout.write(buf)
		Log(file, 'HTTP_RANGE file output end')
	else:
		#
		# output the entire file
		#
		Log(file, 'full file output start')
		buf = os.read(fd, 131072)
		while len(buf) > 0:
			sys.stdout.write(buf)
			buf = os.read(fd, 131072)
		Log(file, 'full file output end')

	os.close(fd)

	if havefile == 0:
		#
		# now tell the tracker that we have the file
		#
		if not havetorrent:
			Log(file, 'mv-2 start')
			cmd = 'mv /tmp/torrent %s.torrent' % (savefile)
			os.system(cmd)
			Log(file, 'mv-2 end')

		Log(file, 'tell tracker "started" start')
		BitTorrent.rocks.sendToTracker(torrentinfo, mypeerid, 'started')
		Log(file, 'tell tracker "started" end')
	else:
		cmd = 'rm -f /tmp/torrent'
		os.system(cmd)

Log(file, 'END\n')
file.close()

