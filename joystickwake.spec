%global debug_package %{nil}

Name: joystickwake
Version: 1.0.0
Release: 3%{?dist}
Summary: A joystick-aware screen waker

License: GPL-3.0
URL: https://codeberg.org/forestix/joystickwake

BuildRequires: systemd-rpm-macros

# For user/group creation
BuildRequires: shadow-utils
Requires(post): shadow-utils
Requires(preun): shadow-utils

Source0: %{name}-%{version}
Source1: %{name}.service

Requires: systemd
Requires: python3-pyudev python3-dbus-fast python3-xlib

%description
joystickwake packaged for fedora

%pre
# Create the system group and user if they don't already exist
getent group joystickwake >/dev/null || groupadd -r joystickwake
getent passwd joystickwake >/dev/null || useradd -r -g joystickwake -s /sbin/nologin -M joystickwake

%prep

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}

install -m 0755 %{_sourcedir}/%{name}-%{version} %{buildroot}%{_bindir}/joystickwake
install -m 0644 %{_sourcedir}/%{name}.service %{buildroot}%{_unitdir}/joystickwake.service

%post
/usr/sbin/semanage fcontext -a -t bin_t "%{_bindir}/joystickwake" 2>/dev/null || :
%systemd_post joystickwake.service
# Add the service user to the 'input' group so it can read joystick devices
usermod -a -G input joystickwake

%preun
%systemd_preun joystickwake.service
userdel joystickwake &>/dev/null || :
groupdel joystickwake &>/dev/null || :

%postun
%systemd_postun_with_restart joystickwake.service

%files
%{_bindir}/joystickwake
%{_unitdir}/joystickwake.service

%changelog
%autochangelog
