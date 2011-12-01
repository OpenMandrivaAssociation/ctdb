%define name ctdb
%define version 1.0.114
%define release %mkrel 3

Summary: Clustered TDB
Name: %name
Version: %version
Release: %release
License: GPLv3
Group: System/Cluster
URL: http://ctdb.samba.org/
Source: http://ctdb.samba.org/packages/redhat/RHEL5/ctdb-%{version}.tar.gz
BuildRequires: autoconf >= 2.50, automake >= 1.6
Requires(pre): chkconfig mktemp psmisc coreutils sed 
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
ctdb is the clustered database used by samba

%package devel
Summary:        Development files for ctdb
Group:          Development/Other

%description devel
devel files for ctdb

%prep
%setup -q

%build
CC="gcc"

## always run autogen.sh
./autogen.sh
export CFLAGS="$RPM_OPT_FLAGS $EXTRA -O0 -D_GNU_SOURCE" 
%configure

make showflags
%make
perl -pi -e 's/^(Version: *)$/$1 %{version}/g' ctdb.pc

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}/%{_initrddir}

%makeinstall_std

install -m644 config/ctdb.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/ctdb
install -m755 config/ctdb.init %{buildroot}%{_initrddir}/ctdb

perl -pi -e 's,/var/ctdb,/var/lib/ctdb,g' %{buildroot}/%{_initrddir}/%{name}
mkdir -p %{buildroot}/var/lib/ctdb
touch %{buildroot}/%{_sysconfdir}/ctdb/nodes

%clean
rm -rf %{buildroot}

%post
%_post_service %{name}

%preun
%_preun_service %{name}


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/sysconfig/ctdb
%attr(755,root,root) %{_initrddir}/ctdb
%config(noreplace) %{_sysconfdir}/%{name}/nodes
%doc doc/*html

%{_sysconfdir}/ctdb/functions
%{_sysconfdir}/ctdb/events.d/
%{_sysconfdir}/ctdb/statd-callout
%{_sysconfdir}/ctdb/*.sh
%{_sbindir}/ctdbd
%{_bindir}/ctdb
%{_bindir}/smnotify
#{_bindir}/ctdb_ipmux
%{_bindir}/ctdb_diagnostics
%{_bindir}/onnode
%{_bindir}/ping_pong
%{_mandir}/man1/ctdb.1.*
%{_mandir}/man1/ctdbd.1.*
%{_mandir}/man1/onnode.1.*
%dir %attr(750,root,root) /var/lib/ctdb

%files devel
%defattr(-,root,root)
%{_includedir}/ctdb.h
%{_includedir}/ctdb_private.h
%{_libdir}/pkgconfig/ctdb.pc

%changelog
