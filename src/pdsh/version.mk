PKGROOT		= /opt
NAME    	= pdsh
VERSION 	= 2.26
RELEASE 	= 1
TARBALL_POSTFIX	= tar.bz2
RPM.FILES 	= \
/etc/ld.so.conf.d/* \\n \
/etc/profile.d/* \\n \
/opt/pdsh
RPM.DESCRIPTION = \
pdsh is  a multithreaded remote shell client which executes commands on \\n\
multiple remote hosts in parallel.  Pdsh can use several different \\n\
remote shell services, including standard "rsh", Kerberos IV, and ssh.

