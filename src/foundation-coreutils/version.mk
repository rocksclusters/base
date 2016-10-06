NAME	= foundation-coreutils
VERSION = 8.9
ifeq ($(strip $(VERSION.MAJOR)), 7)
VERSION = 8.22
endif
RELEASE = 0
RPM.FILES = "/opt/rocks/bin/*\\n/opt/rocks/libexec/coreutils*\\n/opt/rocks/share/info/*\\n/opt/rocks/share/locale/*\\n/opt/rocks/share/man/man1/*"
