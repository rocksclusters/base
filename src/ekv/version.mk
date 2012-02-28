NAME		= rocks-ekv
RELEASE		= 0
FOUNDATION	= /opt/rocks

ifeq ($(strip $(VERSION.MAJOR)), 5)
LIBWRAP	=	/usr/$(LIB)/libwrap.so*
else
LIBWRAP	=	/$(LIB)/libwrap.so.*
endif
