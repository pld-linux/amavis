%include	/usr/lib/rpm/macros.perl
%define		sub_ver	pre2

Summary:	A Mail Virus Scanner
Summary(pl):	Antywirusowy skaner poczty elektronicznej
Name:		amavis
Version:	0.3.13%{sub_ver}
Release:	0.1
URL:		http://www.amavis.org/
Source0:	http://www.amavis.org/dist/perl/%{name}-%{version}.tar.gz
# Source0-md5:	2b90dba30a5ea2b73c2b348e26967f30
Source1:	amavis-README.courier
License:	GPL
Group:		Applications/Mail
Obsoletes:	AMaViS
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	perl-modules
BuildRequires:	perl-Convert-UUlib
BuildRequires:	perl-Convert-TNEF
BuildRequires:	perl-Unix-Syslog
BuildRequires:	perl-Archive-Tar
BuildRequires:	perl-Archive-Zip
BuildRequires:	perl-Compress-Zlib
BuildRequires:	perl-MIME-tools
BuildRequires:	file
BuildRequires:	sh-utils
BuildRequires:	arc
BuildRequires:	bzip2
BuildRequires:	lha
BuildRequires:	unarj
BuildRequires:	ncompress
BuildRequires:	unrar
BuildRequires:	zoo
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
Requires:	file
Requires:	sh-utils
Requires:	arc
Requires:	bzip2
Requires:	lha
Requires:	unarj
Requires:	ncompress
Requires:	unrar
Requires:	zoo
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
%setup -q

%build
#%{__aclocal}
#%{__autoconf}
#%{__automake}
%configure2_13 \
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

install %{SOURCE1} ./README.courier
install amavis/amavis.courier $RPM_BUILD_ROOT%{_sbindir}

# remove unneccessary files
rm -f %{_sbindir}/amavis

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`id -u amavis 2>/dev/null`" ]; then
	if [ "`id -u amavis`" != "97" ]; then
		echo "Error: user amavis doesn't have uid=97. Correct this before installing amavis." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 97 -r -d /var/spool/amavis  -s /bin/false -c "Anti Virus Checker" -g nobody  amavis 1>&2
fi

%postun
if [ "$1" = "0" ]; then
	/usr/sbin/userdel amavis
fi

%files
%defattr(644,root,root,755)
%doc README README.scanners AUTHORS BUGS ChangeLog FAQ TODO doc/amavis.html doc/amavis.png
%attr(750,amavis,root) /var/spool/amavis

%files courier
%defattr(644,root,root,755)
%doc README.courier
%attr(755,root,root) %{_sbindir}/amavis.courier
