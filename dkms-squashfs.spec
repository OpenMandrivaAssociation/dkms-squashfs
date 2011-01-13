%define module squashfs
%define name dkms-%{module}
%define version 3.4
%define kver 2.6.27-rc4-next
%define release %mkrel 2

Summary: Squashfs compressed read-only filesystem
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{module}%{version}.tar.gz
Patch0: dkms-squashfs-name.patch
Patch1: dkms-squashfs-slab-header.patch
License: GPL
Group: System/Kernel and hardware
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Url: http://squashfs.sourceforge.net/
BuildArch: noarch
Requires(post): dkms
Requires(preun): dkms

%description
Squashfs is a compressed read-only filesystem.

%prep
%setup -q -n %{module}%{version}
mkdir -p dkms
pushd dkms
patch -t < ../kernel-patches/linux-%{kver}/%{module}%{version}-patch || [ -f %{module}.h ]
perl -pi -e 's,^#include <linux/(%{module}.*\.h)>$,#include "$1",' *.{c,h}
popd

cat > dkms/dkms.conf <<EOF
PACKAGE_NAME=%{name}
PACKAGE_VERSION=%{version}-%{release}
BUILT_MODULE_NAME[0]=%{module}3
DEST_MODULE_LOCATION[0]="/kernel/fs/%{module}"
AUTOINSTALL=yes
EOF
%patch0 -p1
%patch1 -p1

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/src/%{module}-%{version}-%{release}/
tar c -C dkms . | tar x -C %{buildroot}/usr/src/%{module}-%{version}-%{release}/

%clean
rm -rf %{buildroot}

%post
set -x
/usr/sbin/dkms --rpm_safe_upgrade add -m %{module} -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade build -m %{module} -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade install -m %{module} -v %{version}-%{release}
:

%preun
set -x
/usr/sbin/dkms --rpm_safe_upgrade remove -m %{module} -v %{version}-%{release} --all
:

%files
%defattr(-,root,root)
/usr/src/%{module}-%{version}-%{release}
