NAME		= rocks-ekv
RELEASE		= 0
FOUNDATION	= /opt/rocks

ifeq ($(strip $(VERSION.MAJOR)), 5)
LIBWRAP	=	/usr/$(LIB)/libwrap.so*
else
LIBWRAP	=	/$(LIB)/libwrap.so.*
endif

RPM.FILES = \
/rocks/bin/* \\n\
/usr/bin/* \\n\
/usr/lib64/* \\n\
/usr/sbin/* \\n\
/usr/share/terminfo/v/vt100
