Name: %{_cross_os}hwloc
Version: 2.12.2
Release: 1%{?dist}
Summary: Portable Hardware Locality (hwloc)
License: BSD-3-Clause
URL: https://www.open-mpi.org/projects/hwloc/
Source0: https://download.open-mpi.org/release/hwloc/v2.12/hwloc-%{version}.tar.bz2

BuildRequires: %{_cross_os}glibc-devel
Requires: %{_cross_os}glibc

%description
%{summary}.

%package devel
Summary: Files for development using hwloc
Requires: %{name}

%description devel
%{summary}.

%prep
%autosetup -n hwloc-%{version} -p1

%build
%cross_configure     --enable-static     --disable-shared     --disable-doxygen     --disable-pci     --disable-opencl     --disable-cuda     --disable-nvml     --disable-gl     --disable-libudev     --disable-libxml2     --exec-prefix=%{_cross_prefix}     --program-prefix=""

%force_disable_rpath

%make_build

%install
%make_install

%files
%license COPYING
%{_cross_attribution_file}
%{_cross_bindir}/hwloc-annotate
%{_cross_bindir}/hwloc-compress-dir
%{_cross_bindir}/hwloc-gather-topology
%{_cross_bindir}/hwloc-ls
%{_cross_bindir}/hwloc-ps
%{_cross_bindir}/hwloc-bind
%{_cross_bindir}/hwloc-calc
%{_cross_bindir}/hwloc-diff
%{_cross_bindir}/hwloc-distrib
%{_cross_bindir}/hwloc-info
%{_cross_bindir}/hwloc-patch
%{_cross_bindir}/lstopo-no-graphics
%exclude %{_cross_bindir}/lstopo
# These are not on aarch64
%if "%{_cross_arch}" == "x86_64"
%{_cross_sbindir}/hwloc-dump-hwdata
%{_cross_bindir}/hwloc-gather-cpuid
%endif
%exclude %{_cross_datadir}
%exclude %{_cross_mandir}

%files devel
%{_cross_libdir}/libhwloc.a
%{_cross_includedir}/hwloc.h
%{_cross_includedir}/hwloc/*.h
%{_cross_includedir}/hwloc/autogen/*.h
%{_cross_pkgconfigdir}/*.pc
