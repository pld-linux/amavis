%include	/usr/lib/rpm/macros.perl
%define		sub_ver	pre2
%define		_rel 1
Summary:	A Mail Virus Scanner
Summary(pl):	Antywirusowy skaner poczty elektronicznej
Name:		amavis
Version:	0.3.13
Release:	2.%{sub_ver}.%{_rel}
URL:		http://www.amavis.org/
Source0:	http://www.amavis.org/dist/perl/%{name}-%{version}%{sub_ver}.tar.gz
# Source0-md5:	2b90dba30a5ea2b73c2b348e26967f30
Source1:	%{name}-README.courier
Source2:	%{name}-acx_pthread.m4
Patch0:		%{name}-config.patch
License:	GPL
Group:		Applications/Mail
BuildRequires:	arc
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	file
BuildRequires:	lha
BuildRequires:	libtool
BuildRequires:	ncompress
BuildRequires:	perl-Archive-Tar
BuildRequires:	perl-Archive-Zip
BuildRequires:	perl-Compress-Zlib
BuildRequires:	perl-Convert-TNEF
BuildRequires:	perl-Convert-UUlib
BuildRequires:	perl-MIME-tools
BuildRequires:	perl-Unix-Syslog
BuildRequires:	perl-modules
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.202
BuildRequires:	sendmail-devel
BuildRequires:	unarj
BuildRequires:	unrar
BuildRequires:	unzip
BuildRequires:	zoo
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	arc
Requires:	bzip2
Requires:	file
Requires:	lha
Requires:	ncompress
Requires:	sh-utils
Requires:	unarj
Requires:	unrar
Requires:	zoo
Provides:	group(amavis)
Provides:	user(amavis)
Obsoletes:	AMaViS
Obsoletes:	amavisd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
AMaViS is a script that interfaces a mail transport agent (MTA) with
one or more virus scanners.

%description -l pl
AMaViS to skrypt po¶rednicz±cy pomiêdzy agentem transferu poczty (MTA)
a jednym lub wiêcej programów antywirusowych.

%package courier
Summary:	A Mail Virus Scanner - courier backend
Summary(pl):	Antywirusowy skaner poczty elektronicznej - backend dla couriera
Group:		Applications/Mail
Requires:	amavis = %{version}-%{release}
Requires:	courier
Provides:	amavis-courier

%description courier
AMaViS is a script that interfaces a mail transport agent (MTA) with
one or more virus scanners. This package contains backend for courier.

%description courier -l pl
AMaViS to skrypt po¶rednicz±cy pomiêdzy agentem transferu poczty (MTA)
a jednym lub wiêcej programów antywirusowych.

%prep
%setup -q -n %{name}-%{version}%{sub_ver}
%patch0 -p1
install -d m4
install %{SOURCE2} m4/acx_pthread.m4

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--enable-all \
	--with-sendmail-wrapper=%{_sbindir}/sendmail \
	--with-runtime-dir=/var/spool/amavis/runtime \
	--with-virusdir=/var/spool/amavis/virusmails \
	--with-mailto="postmaster" \
	--enable-courier \
	--with-amavisuser=amavis \
	--with-perl=%{__perl}

%{__make}

cp amavis/amavis amavis/amavis.courier

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	amavisuser=$(id -u) \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} ./README.courier
install amavis/amavis.courier $RPM_BUILD_ROOT%{_sbindir}
install amavis/amavis.conf $RPM_BUILD_ROOT%{_sysconfdir}/amavis.conf

# remove unneccessary files
rm -f $RPM_BUILD_ROOT%{_sbindir}/amavis

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 116 -r -f amavis
%useradd -u 97 -r -d /var/spool/amavis -s /bin/false -c "Anti Virus Checker" -g nobody amavis

%postun
if [ "$1" = "0" ]; then
	%userremove amavis
	%groupremove amavis
fi

%files
%defattr(644,root,root,755)
%doc README README.scanners AUTHORS BUGS ChangeLog FAQ TODO doc/amavis.html doc/amavis.png
%attr(751,amavis,amavis) %dir /var/spool/amavis
%attr(753,amavis,amavis) %dir /var/spool/amavis/runtime
%attr(753,amavis,amavis) %dir /var/spool/amavis/virusmails
%attr(644,amavis,amavis) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/amavis.conf

%files courier
%defattr(644,root,root,755)
%doc README.courier
%attr(755,root,root) %{_sbindir}/amavis.courier
