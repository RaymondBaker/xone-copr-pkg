%if 0%{?fedora}
%global buildforkernels akmod
%endif
%global debug_package %{nil}

%global commit 29033e16226bea4458b53fffc6177b95f6907f26
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global prjname xone

Name:           %{prjname}-kmod
Summary:        Kernel module (kmod) for %{prjname}
Version:        0.3.0
Release:        11%{?dist}
Epoch:          1
License:        GPLv2+


URL:            https://github.com/dlundqvist/xone
Source0:        %{url}/archive/%{commit}/%{prjname}-%{commit}.tar.gz

BuildRequires:  gcc
BuildRequires:  elfutils-libelf-devel
BuildRequires:  kmodtool

Requires:       lpf-xone-firmware

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{prjname} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
xone is a Linux kernel driver for Xbox One and Xbox Series X|S accessories.
It serves as a modern replacement for xpad, aiming to be compatible with
Microsoft's Game Input Protocol (GIP).

This package contains the kmod module for %{prjname}.

%prep
%{?kmodtool_check}


# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --kmodname %{prjname} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c

for kernel_version  in %{?kernel_versions} ; do
  cp -a xone-%{commit} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
  make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} VERSION=v%{version} modules
done

%install
for kernel_version in %{?kernel_versions}; do
    mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    install -D -m 755 _kmod_build_${kernel_version%%___*}/*.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/*.ko
done

%{?akmod_install}


%changelog

* Thu Oct 02 2025 Jan200101 <raymond_baker@hotmail.com> - 1:0.3.0-12
- Update to V0.4.5

* Wed Aug 06 2025 Jan200101 <raymond_baker@hotmail.com> - 1:0.3.0-11
- Update to V0.4.1

* Sat Mar 29 2025 Jan200101 <raymond_baker@hotmail.com> - 1:0.3.0-10
- fix package

* Thu Mar 27 2025 Jan200101 <raymond_baker@hotmail.com> - 1:0.3.0-9
- move to dlundqvist fork

* Wed Nov 27 2024 Jan200101 <sentrycraft123@gmail.com> - 1:0.3.0-7
- split kernel module into separate package

