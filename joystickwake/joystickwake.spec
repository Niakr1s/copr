%global debug_package %{nil}
%global _sourcedir %{_topdir}/SOURCES/%{name}

Name: joystickwake
Version: 1.0.0
Release: 5%{?dist}
Summary: A joystick-aware screen waker

License: GPL-3.0
URL: https://codeberg.org/forestix/joystickwake

Source0: %{name}-%{version}.tar.gz

Requires: python3-pyudev python3-dbus-fast python3-xlib

%description
joystickwake packaged for fedora

%prep
%setup -q -c

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 %{name}-%{version} %{buildroot}%{_bindir}/%{name}

%post
/usr/sbin/semanage fcontext -a -t bin_t "%{_bindir}/%{name}" 2>/dev/null || :

%files
%{_bindir}/%{name}

%changelog
%autochangelog
