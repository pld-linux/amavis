
# conditional build _with_mks32 support for mks32 i386 _only_

%include	/usr/lib/rpm/macros.perl    
Summary:	A Mail Virus Scanner
Summary(pl):	Antywirusowy skaner poczty elektronicznej
Name:		amavis
Version:	11
Release:	1
URL:		http://www.amavis.org/
Source0:	http://www.amavis.org/dist/perl/%{name}-perl-%{version}.tar.gz
%{?_with_mks32:Patch0:		amavis-perl-mks32.patch}
License:	GPL
Group:		Applications/Mail
Obsoletes:	AMaViS
BuildRequires:	autoconf >= 2.52
BuildRequires:	perl
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
Requires:	file
Requires:	sh-utils
Requires:	arc
Requires:	bzip2
Requires:	lha
Requires:	unarj
Requires:	ncompress
Requires:	unrar
Requires:	zoo
Requires:	%{_sbindir}/sendmail
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
AMaViS is a script that interfaces a mail transport agent (MTA) with
one or more virus scanners.

%description -l pl
AMaViS to skrypt po�rednicz�cy pomi�dzy agentem transferu poczty (MTA)
a jednym lub wi�cej program�w antywirusowych.

%prep
%setup -q -n %{name}-perl-%{version}
%{?_with_mks32:%patch -p1}  

%build
autoconf
%configure \
	--enable-all \
	--with-sendmail-wrapper=%{_sbindir}/sendmail \
	--with-runtime-dir=/var/spool/amavis/runtime \
	--with-virusdir=/var/spool/amavis/virusmails \
	--with-mailto="postmaster" \
	--with-amavisuser=amavis

%{__make}

gzip -9nf README* AUTHORS BUGS ChangeLog FAQ HINTS TODO doc/amavis.html

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	amavisuser=$(id -u) \
	DESTDIR=$RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%doc *.gz doc/*.gz doc/amavis.png
%attr(750,amavis,root) /var/spool/amavis

%pre
if [ -n "`id -u amavis 2>/dev/null`" ]; then
        if [ "`id -u amavis`" != "97" ]; then
                echo "Warning: user amavis haven't uid=97. Correct this before installing amavis" 1>&2
                exit 1
        fi
else
        /usr/sbin/useradd -u 97 -r -d /var/spool/amavis  -s /bin/false -c "Anti Virus Checker" -g nobody  amavis 1>&2
fi

%postun
if [ "$1" = "0" ]; then
        /usr/sbin/userdel amavis
fi

%clean
rm -rf $RPM_BUILD_ROOT
