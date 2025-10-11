Name: %{_cross_os}libdrm
Version: 2.4.123
Release: 1%{?dist}
Summary: Direct Rendering Manager runtime library
License: MIT
URL: https://dri.freedesktop.org
Source0: https://dri.freedesktop.org/libdrm/libdrm-%{version}.tar.xz

BuildRequires: %{_cross_os}glibc-devel
Requires: %{_cross_os}glibc

%description
%{summary}.

%package devel
Summary: Files for development using the direct rendering manager library
Requires: %{name}

%description devel
%{summary}.

%prep
%autosetup -n libdrm-%{version} -p1

%build
%ifarch x86_64
%cross_meson     --auto-features=disabled     -Dcairo-tests=disabled     -Dman-pages=disabled     -Dvalgrind=disabled     -Dfreedreno=disabled     -Dvc4=disabled     -Detnaviv=disabled     -Dexynos=disabled     -Dtegra=disabled     -Domap=disabled     -Dintel=disabled     -Dradeon=enabled     -Damdgpu=enabled     -Dnouveau=disabled     -Dtests=false

%cross_meson_build
%endif

%install
%ifarch x86_64
%cross_meson_install
%endif

%files
%ifarch x86_64
%license COPYING
%{_cross_attribution_file}
%{_cross_libdir}/*.so.*
%{_cross_includedir}/libsync.h
%{_cross_datadir}/libdrm/amdgpu.ids
%endif

%files devel
%ifarch x86_64
%{_cross_libdir}/*.so
%{_cross_includedir}/libdrm/
%{_cross_includedir}/xf86drm.h
%{_cross_includedir}/xf86drmMode.h
%{_cross_pkgconfigdir}/*.pc
%endif
