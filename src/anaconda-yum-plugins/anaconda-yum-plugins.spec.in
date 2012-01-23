Summary: Installation-related yum plugins
Name:    anaconda-yum-plugins
Epoch:   1
Version: 1.0
Release: 5.1%{?dist}
License: GPLv2+
Group:   Applications/System
URL:     http://fedoraproject.org/wiki/Anaconda

Source0: %{name}-%{version}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires:  python, yum

%description
The anaconda yum-plugins package contains yum plugins that are useful for
anaconda and other system installation-related programs.

%prep
%setup -q

%build
# noop

%install
%{__rm} -rf %{buildroot}
# RPM will take care of the python-compiling stuff
%{__make} install DESTDIR=%{buildroot} NO_PY_COMPILE=1

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/*
%{_prefix}/lib/yum-plugins/*

%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1:1.0-5.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep 19 2008 David Cantrell <dcantrell@redhat.com> 1:1.0-3
- Need epoch increased since version is back to 1.0, but it was previously
  the same as the anaconda version number.  jkeating and wwoods said to do
  this too, so blame them.

* Thu Sep 18 2008 Chris Lumens <clumens@redhat.com> 1.0-2
- Include the distro tag in the release number.

* Mon Sep 15 2008 Will Woods <wwoods@redhat.com> - 1.0-1
- Initial packaging (moved out of anaconda package)
