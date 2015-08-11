NAME = rocks-devel
RELEASE = 3
RPM.EXTRAS="%define _use_internal_dependency_generator 0\\n%define __find_requires %{_builddir}/%{name}-%{version}/filter-requires.sh"
