#! @PYTHON@
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.5 (Mamba)
# 		         version 6.0 (Mamba)
# 
# Copyright (c) 2000 - 2012 The Regents of the University of California.
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
# $Log: ssl-genuser.py,v $
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
# Revision 1.14  2004/03/25 03:15:53  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.13  2003/08/15 22:34:47  mjk
# 3.0.0 copyright
#
# Revision 1.12  2003/05/22 16:39:28  mjk
# copyright
#
# Revision 1.11  2003/02/17 18:43:05  bruno
# updated copyright to 2003
#
# Revision 1.10  2002/10/18 21:33:26  mjk
# Rocks 2.3 Copyright
#
# Revision 1.9  2002/02/21 21:33:27  bruno
# added new copyright
#
# Revision 1.8  2001/05/09 20:17:17  bruno
# bumped copyright 2.1
#
# Revision 1.7  2001/04/10 14:16:30  bruno
# updated copyright
#
# Revision 1.6  2001/02/17 03:42:07  mjk
# *** empty log message ***
#
# Revision 1.5  2001/02/16 17:59:59  mjk
# Bump version
# Back to -des
# Fixed typos
#
# Revision 1.4  2001/02/16 01:00:31  mjk
# Common name is user from the command line not from the environment.
#
# Revision 1.3  2001/02/15 01:04:50  mjk
# User keys are encrypted with des3
#
# Revision 1.2  2001/02/14 20:16:32  mjk
# Release 2.0 Copyright
#
# Revision 1.1  2001/02/14 01:20:52  mjk
# Initial checkin, actually works!
#


import sys
import string
import os
import getopt
import socket
import pwd

usage_name    = 'SSL Generate User Certificate'
usage_command = sys.argv[0]
usage_version = '@VERSION@'
usage_text    = '[-h] [-p path] username'
usage_help    = \
'\t--help,-h     Help\n' \
'\t--path,-p     Set the root of the SSL cert/config tree\n'



def help():
    usage()
    print usage_help


def usage():
    print usage_name, '- version', usage_version
    print 'Usage: ', usage_command, usage_text

def gen_user():

    # Create the SSL environment if it doesn't already exist
    for d in [ certdir, os.path.join(certdir, 'ca.db.certs') ]:
        if not os.path.isdir(d):
            try:
                os.makedirs(d)
            except:
                print 'cannot create directory %s' % (d)
                sys.exit(-1)
    for f in [ os.path.join(certdir, 'ca.db.index') ]:
        if not os.path.isfile(f):
            os.system('touch %s' % (f))
    for f in [ os.path.join(certdir, 'ca.db.serial') ]:
        if not os.path.isfile(f):
            os.system('echo 01 > %s' % (f))

    # Generate User key (PEM format).
    if os.path.isfile(user_key):
        print 'User Key already present'
    else:
        os.system('%s genrsa -des3 -out %s 2048' % (openssl, user_key))


    # Write an openssl configuration for certificate requests
    cnf = os.path.join(ssldir, 'user-request.config')
    try:
        file = open(cnf, 'w')
    except:
        print 'cannot write config file %s' % (cnf)
        sys.exit(-1)
    file.write('[ req ]\n')
    file.write('prompt             = no\n')
    file.write('distinguished_name = req_distinguished_name\n')
    file.write('\n[ req_distinguished_name ]\n')
    file.write('organizationName       = NPACI Rocks\n')
    file.write('commonName             = %s\n' % user)
    file.close()

    # Generate the Certificate Request
    if os.path.isfile(user_crs):
        print 'Certificate Request already present'
    else:    
        os.system('%s req -new -days 730 -config %s -key %s -out %s' %
                  (openssl, cnf, user_key, user_crs))

    # Write an openssl configuration to sign the request.
    cnf = os.path.join(ssldir, 'user.config')
    if not os.path.isfile(cnf):
        try:
            file = open(cnf, 'w')
        except:
            print 'cannot write config file %s' % (cnf)
            sys.exit(-1)

        file.write('[ ca ]\n')    
        file.write('default_ca = CA_default\n')
        file.write('\n[ CA_default ]\n')
        file.write('dir              = %s\n' % (certdir))
        file.write('certs            = $dir/certs\n')
        file.write('database         = $dir/ca.db.index\n')
        file.write('new_certs_dir    = $dir/ca.db.certs\n')
        file.write('serial           = $dir/ca.db.serial\n')
        file.write('certificate      = $dir/ca.crt\n')
        file.write('private_key      = $dir/ca.key\n')
        file.write('RANDFILE         = $dir/.rand\n')
        file.write('default_days     = 730\n')
        file.write('default_crl_days = 730\n')
        file.write('default_md       = md5\n')
        file.write('policy           = policy_anything\n')
        file.write('\n[ policy_anything ]\n')
        file.write('countryName             = optional\n')
        file.write('stateOrProvinceName     = optional\n')
        file.write('localityName            = optional\n')
        file.write('organizationName        = supplied\n')
        file.write('organizationalUnitName  = optional\n')
        file.write('commonName              = supplied\n')
        file.write('emailAddress            = optional\n')
        file.close()

    # Generate the CA signed User Certificate
    if os.path.isfile(user_crt):
        print 'Server Certificate already present'
    else:
        os.system('%s ca -batch -config %s -out %s -infiles %s' %
                  (openssl, cnf, user_crt, user_crs))


try:
    opts, args = getopt.getopt(sys.argv[1:], 'hp:', 
                               ['help', 'path='])
except:
    usage()
    sys.exit(0)

do_dump = 0                             # Don't dump on default
ssldir	= '@CERTDIR@'
openssl	= '@OPENSSL@'

for c in opts:
    if c[0] in [ '-p', '--path' ]:
        ssldir = c[1]
    elif c[0] in [ '-h', '--help' ]:
        help()
        sys.exit(0);

if not args :                           # no user specified, exit
    usage()
    sys.exit(-1)

for user in args:
    (name, passwd, uid, gid, gecos, dir, shell) = pwd.getpwnam(user)
    certdir   = os.path.join(ssldir,  'certs')
    ca_key    = os.path.join(certdir, 'ca.key')
    ca_crt    = os.path.join(certdir, 'ca.crt')
    rexecdir  = os.path.join(dir, '.rexec')
    if not os.path.isdir(rexecdir):
        os.mkdir(rexecdir)
        os.chown(rexecdir, uid, gid)
        os.chmod(rexecdir, 0700)
    user_key  = os.path.join(rexecdir, 'cli_key.pem')
    user_crs  = os.path.join(rexecdir, 'cli_req.pem')
    user_crt  = os.path.join(rexecdir, 'cli_cert.pem')
    gen_user()
    os.chown(user_key, uid, gid)
    os.chmod(user_key, 0600)
    os.chown(user_crs, uid, gid)
    os.chmod(user_crs, 0600)
    os.chown(user_crt, uid, gid)
    os.chmod(user_crt, 0644)


