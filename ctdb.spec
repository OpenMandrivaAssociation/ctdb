%define name ctdb
%define version 1.0
%define release %mkrel 5
%define initdir %{_sysconfdir}/init.d

Summary	: Clustered TDB
Name	: %name
Version	: %version
Release	: %release
License	: GPL
Group	: System/Cluster
URL	: http://ctdb.samba.org/
Source  : %{name}-%{version}.tar.gz
BuildRequires: autoconf >= 2.50, automake >= 1.6
Requires(pre): chkconfig mktemp psmisc coreutils sed 
Requires(pre,postun): rpm-helper
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
ctdb is the clustered database used by samba

%package devel
Summary:        Development files for ctdb
Group:          Development/Other

%description devel
devel files for ctdb
#######################################################################
%prep
%setup -q

%build
CC="gcc"

## always run autogen.sh
./autogen.sh
export CFLAGS="$RPM_OPT_FLAGS $EXTRA -O0 -D_GNU_SOURCE" 
%configure

make showflags
make   

%install
# Clean up in case there is trash left from a previous build
rm -rf $RPM_BUILD_ROOT

# Create the target build directory hierarchy
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/init.d

make DESTDIR=$RPM_BUILD_ROOT install

install -m644 config/ctdb.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ctdb
install -m755 config/ctdb.init $RPM_BUILD_ROOT%{initdir}/ctdb

# Remove "*.old" files
find $RPM_BUILD_ROOT -name "*.old" -exec rm -f {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service %{name}

%preun
%_preun_service %{name}


#######################################################################
## Files section                                                     ##
#######################################################################

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/sysconfig/ctdb
%attr(755,root,root) %{initdir}/ctdb
%doc doc/*html

%{_sysconfdir}/ctdb/functions
%{_sysconfdir}/ctdb/events.d/README
%{_sysconfdir}/ctdb/events.d/00.ctdb
%{_sysconfdir}/ctdb/events.d/10.interface
%{_sysconfdir}/ctdb/events.d/40.vsftpd
%{_sysconfdir}/ctdb/events.d/41.httpd
%{_sysconfdir}/ctdb/events.d/50.samba
%{_sysconfdir}/ctdb/events.d/60.nfs
%{_sysconfdir}/ctdb/events.d/61.nfstickle
%{_sysconfdir}/ctdb/events.d/70.iscsi
%{_sysconfdir}/ctdb/events.d/90.ipmux
%{_sysconfdir}/ctdb/events.d/91.lvs
%{_sysconfdir}/ctdb/statd-callout
%{_sbindir}/ctdbd
%{_bindir}/ctdb
%{_bindir}/smnotify
%{_bindir}/ctdb_ipmux
%{_bindir}/ctdb_diagnostics
%{_bindir}/onnode.ssh
%{_bindir}/onnode.rsh
%{_bindir}/onnode
%{_mandir}/man1/ctdb.1.*
%{_mandir}/man1/ctdbd.1.*
%{_mandir}/man1/onnode.1.*

%files devel
%{_includedir}/ctdb.h
%{_includedir}/ctdb_private.h

%changelog
