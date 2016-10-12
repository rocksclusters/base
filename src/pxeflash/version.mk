NAME	= pxeflash
VERSION = 1.0
RELEASE = 0
DOSBOOT = FDSTD.288
PXEIMAGE = $(NAME).img
PKGROOT = /opt/pxeflash
MEMDISK		= /usr/share/syslinux/memdisk
RPM.FILES = \
/opt/pxeflash \\n\
/tftpboot/pxelinux/*
