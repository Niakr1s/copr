%global debug_package %{nil}

Name: nvidia-pstated
Version: 1.0.9
Release: %autorelease
Summary: A daemon that automatically manages the performance states of NVIDIA GPUs.

License: GPL-3.0
URL: https://github.com/sasha0552/nvidia-pstated

BuildRequires: systemd-rpm-macros
Source0: %{name}-%{version}
Source1: %{name}.service

Requires: systemd

%description
nvidia-pstated packaged for fedora

%prep

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}

install -m 0755 %{_sourcedir}/%{name}-%{version} %{buildroot}%{_bindir}/nvidia-pstated
install -m 0644 %{_sourcedir}/%{name}.service %{buildroot}%{_unitdir}/nvidia-pstated.service

%post
/usr/bin/chcon -t bin_t %{_bindir}/nvidia-pstated
%systemd_post nvidia-pstated.service

%preun
%systemd_preun nvidia-pstated.service

%postun
%systemd_postun_with_restart nvidia-pstated.service

%files
%{_bindir}/nvidia-pstated
%{_unitdir}/nvidia-pstated.service

%changelog
%autochangelog
