Summary:	A Mail Virus Scanner
Name:		amavis
Version:	0.2.1
Release:	1
URL:		http://www.amavis.org
Source0:	http://www.amavis.org/dist/%{name}-%{version}.tar.gz
Patch0:		%{name}-AVP-opt.patch
License:	GPL
Group:		Applications/Mail
Group(de):	Applikationen/Post
Group(pl):	Aplikacje/Poczta
Group(pt):	Aplicações/Correio Eletrônico
Obsoletes:	AMaViS
Requires:	%{_sbindir}/sendmail
#Requires:	/usr/local/AvpLinux/AvpLinux
BuildRequires:	%{_sbindir}/sendmail
#BuildRequires:	/usr/local/AvpLinux/AvpLinux
BuildRequires:	maildrop
BuildRequires:	tnef
# does it really needed for build?
BuildRequires:	unrar
BuildRequires:	unzip
BuildRequires:	sharutils
BuildRequires:	qmail
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Mail Virus Scanner for Linux and other UN*X based platforms.

%prep
%setup -q
#%patch0 -p1

%build
#touch depcomp
#autoconf
#automake
%configure --enable-sendmail=%{_sbindir}/sendmail \
	--with-virusdir=/var/spool/virus
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/securetar
%attr(755,root,root) %{_bindir}/zipsecure
%attr(755,root,root) %{_sbindir}/scanmails
%doc AUTHORS COPYING README* BUGS FAQ
%doc doc/amavis.html doc/amavis.txt doc/amavis.gif

%clean
rm -rf $RPM_BUILD_ROOT
