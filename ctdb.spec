Summary:	Clustered TDB
Name:		ctdb
Version:	2.0
Release:	1
License:	GPLv3
Group:		System/Cluster
Url:		http://ctdb.samba.org/
Source0:	http://ftp.samba.org/pub/ctdb/ctdb-%{version}.tar.gz
# Fedora specific patch, ctdb should not be enabled by default in the runlevels
Patch1: ctdb-no_default_runlevel.patch
Patch2: ctdb-2.0-linkage.patch
# Submitted to upstream for review https://lists.samba.org/archive/samba-technical/2011-September/079198.html
Patch5: 0001-IPv6-neighbor-solicit-cleanup.patch
Patch7: 0002-Add-systemd-support.patch

BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(talloc)
BuildRequires:	pkgconfig(tevent)
Requires(pre):	chkconfig mktemp psmisc coreutils sed 
Requires(pre,postun):	rpm-helper

%description
ctdb is the clustered database used by samba

%package devel
Summary: Development files for ctdb
Group: Development/Other

%description devel
devel files for ctdb

%prep
%setup -q
%apply_patches

%build
CC="%__cc"

## always run autogen.sh
./autogen.sh
export CFLAGS="$RPM_OPT_FLAGS $EXTRA -D_GNU_SOURCE" 
%configure2_5x \
	--enable-shared \
	--disable-static \
	--without-included-popt \
	--without-included-talloc \
	--without-included-tdb \
	--without-included-tevent

make showflags
%make
sed -i -e 's/^(Version: *)$/$1 %{version}/g' ctdb.pc

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
%_post_service %{name}

%preun
%_preun_service %{name}


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
