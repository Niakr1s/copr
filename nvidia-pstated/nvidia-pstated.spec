%global debug_package %{nil}
%global _sourcedir %{_topdir}/SOURCES/%{name}

Name: nvidia-pstated
Version: 1.0.9
Release: 5%{?dist}
Summary: A daemon that automatically manages the performance states of NVIDIA GPUs.

License: GPL-3.0
URL: https://github.com/sasha0552/nvidia-pstated

BuildRequires: systemd-rpm-macros

Source0: %{name}-%{version}
Source1: %{name}@.service

Requires: systemd

%description
nvidia-pstated packaged for fedora

%prep

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}

install -m 0755 %{SOURCE0} %{buildroot}%{_bindir}/%{name}
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}@.service

%post
/usr/sbin/semanage fcontext -a -t bin_t "%{_bindir}/%{name}" 2>/dev/null || :
%systemd_post %{name}@.service

%preun
%systemd_preun %{name}@.service

%postun
%systemd_postun_with_restart %{name}@.service

%files
%{_bindir}/%{name}
%{_unitdir}/%{name}@.service

%changelog
%autochangelog
