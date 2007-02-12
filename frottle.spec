Summary:	Packet scheduling and QoS for wireless networks
Summary(pl.UTF-8):   Szeregowanie pakietów i QoS dla sieci bezprzewodowych
Name:		frottle
Version:	0.2.1
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/frottle/%{name}-%{version}.tar.gz
# Source0-md5:	eb18d7490fbc874fcecb1f4686f2707a
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://frottle.sourceforge.net/
BuildRequires:	iptables-devel
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Frottle (Freenet throttle) is an open source GNU GPL project to
control traffic on wireless networks. Such control eliminates the
common hidden-node effect even on large scale wireless networks.
Frottle is currently only available for Linux wireless gateways using
iptables firewalls, with plans to develop a windows client in the
future.

Frottle works by scheduling the traffic of each client, using a master
node to co-ordinate actions. This eliminates collisions, and prevents
clients with stronger signals from receiving bandwidth bias.

%description -l pl.UTF-8
Frottle (Freenet throttle) to projekt z otwartymi źródłami na licencji
GNU GPL służący do kontroli ruchu w sieciach bezprzewodowych. Kontrola
ta eliminuje popularny efekt ukrytego węzła nawet w dużych rozmiarów
sieciach bezprzewodowych. Frottle jest aktualnie dostępne tylko dla
bramek bezprzewodowych na Linuksie używających firewalli na iptables,
ale są plany stworzenia w przyszłości windowsowego klienta.

Frottle działa szeregując ruch każdego klienta, używając głównego
węzła do koordynowania akcji. Eliminuje to kolizje i zapobiega
otrzymywaniu większego pasma przez klientów z silniejszym sygnałem.

%prep
%setup -q

%build
CPPFLAGS="-I%{_includedir}/libipq"
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install frottle.conf.sample $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart >&2
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start frottle daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop >&2
	fi
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog INSTALL README
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man?/*
