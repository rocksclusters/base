#! @PYTHON@
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
# $Log: ssl-genca.py,v $
# Revision 1.16  2012/11/27 00:48:51  phil
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
# Revision 1.11  2008/10/18 00:56:03  mjk
# copyright 5.1
#
# Revision 1.10  2008/03/06 23:41:46  mjk
# copyright storm on
#
# Revision 1.9  2007/06/23 04:03:26  mjk
# mars hill copyright
#
# Revision 1.8  2006/09/11 22:47:30  mjk
# monkey face copyright
#
# Revision 1.7  2006/08/10 00:09:47  mjk
# 4.2 copyright
#
# Revision 1.6  2006/01/16 06:49:02  mjk
# fix python path for source built foundation python
#
# Revision 1.5  2005/10/12 18:08:47  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:02:26  mjk
# updated copyright
#
# Revision 1.3  2005/07/11 23:51:38  mjk
# use rocks version of python
#
# Revision 1.2  2005/05/24 21:22:01  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/01 02:04:42  mjk
# moved from core to base
#
# Revision 1.13  2004/03/25 03:15:53  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.12  2003/08/15 22:34:47  mjk
# 3.0.0 copyright
#
# Revision 1.11  2003/05/22 16:39:28  mjk
# copyright
#
# Revision 1.10  2003/02/17 18:43:05  bruno
# updated copyright to 2003
#
# Revision 1.9  2002/10/18 21:33:26  mjk
# Rocks 2.3 Copyright
#
# Revision 1.8  2002/02/21 21:33:27  bruno
# added new copyright
#
# Revision 1.7  2001/05/09 20:17:17  bruno
# bumped copyright 2.1
#
# Revision 1.6  2001/04/10 14:16:30  bruno
# updated copyright
#
# Revision 1.5  2001/02/15 00:32:07  mjk
# Fixed perms on ca.crt
#
# Revision 1.4  2001/02/14 20:16:32  mjk
# Release 2.0 Copyright
#
# Revision 1.3  2001/02/14 19:09:44  mjk
# - Don't copy CA Cert over to /var/lib/ssl/certs/ (fixed rexec)
# - Buried some dead code
# - Create the cert dir in the spec file
#
# Revision 1.2  2001/02/14 01:27:36  mjk
# - Lock down key and cert permissions a bit better
# - We still have our pants down since all the keys are unencrypted
#
# Revision 1.1  2001/02/14 01:20:48  mjk
# Initial checkin, actually works!
#


import sys
import string
import os
import getopt
import socket
import popen2

usage_name    = 'SSL Generate Certificate Authority'
usage_command = sys.argv[0]
usage_version = '@VERSION@'
usage_text    = '[-hd] [-p path]'
usage_help    = \
'\t--dump,-d     Dump certificate into human form' \
'\t--help,-h     Help\n' \
'\t--path,-p     Set the root of the SSL cert/config tree\n'



def help():
    usage()
    print usage_help


def usage():
    print usage_name, '- version', usage_version
    print 'Usage: ', usage_command, usage_text

def ypdomain():
    for line in os.popen('/bin/ypdomainname').readlines():
        return line[:-1]

def domainname():
    try:
        file = open('/etc/resolv.conf', 'r')
    except:
        print 'warning: no domain name'
    for line in file.readlines():
        fields = string.split(line[:-1], ' ')
        if fields[0] == 'domain':
            return fields[1]
    return 'unknown'
    
    

def gen_ca():    
    if not os.path.isdir(certdir):
        try:
            os.makedirs(certdir)
        except:
            print 'cannot create certificate directory %s' % (certdir)
            sys.exit(-1)

    # Generate Certificate Authority (CA) private key (PEM format).
    # Until we get everything working don't encrpyt the private key
    # (pants down mode).
    if os.path.isfile(ca_key):
        print 'CA Key already present'
    else:
        os.system('%s genrsa -out %s 2048' % (openssl, ca_key))
        os.chmod(ca_key, 0600)


    # Write an openssl configuration to set us up to self-signed the
    # above private key.
    cnf = os.path.join(ssldir, 'genca.config')
    try:
        file = open(cnf, 'w')
    except:
        print 'cannot write config file %s' % (cnf)
        sys.exit(-1)
    file.write('[ req ]\n')
    file.write('distinguished_name = req_distinguished_name\n')
    file.write('\n[ req_distinguished_name ]\n')
    file.write('organizationName               = Organization Name\n')
    file.write('organizationName_default       = NPACI Rocks\n')
    file.write('commonName                     = Common Name (hostname)\n')
    file.write('commonName_default             = %s@%s\n' %
               (ypdomain(), domainname()))
    file.write('commonName_max                 = 64\n')
    file.close()

    # Generate self signed CA Certificate (X509 structure) with the RSA
    # key of the CA (output also PEM format).
    if os.path.isfile(ca_crt):
        print 'CA Certificate already present'
    else:    
        os.system('%s req -new -x509 -days 730 -config %s -key %s -out %s' %
                  (openssl, cnf, ca_key, ca_crt))
        os.chmod(ca_crt, 0644)

def dump_ca():
    print 'CA Certificate'
    print '--------------'
    os.system('%s x509 -noout -text -in %s' % (openssl, ca_crt))
    print 'CA Private Key'
    print '--------------'
    os.system('%s rsa  -noout -text -in %s' % (openssl, ca_key))
           



try:
    opts, args = getopt.getopt(sys.argv[1:], 'dhp:', 
                               ['dump', 'help', 'path='])
except:
    usage()
    sys.exit(0)

do_dump = 0                             # Don't dump on default
ssldir	= '@CERTDIR@'
openssl	= '@OPENSSL@'
config	= {}
config['country_name']	= 'US'
config['state_name']	= 'California'
config['city_name']	= 'La Jolla'
config['org_name']	= 'NPACI Rocks'

for c in opts:
    if c[0] in [ '-d', '--dump' ]:
        do_dump = 1
    elif c[0] in [ '-p', '--path' ]:
        ssldir = c[1]
    elif c[0] in [ '-h', '--help' ]:
        help()
        sys.exit(0);

certdir = os.path.join(ssldir, 'certs')
ca_key  = os.path.join(certdir, 'ca.key')
ca_crt  = os.path.join(certdir, 'ca.crt')

gen_ca()
if do_dump:
    dump_ca()
