NAME	= foundation-python
CONFIGOPTS = --enable-ipv6 --enable-unicode=ucs4

ifeq ($(strip $(VERSION.MAJOR)), 5)
VERSION = 2.4.3
RELEASE = 0
ADDFLAGS = 
endif
ifeq ($(strip $(VERSION.MAJOR)), 6)
VERSION = 2.6.7
RELEASE = 0
ADDFLAGS = "CFLAGS=-fPIC"
#CONFIGOPTS += --exec-prefix=$(PKGROOT)
endif 
ifeq ($(strip $(VERSION.MAJOR)), 7)
VERSION = 2.7.5
RELEASE = 0
ADDFLAGS = "CFLAGS=-fPIC"
RPM.EXTRAS="%define _python_bytecompile_errors_terminate_build 0\\n%define __python_requires  %{_builddir}/%{name}-%{version}/filter_python_requires.sh"
#CONFIGOPTS += --exec-prefix=$(PKGROOT)
endif 
RPM.FILES = "/opt/rocks/bin/*\\n/opt/rocks/include/python2*\\n/opt/rocks/lib/lib*\\n/opt/rocks/lib/pkgconfig/*\\n/opt/rocks/lib/python2*\\n/opt/rocks/share/man/man1/*\\n/opt/rocks/usr/bin/*"
