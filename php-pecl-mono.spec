# TODO
# - doesn't compile
#  - php-pecl-mono-0.7/mono-0.7/php_mono.c:33:37: mono/metadata/tabledefs.h: No such file or directory
#  - add missing -I: php52-pecl-mono-0.7/php_mono.h:25:26: fatal error: mono/jit/jit.h: No such file or directory
# - package examples into examplesdir
%define		php_name	php%{?php_suffix}
%define		modname	mono
%define		status		beta
Summary:	%{modname} - allows you to access .NET assemblies from PHP
Summary(pl.UTF-8):	%{modname} - pozwala na dostęp do wstawek .NET w PHP
Name:		%{php_name}-pecl-%{modname}
Version:	0.7
Release:	0.2
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	23639443898018a743250a62b1873a89
URL:		http://pecl.php.net/package/mono/
BuildRequires:	mono-devel
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Obsoletes:	php-mono
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A C extension that interfaces with the mono library to allow access to
.NET assemblies.

In PECL status of this package is: %{status}.

%description -l pl.UTF-8
Rozszerzenie w C, które jest interfejsem do biblioteki mono,
pozwalającym na dostęp do wstawek w .NET.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure \
	--with-%{modname}

%{__make} \
	CPPFLAGS="-DHAVE_CONFIG_H -I/usr/X11R6/include/X11/" \
	CFLAGS_CLEAN="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
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
%doc examples/{*.php,*.jpg,*.gif}
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
