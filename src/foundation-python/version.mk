NAME	= foundation-python
CONFIGOPTS = --enable-ipv6 --enable-unicode=ucs4

ifeq ($(strip $(VERSION.MAJOR)), 5)
VERSION = 2.4.3
RELEASE = 0
ADDFLAGS = 
else
VERSION = 2.6.7
RELEASE = 0
ADDFLAGS = "CFLAGS=-fPIC"
#CONFIGOPTS += --exec-prefix=$(PKGROOT)
RPM.EXTRAS="%define _python_bytecompile_errors_terminate_build 0\\n%define __python_requires  %{_builddir}/%{name}-%{version}/filter_python_requires.sh"
endif 
