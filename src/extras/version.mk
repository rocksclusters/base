NAME		= rocks-extras
RELEASE		= 0

MAKE.iscontrib  = 1

#DISTPATH	= $(shell rocks-dist --path=dist.getRPMSPath paths)
DISTPATH	= rocks-dist/$(ARCH)/RedHat/RPMS
OS_VERSION	= $(shell mysql --batch --execute='select version from rolls where name="os" and enabled="yes"' -u apache cluster | grep -v version)


ifeq ($(strip $(VERSION.MAJOR)), 5)
CACHENAMED	= caching-nameserver
else
CACHENAMED	= bind-chroot
endif
