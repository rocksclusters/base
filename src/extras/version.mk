NAME		= rocks-extras
RELEASE		= 0

MAKE.iscontrib  = 1

DISTPATH	= $(shell rocks-dist --path=dist.getRPMSPath paths)
OS_VERSION	= $(shell mysql --batch --execute='select version from rolls where name="os" and enabled="yes"' -u apache cluster | grep -v version)

