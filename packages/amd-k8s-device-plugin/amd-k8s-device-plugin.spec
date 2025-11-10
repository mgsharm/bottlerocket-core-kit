%global goproject github.com/ROCm
%global gorepo k8s-device-plugin
%global goimport %{goproject}/%{gorepo}

%global gover 1.31.0.8.mgsharm.norocm
%global rpmver %{gover}

Name: %{_cross_os}amd-k8s-device-plugin
Version: %{rpmver}
Release: 1%{?dist}
Summary: Kubernetes device plugin for AMD GPUs (modified for non-ROCm GPUs)
License: Apache-2.0
URL: https://github.com/ROCm/k8s-device-plugin

# Use local modified source instead of upstream
Source0: k8s-device-plugin-local.tar.gz
Source1: amd-k8s-device-plugin.service

BuildRequires: %{_cross_os}glibc-devel
BuildRequires: %{_cross_os}libdrm-devel
BuildRequires: %{_cross_os}hwloc-devel
Requires: %{name}(binaries)
Requires: %{_cross_os}libdrm
Requires: %{_cross_os}hwloc

%description
%{summary}. Modified to work with non-ROCm AMD GPUs like Radeon Pro V520.

%package bin
Summary: Kubernetes device plugin for AMD GPUs binaries
Provides: %{name}(binaries)
Requires: (%{_cross_os}image-feature(no-fips) and %{name})
Conflicts: (%{_cross_os}image-feature(fips) or %{name}-fips-bin)

%description bin
%{summary}.

%package fips-bin
Summary: Kubernetes device plugin for AMD GPUs binaries, FIPS edition
Provides: %{name}(binaries)
Requires: (%{_cross_os}image-feature(fips) and %{name})
Conflicts: (%{_cross_os}image-feature(no-fips) or %{name}-bin)

%description fips-bin
%{summary}.

%prep
%autosetup -n k8s-device-plugin -p1
%cross_go_setup k8s-device-plugin %{goproject} %{goimport}

%build
%ifarch x86_64
%cross_go_configure %{goimport}
export CGO_LDFLAGS="-Wl,-z,relro -Wl,-z,now"
export GOLDFLAGS="-compressdwarf=false -linkmode=external -extldflags ${CGO_LDFLAGS}"

go build -ldflags= -o amd-device-plugin ./cmd/k8s-device-plugin/
gofips build -ldflags= -o fips/amd-device-plugin ./cmd/k8s-device-plugin/
%endif

%install
%ifarch x86_64
install -d %{buildroot}%{_cross_bindir}
install -p -m 0755 amd-device-plugin %{buildroot}%{_cross_bindir}

install -d %{buildroot}%{_cross_fips_bindir}
install -p -m 0755 fips/amd-device-plugin %{buildroot}%{_cross_fips_bindir}

install -d %{buildroot}%{_cross_unitdir}
install -p -m 0644 %{S:1} %{buildroot}%{_cross_unitdir}
%endif

%files
%license LICENSE
%{_cross_attribution_file}
%{_cross_unitdir}/amd-k8s-device-plugin.service

%files bin
%{_cross_bindir}/amd-device-plugin

%files fips-bin
%{_cross_fips_bindir}/amd-device-plugin
