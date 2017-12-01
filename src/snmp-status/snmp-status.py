#! @PYTHON@
# 
# $Id: snmp-status.py,v 1.15 2012/11/27 00:48:44 phil Exp $
#
# SNMP based cluster wide ps
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
#
# $Log: snmp-status.py,v $
# Revision 1.15  2012/11/27 00:48:44  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.14  2012/05/06 05:48:49  phil
# Copyright Storm for Mamba
#
# Revision 1.13  2011/07/23 02:30:50  phil
# Viper Copyright
#
# Revision 1.12  2010/09/07 23:53:09  bruno
# star power for gb
#
# Revision 1.11  2009/05/01 19:07:09  mjk
# chimi con queso
#
# Revision 1.10  2008/10/18 00:56:02  mjk
# copyright 5.1
#
# Revision 1.9  2008/03/06 23:41:45  mjk
# copyright storm on
#
# Revision 1.8  2007/06/23 04:03:25  mjk
# mars hill copyright
#
# Revision 1.7  2006/09/11 22:47:27  mjk
# monkey face copyright
#
# Revision 1.6  2006/08/10 00:09:45  mjk
# 4.2 copyright
#
# Revision 1.5  2005/12/31 07:35:47  mjk
# - sed replace the python path
# - added os makefiles
#
# Revision 1.4  2005/10/12 18:08:46  mjk
# final copyright for 4.1
#
# Revision 1.3  2005/09/16 01:02:25  mjk
# updated copyright
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
# Revision 1.8  2001/11/05 20:23:30  mjk
# - Fixed 'args' problem with --ps dump (failed most of the time)
# - Remove debug print statements for --rpm
#
# Revision 1.7  2001/05/09 20:17:23  bruno
# bumped copyright 2.1
#
# Revision 1.6  2001/04/10 14:16:32  bruno
# updated copyright
#
# Revision 1.5  2001/03/07 23:55:15  mjk
# - Handles case when server responds with bad hex only data.
# - RedHat 7.0 doesn't report RPMS anymore
# - Default to ps data if no flag are given.
#
# Revision 1.4  2001/02/21 05:56:53  mjk
# Web docs and manpages
#
# Revision 1.3  2001/02/14 20:16:36  mjk
# Release 2.0 Copyright
#
# Revision 1.2  2000/11/02 05:13:51  mjk
# Added Copyright
#
# Revision 1.1  2000/08/04 22:04:24  mjk
# Initial Checkin
#

import sys
import string
import os
import shutil
import getopt
import re
import popen2

usage_name    = 'SNMP Status'
usage_command = sys.argv[0]
usage_version = '@VERSION@'
usage_text    = "[-ahprv] machines"
usage_help    = \
"\t--all,-a         show all\n" \
"\t--help,-h        help\n" \
"\t--ps, -p         show process status\n" \
"\t--rpm, -r        show installed rpm list\n" \
"\t--verbose, -v    verbose output\n" 

def help() :
    usage()
    print usage_help

def usage() :
    print usage_name, '- version', usage_version
    print 'Usage: ', usage_command, usage_text

def gen_host_list(file, name) :
    retval = []
    file   = open(file, 'r')
    for line in file.readlines():
        fields = string.split(line[:-1])
        if len(fields) > 1 and string.find(fields[1], name) == 0:
            retval.append(fields[1])
    return retval


def snmp_ps(host) :
    table = 'host.hrSWRun.hrSWRunTable'
    entry = 'hrSWRunEntry'
    name   = {}
    args   = {}
    status = {}
    index  = []
    cmd = 'snmpwalk ' + host + ' public ' + table
    for line in os.popen(cmd).readlines() :

        # strip leading key name
        # strip quoted values
        # strip spurious Hex: values
        # create pair list ((key, index), value)
        # cast index into integer
        
        if string.count(line, table, 0):
            line = string.replace(line, table + '.' + entry + '.', '')
            line = string.replace(line, '"', '')
            line = re.sub('\ *Hex:.*$', '', line)
            pair = string.split(line[:-1], '=')
            pair[0] = string.split(pair[0], '.')
            pair[0][1] = int(pair[0][1])

            # pid
            if pair[0][0] == 'hrSWRunIndex':
                index.append(pair[0][1])
            
            # command name (minus trailing .)
            if pair[0][0] == 'hrSWRunName':
                name[pair[0][1]] = string.strip(re.sub('\.$', '', pair[1]))

            # command line (minus traling .)
            if pair[0][0] == 'hrSWRunParameters':
                args[pair[0][1]] = string.strip(re.sub('\.$', '', pair[1]))
            else:
                args[pair[0][1]] = ''

            # job status (minus trailing (N) status)
            if pair[0][0] == 'hrSWRunStatus':
                status[pair[0][1]] = string.strip(re.sub('\(.*\)', '',
                                                         pair[1]))

    table = 'host.hrSWRunPerf.hrSWRunPerfTable'
    entry = 'hrSWRunPerfEntry'
    cpu   = {}
    mem   = {}
    cmd = 'snmpwalk ' + host + ' public ' + table
    for line in os.popen(cmd).readlines() :

        # strip leading key name
        # create pair list ((key, index), value)
        # cast index into integer
        
        if string.count(line, table, 0):
            line = string.replace(line, table + '.' + entry + '.', '')
            pair = string.split(line[:-1], '=')
            pair[0] = string.split(pair[0], '.')
            pair[0][1] = int(pair[0][1])

            # CPU Perf
            if pair[0][0] == 'hrSWRunPerfCPU':
                cpu[pair[0][1]] = int(pair[1])

            # MEM Perf
            if pair[0][0] == 'hrSWRunPerfMem':
                mem[pair[0][1]] = int(re.sub('KBytes$', '', pair[1]))

            

    # build retval list ((pid, arg, cpu, mem, status), ...)
    list = []
    for pid in index:
        list.append(pid, name[pid], args[pid], cpu[pid], mem[pid], status[pid])
    return list

def snmp_rpm(host):
    table = 'host.hrSWInstalled.hrSWInstalledTable'
    entry = 'hrSWInstalledEntry'
    index = []
    rpm   = {}
    date  = {}
    
    cmd = 'snmpwalk ' + host + ' public ' + table
    for line in os.popen(cmd).readlines() :
        # strip leading key name
        # strip quoted values
        # strip spurious Hex: values
        # create pair list ((key, index), value)

        if string.count(line, table, 0):
            line = string.replace(line, table + '.' + entry + '.', '')
            line = string.replace(line, '"', '')
            pair = string.split(line[:-1], '=')
            pair[0] = string.split(pair[0], '.')


            if pair[0][0] == 'hrSWInstalledIndex':
                index.append(pair[0][1])
            
            if pair[0][0] == 'hrSWInstalledName':
                rpm[pair[0][1]] = string.strip(pair[1])

            if pair[0][0] == 'hrSWInstalledDate':
                date[pair[0][1]] = string.split(string.strip(pair[1]), ',')

    # build retval list ((pid, arg, status), ...)
    list = []
    for i in index:
        list.append(rpm[i], date[i])
    return list


do_ps      = 0
do_rpm     = 0
do_verbose = 0

opts, args =  getopt.getopt(sys.argv[1:], 'hprva',
                            ["help", "ps", "rpm", "verbose", "all"])

for c in opts :
    if c[0] == '-h' or c[0] == '--help':
        help()
        sys.exit(0)
    elif c[0] == '-p' or c[0] == '--ps':
        do_ps = 1
    elif c[0] == '-r' or c[0] == '--rpm':
        do_rpm = 1
    elif c[0] == '-v' or c[0] == '--verbose':
        do_verbose = 1
    elif c[0] == '-a' or c[0] == '--all':
        do_ps  = 1
        do_rpm = 1


if not args:
    host_list = gen_host_list('/etc/hosts', 'compute')
else:
    host_list = args

data = {}

# default mode is remote ps
if not do_ps and not do_rpm:
    do_ps = 1

if do_ps:
    dict = {}
    for host in host_list:
        dict[host] = snmp_ps(host)
    data['ps'] = dict

if do_rpm:
    dict = {}
    for host in host_list:
        dict[host] = snmp_rpm(host)
    data['rpm'] = dict


if data.has_key('ps'):
    for host in data['ps'].keys():
        if len(data['ps'].keys()) > 1:
            prefix = host
        else:
            prefix = ''
        if do_verbose:
            print '%s    PID   TIME    MEM  PROCESS' % (prefix)
        for job in data['ps'][host]:
            print '%s %6d %6d %6d  %s %s' % (prefix, job[0], job[3], job[4],
                                             job[1], job[2])

if data.has_key('rpm'):
    for host in data['rpm'].keys():
        for rpm in data['rpm'][host]:
            if len(data['rpm'].keys()) > 1:
                prefix = host
            else:
                prefix = ''
            print '%s %s' % (prefix, rpm[0])

