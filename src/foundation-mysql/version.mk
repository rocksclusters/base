NAME	= foundation-mysql
VERSION = 5.6.26
RELEASE = 1
RPM.FILE.EXTRAS="%config /opt/rocks/mysql/my.cnf"
RPM.EXTRAS="%define __perl_provides  %{_builddir}/%{name}-%{version}/filter-perl-prov.sh\\n%define __perl_requires   %{_builddir}/%{name}-%{version}/filter-perl-req.sh\\n%define __perllib_requires %{_builddir}/%{name}-%{version}/filter-perl-req.sh"
RPM.SCRIPTLETS.FILE=scriptlets
RPM.FILESLIST=filelist
