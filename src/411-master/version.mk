NAME = rocks-411-master
RELEASE = 1
RPM.ARCH = noarch
RPM.FILE.EXTRAS = "%config /var/411/Files.mk"
RPM.FILES = \
/etc/411.d \\n\
/etc/rc.d/init.d/* \\n\
/opt/rocks/sbin/* \\n\
/opt/rocks/var/plugins/411 \\n\
/var/411
