
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define debug_package %{nil}
%define prefix /opt/ptin
%define _prefix %{prefix}/%{name}
%define _docdir %{prefix}/%{name}/doc


Name    : njs2rpm
Version : 1.0.3
Release : 1.%{disttype}%{distnum}
Summary: NJS2RPM - convert NodeJS module to RPM
Group: Development/Libraries
License: LGPLv2+
Source: %{name}-%{version}.tar.gz
URL: https://github.com/sfreire/njs2rpm
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch
Requires: redhat-rpm-config, tar, coreutils, wget, nodejs-packaging, nodejs-devel, npm, rpm-build

%description 
NJS2RPM - convert NodeJS modules to RPM packages (by Sergio Freire)
A simple Bash script to build RPMs of any available NodeJS module, any version. It fetches the source from NPM Registry and builds the RPM. Simple, isn't it?
No more NodeJS modules installed ad-hoc using "npm".

%prep
%setup

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/%{_prefix}/bin
mkdir -p %{buildroot}/%{_docdir}
cp njs2rpm %{buildroot}/%{_prefix}/bin
cp default.n2r  %{buildroot}/%{_prefix}/bin
cp *.md LICENSE %{buildroot}/%{_docdir}
ln -s %{_prefix}/bin/njs2rpm %{buildroot}/usr/bin/njs2rpm

%clean
rm -rf %{buildroot}

%pre

%post

%preun

%files
%defattr (0755,root,root,0755)
%dir %{_prefix}/bin
%{_prefix}/bin/*
/usr/bin/njs2rpm
%{_docdir}/README.md
%{_docdir}/LICENSE

%changelog
* Mon May 19 2014 JM Goncalves <joao-m-goncalves@telecom.pt> - 1.0.3-1
- added rpm-build to Requires
- fixed egrep multi-match in license retrieval (caused problems with MIT License)
* Tue Jan 21 2014 Sergio Freire <sergio-s-freire@ptinovacao.pt> - 1.0.2-1
- fixed issue #1 (problem with user defined _topdir)
* Thu Nov  8 2013 Sergio Freire <sergio-s-freire@ptinovacao.pt> - 1.0.1-1
- changed default template so RPM macro _rpmconfigdir points to 32 bit libs diretory. have to fix this better
- disabled debuginfo packages on default template
- avoid stderr messages of tar in RHEL5
* Thu Nov  7 2013 Sergio Freire <sergio-s-freire@ptinovacao.pt> - 1.0.0-4
- describe better the package description
- removed my email from the default template
* Thu Nov  7 2013 Sergio Freire <sergio-s-freire@ptinovacao.pt> - 1.0.0-3
- change name from n2r to njs2rpm
- included LICENSE
* Wed Nov  6 2013 Sergio Freire <sergio-s-freire@ptinovacao.pt> - 1.0.0-2
- first public release, compatible with RHEL5 and RHEL6
