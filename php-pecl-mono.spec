%define		_modname	mono
%define		_status		beta
Summary:	Allows you to access .NET assemblies from PHP
Summary(pl):	Pozwala na dostêp do wstawek .NET w PHP
Name:		php-pecl-%{_modname}
Version:	0.7
Release:	0.1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pear.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	23639443898018a743250a62b1873a89
URL:		http://pear.php.net/package/mono/
BuildRequires:	php-devel
BuildRequires:	mono-devel
Requires:	php-common
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
A C extension that interfaces with the mono library to allow access to
.NET assemblies.

This extension has in PEAR status: %{_status}.

%description -l pl
Rozszerzenie w C, które jest interfejsem do biblioteki mono,
pozwalaj±cym na dostêp do wstawek w .NET.

To rozszerzenie ma w PEAR status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure \
	--with-%{_modname}

%{__make} \
CPPFLAGS="-DHAVE_CONFIG_H -I%{_prefix}/X11R6/include/X11/" \
	CFLAGS_CLEAN="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php-module-install install %{_modname} %{_sysconfdir}/php.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove %{_modname} %{_sysconfdir}/php.ini
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/examples/{*.php,*.jpg,*.gif}
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
