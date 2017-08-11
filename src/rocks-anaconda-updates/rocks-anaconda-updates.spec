Summary: rocks-anaconda-updates
Name: rocks-anaconda-updates
Version: 7.0
Release: 2
License: University of California
Vendor: Rocks Clusters
Group: System Environment/Base
Source: rocks-anaconda-updates-7.0.tar.gz
Buildroot: /export/home/repositories/rocks/src/roll/base/src/rocks-anaconda-updates/rocks-anaconda-updates.buildroot




%description
rocks-anaconda-updates
%prep
%setup
%build
printf "\n\n\n### build ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/base/src/rocks-anaconda-updates/rocks-anaconda-updates.buildroot make -f /export/home/repositories/rocks/src/roll/base/src/rocks-anaconda-updates/rocks-anaconda-updates.spec.mk build
%install
printf "\n\n\n### install ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/base/src/rocks-anaconda-updates/rocks-anaconda-updates.buildroot make -f /export/home/repositories/rocks/src/roll/base/src/rocks-anaconda-updates/rocks-anaconda-updates.spec.mk install
%files 
/RedHat/base/*

