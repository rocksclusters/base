NAME	= foundation-mysql
VERSION = 5.6.15
RELEASE = 1
RPM.FILE.EXTRAS="%config /opt/rocks/mysql/my.cnf"
RPM.EXTRAS="%define __perl_provides  %{_builddir}/%{name}-%{version}/filter-perl-prov.sh\\n%define __perl_requires   %{_builddir}/%{name}-%{version}/filter-perl-req.sh"
RPM.SCRIPTLETS.FILE=scriptlets
