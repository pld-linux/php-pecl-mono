# TODO
# - doesn't compile
# - package examples into examplesdir
%define		_modname	mono
%define		_status		beta
Summary:	Allows you to access .NET assemblies from PHP
Summary(pl):	Pozwala na dostêp do wstawek .NET w PHP
Name:		php-pecl-%{_modname}
Version:	0.7
Release:	0.2
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	23639443898018a743250a62b1873a89
URL:		http://pecl.php.net/package/mono/
BuildRequires:	mono-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Obsoletes:	php-mono
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A C extension that interfaces with the mono library to allow access to
.NET assemblies.

In PECL status of this package is: %{_status}.

%description -l pl
Rozszerzenie w C, które jest interfejsem do biblioteki mono,
pozwalaj±cym na dostêp do wstawek w .NET.

To rozszerzenie ma w PECL status: %{_status}.

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
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/examples/{*.php,*.jpg,*.gif}
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
