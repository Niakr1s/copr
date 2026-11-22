%global debug_package %{nil}
%global __provides_exclude_from ^%{_libdir}/%{name}/.*\\.so.*$
%global __requires_exclude ^lib(llama|ggml|mtmd).*\\.so.*$
%global bin_prefix cmpfix

Name:           llama-cpp-cmpfix
Version:        1.0.0
Release:        1%{?dist}
Summary:        llama.cpp CUDA inference server, CLI, and libraries, with fixes for NVIDIA CMP cards

License:        MIT
URL:            https://github.com/ggml-org/llama.cpp

Source0:        %{name}-%{version}.tar.gz

# each update you should bump this tag (get it from https://github.com/ggml-org/llama.cpp/releases/download/v1.0.0/nightly-tag.txt)
%global nightly b12359
Source1:        %{url}/releases/download/%{nightly}/llama-%{nightly}-ui.tar.gz

# Build-time only
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  git
BuildRequires:  openssl-devel
BuildRequires:  cuda-toolkit

# Runtime only
Requires:       cuda-toolkit

%description
llama.cpp built with the CUDA backend, with DP4A disabled, that makes inference
faster on mining GPUs (like CMP 50HX and similar), providing the
cmpfix-llama-server HTTP server, the cmpfix-llama-cli command-line tool,
and all required shared libraries.

%prep
%setup -q -n llama.cpp-%{version}
mkdir tools/ui/dist
tar -xzf %{SOURCE1} -C tools/ui/dist --strip-components=1

%build
export PATH="/usr/local/cuda/bin:$PATH"
export CUDACXX="/usr/local/cuda/bin/nvcc"

cmake -B build -DGGML_CUDA=ON \
  -DLLAMA_BUILD_TESTS=OFF \
  -DLLAMA_USE_PREBUILT_UI=OFF \
  -DCMAKE_EXE_LINKER_FLAGS="-no-pie" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_CUDA_ARCHITECTURES="75;80;86;89;120" \
  -DCMAKE_CUDA_FLAGS="-DDISABLE_DP4A --fmad=false" \
  -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON \
  -DCMAKE_INSTALL_RPATH='$ORIGIN'
cmake --build build -j"$(nproc)"

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/%{name}
mkdir -p %{buildroot}%{_userunitdir}

cp -a build/bin/lib*.so* %{buildroot}%{_libdir}/%{name}/

for bin in llama-server llama-cli llama-bench llama-quantize llama-mtmd-cli; do
    install -m 0755 "build/bin/$bin" "%{buildroot}%{_libdir}/%{name}/$bin"
    ln -s "%{_libdir}/%{name}/$bin" "%{buildroot}%{_bindir}/%{bin_prefix}-$bin"
done

%files
%license LICENSE
%{_bindir}/%{bin_prefix}-llama-server
%{_bindir}/%{bin_prefix}-llama-cli
%{_bindir}/%{bin_prefix}-llama-bench
%{_bindir}/%{bin_prefix}-llama-quantize
%{_bindir}/%{bin_prefix}-llama-mtmd-cli
%{_libdir}/%{name}/

%changelog
%autochangelog
