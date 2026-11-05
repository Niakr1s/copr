%global debug_package %{nil}

Name: joystickwake
Version: 1.0.0
Release: 4%{?dist}
Summary: A joystick-aware screen waker

License: GPL-3.0
URL: https://codeberg.org/forestix/joystickwake

%global pkg_dir joystickwake
Source0: ${pkg_dir}/%{name}-%{version}

Requires: python3-pyudev python3-dbus-fast python3-xlib

%description
joystickwake packaged for fedora

%prep

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 %{_sourcedir}/%{pkg_dir}/%{name}-%{version} %{buildroot}%{_bindir}/joystickwake

%post
/usr/sbin/semanage fcontext -a -t bin_t "%{_bindir}/joystickwake" 2>/dev/null || :

%files
%{_bindir}/joystickwake

%changelog
%autochangelog
