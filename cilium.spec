%global debug_package %{nil}

Name: cilium
Epoch: 100
Version: 1.11.4
Release: 1%{?dist}
Summary: eBPF-based Networking, Security, and Observability
License: Apache-2.0
URL: https://github.com/cilium/cilium/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.18
BuildRequires: glibc-static

%description
Cilium is open source software for providing and transparently securing
network connectivity and loadbalancing between application workloads
such as application containers or processes. Cilium operates at Layer
3/4 to provide traditional networking and security services as well as
Layer 7 to protect and secure use of modern application protocols such
as HTTP, gRPC and Kafka. Cilium is integrated into common orchestration
frameworks such as Kubernetes.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
mkdir -p bin
set -ex && \
    export CGO_ENABLED=1 && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w" \
        -o ./bin/cilium ./cilium

%install
install -Dpm755 -d %{buildroot}%{_bindir}
install -Dpm755 -d %{buildroot}%{_prefix}/share/bash-completion/completions
install -Dpm755 -t %{buildroot}%{_bindir}/ bin/cilium
./bin/cilium completion bash > %{buildroot}%{_prefix}/share/bash-completion/completions/cilium

%files
%license LICENSE
%{_bindir}/*
%{_prefix}/share/bash-completion/completions/*

%changelog
