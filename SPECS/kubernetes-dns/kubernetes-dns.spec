Summary:        Kubernetes DNS
Name:           kubernetes-dns
Version:        1.14.8
Release:        11%{?dist}
License:        ASL 2.0
URL:            https://github.com/kubernetes/dns/archive/%{version}.tar.gz
Source0:        kubernetes-dns-%{version}.tar.gz
%define sha1    kubernetes-dns-%{version}.tar.gz=cad22fbc8499901262dfea3da504eabb7f616129
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go

%description
Kubernetes DNS is a name lookup service for kubernetes pods.

%prep -p exit
%autosetup -n dns-%{version}

%build
%ifarch x86_64
export ARCH=amd64
%endif
%ifarch aarch64
export ARCH=arm64
%endif
export VERSION=%{version}
export PKG=k8s.io/dns
export GOARCH=${ARCH}
export GOHOSTARCH=${ARCH}
export GOOS=linux
export GOHOSTOS=linux
export GOROOT=/usr/lib/golang
export GOPATH=/usr/share/gocode
export GO111MODULE=auto
export CGO_ENABLED=0
mkdir -p ${GOPATH}/src/${PKG}
cp -r * ${GOPATH}/src/${PKG}/
pushd ${GOPATH}/src/${PKG}
ARCH=${ARCH} VERSION=${VERSION} PKG=${PKG} go install \
    -installsuffix "static" \
    -ldflags "-X ${PKG}/pkg/version.VERSION=${VERSION}" \
    ./...

%install
install -m 755 -d %{buildroot}%{_bindir}
binaries=(dnsmasq-nanny e2e kube-dns sidecar sidecar-e2e)
for bin in "${binaries[@]}"; do
  echo "+++ INSTALLING ${bin}"
  install -pm 755 -t %{buildroot}%{_bindir} ${GOPATH}/bin/${bin}
done

%check
export ARCH=amd64
export VERSION=%{version}
export PKG=k8s.io/dns
export GOPATH=/usr/share/gocode
pushd ${GOPATH}/src/${PKG}
./build/test.sh cmd pkg

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/dnsmasq-nanny
%{_bindir}/e2e
%{_bindir}/kube-dns
%{_bindir}/sidecar
%{_bindir}/sidecar-e2e

%changelog
*   Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 1.14.8-11
-   Bump up version to compile with new go
*   Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.14.8-10
-   Bump up version to compile with new go
*   Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 1.14.8-9
-   Bump up version to compile with new go
*   Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.14.8-8
-   Bump up version to compile with new go
*   Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 1.14.8-7
-   Bump up version to compile with new go
*   Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.14.8-6
-   Bump up version to compile with new go
*   Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 1.14.8-5
-   Bump up version to compile with new go
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.14.8-4
-   Bump up version to compile with go 1.13.3-2
*   Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.14.8-3
-   Bump up version to compile with go 1.13.3
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.14.8-2
-   Bump up version to compile with new go
*   Fri May 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.14.8-1
-   kubernetes-dns 1.14.8.
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.14.6-3
-   Aarch64 support
*   Wed Nov 01 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.14.6-2
-   Remove go testing framework binary.
*   Mon Oct 02 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.14.6-1
-   kubernetes-dns 1.14.6.
*   Mon Sep 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.14.4-1
-   kubernetes-dns 1.14.4.
*   Wed Jun 28 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.14.2-1
-   kubernetes-dns for PhotonOS.
