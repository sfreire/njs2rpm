
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define debug_package %{nil}
%define prefix /opt/ptin
%define _prefix %{prefix}/%{name}


Name    : n2r
Version : 1.0.0
Release : 2.%{disttype}%{distnum}
Summary: N2R - convert NodeJS module to RPM
Group: Development/Libraries
License: LGPLv2+
Source: %{name}-%{version}.tar.gz
URL: https://github.com/sfreire/n2r
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch
Requires: redhat-rpm-config, tar, coreutils, wget, nodejs-packaging, nodejs-devel, npm

%description 
NodeJS module to RPM packager

%prep
%setup

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/%{_prefix}/bin
cp n2r %{buildroot}/%{_prefix}/bin
cp default.n2r  %{buildroot}/%{_prefix}/bin
ln -s %{_prefix}/bin/n2r %{buildroot}/usr/bin/n2r

%clean
rm -rf %{buildroot}

%pre

%post

%preun

%files
%defattr (0755,root,root,0755)
%dir %{_prefix}/bin
%{_prefix}/bin/*
/usr/bin/n2r

%changelog
* Wed Nov  6 2013 Sergio Freire <sergio-s-freire@ptinovacao.pt> - 1.0.0-2
- first public release, compatible with RHEL5 and RHEL6
