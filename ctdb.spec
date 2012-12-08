%define name ctdb
%define version 1.13
%define release 1

Summary: Clustered TDB
Name: %name
Version: %version
Release: %release
License: GPLv3
Group: System/Cluster
URL: http://ctdb.samba.org/
Source0: http://ctdb.samba.org/packages/redhat/RHEL5/ctdb-%{version}.tar.xz
BuildRequires: autoconf >= 2.50, automake >= 1.6
Requires(pre): chkconfig mktemp psmisc coreutils sed 
Requires(pre): rpm-helper
Requires(postun): rpm-helper

# Fedora specific patch, ctdb should not be enabled by default in the runlevels
Patch1: ctdb-no_default_runlevel.patch
Patch3: 0001-Set-FD_CLOEXEC-for-epoll-file-descriptors.patch
Patch4: 0001-Fixes-for-various-issues-found-by-Coverity.patch

# Submitted to upstream for review https://lists.samba.org/archive/samba-technical/2011-September/079198.html
Patch5: 0001-IPv6-neighbor-solicit-cleanup.patch

Patch7: 0002-Add-systemd-support.patch

%description
ctdb is the clustered database used by samba

%package devel
Summary:        Development files for ctdb
Group:          Development/Other

%description devel
devel files for ctdb

%prep
%setup -q

%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch7 -p1

%build
CC="gcc"

## always run autogen.sh
./autogen.sh
export CFLAGS="$RPM_OPT_FLAGS $EXTRA -O0 -D_GNU_SOURCE" 
%configure2_5x --disable-static

make showflags
%make
perl -pi -e 's/^(Version: *)$/$1 %{version}/g' ctdb.pc

%install


%makeinstall_std

mkdir -p %{buildroot}%{_sysconfdir}/ctdb/systemd
install -m 755 config/systemd/ctdb_check_persistent_databases.pre %{buildroot}%{_sysconfdir}/ctdb/systemd
install -m 755 config/systemd/ctdb_set_ctdb_variables.post %{buildroot}%{_sysconfdir}/ctdb/systemd
install -m 755 config/systemd/ctdb_drop_all_public_ips %{buildroot}%{_sysconfdir}/ctdb/systemd
install -m 755 config/systemd/ctdb.systemd %{buildroot}%{_sysconfdir}/ctdb/systemd
mkdir -p %{buildroot}%{_unitdir}
install -m 755 config/ctdb.service %{buildroot}%{_unitdir}


perl -pi -e 's,/var/ctdb,/var/lib/ctdb,g' %{buildroot}/%{_initrddir}/%{name}
mkdir -p %{buildroot}/var/lib/ctdb
touch %{buildroot}/%{_sysconfdir}/ctdb/nodes

%post
%_post_service %{name}.service

%preun
%_preun_service %{name}.service


%files
%config(noreplace) %{_sysconfdir}/ctdb/systemd
%attr(755,root,root) %{_unitdir}/ctdb.service
%config(noreplace) %{_sysconfdir}/%{name}/nodes
%doc doc/*html

%{_sysconfdir}/ctdb/functions
%{_sysconfdir}/ctdb/events.d/
%{_sysconfdir}/ctdb/statd-callout
%{_sysconfdir}/ctdb/*.sh
%{_sbindir}/ctdbd
%{_bindir}/ctdb
%{_bindir}/ltdbtool
%{_bindir}/smnotify
#{_bindir}/ctdb_ipmux
%{_bindir}/ctdb_diagnostics
%{_bindir}/onnode
%{_bindir}/ping_pong
%{_mandir}/man1/ctdb.1.*
%{_mandir}/man1/ltdbtool.1.*
%{_mandir}/man1/ctdbd.1.*
%{_mandir}/man1/onnode.1.*
%{_mandir}/man1/ping_pong.1.*
%dir %attr(750,root,root) /var/lib/ctdb

%files devel
%{_includedir}/*.h
%{_libdir}/pkgconfig/ctdb.pc
%{_libdir}/*.a
