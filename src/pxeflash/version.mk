NAME	= pxeflash
VERSION = 1.0
RELEASE = 0
DOSBOOT = FDSTD.288
PXEIMAGE = $(NAME).img
PKGROOT = /opt/pxeflash

ifeq ($strip $(VERSION.MAJOR), 5)
MEMDISK		= /usr/lib/syslinux/memdisk
else
MEMDISK		= /usr/share/syslinux/memdisk
endif
