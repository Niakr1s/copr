%global debug_package %{nil}

Name: llama-cpp-cmpfix
Version: 0.6.0
Release: 1%{?dist}
Summary: llama.cpp CUDA inference server, CLI, and libraries, with fixes for nvidia cmp cards
Conflicts: llama-cpp

License: GPL-3.0
URL: https://github.com/Niakr1s/llama.cpp

# Build-time only
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  git
BuildRequires:  openssl-devel
BuildRequires:  patchelf
BuildRequires:  cuda-toolkit

# Runtime only
Requires:       cuda-toolkit

Source0: %{name}-%{version}.tar.gz

%description
llama.cpp built with the CUDA backend, with DP4A disabled, that makes inference
faster on mining GPUs (like cmp50hx and similar), providing the llama-server
HTTP server, the llama-cli command-line tool, and all required shared
libraries.

%prep
%setup -q -n llama.cpp-%{version}

%build
export PATH="/usr/local/cuda/bin:$PATH"
export CUDACXX="/usr/local/cuda/bin/nvcc"

cmake -B build -DGGML_CUDA=ON \
  -DCMAKE_EXE_LINKER_FLAGS="-no-pie" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_CUDA_ARCHITECTURES="75;80;86;89;120" \
  -DCMAKE_CUDA_FLAGS="-DDISABLE_DP4A --fmad=false" \
  -DCMAKE_INSTALL_RPATH=""
cmake --build build -j"$(nproc)"

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_libdir}

install -m 0755 build/bin/llama-server %{buildroot}%{_bindir}/llama-server
install -m 0755 build/bin/llama-cli %{buildroot}%{_bindir}/llama-cli

for lib in \
    libllama-server-impl.so \
    libllama-cli-impl.so \
    libllama-common.so \
    libmtmd.so \
    libllama.so \
    libggml.so \
    libggml-cpu.so \
    libggml-cuda.so \
    libggml-base.so ; do
    cp -a build/bin/${lib}* %{buildroot}%{_libdir}/
done

patchelf --remove-rpath %{buildroot}%{_bindir}/llama-server
patchelf --remove-rpath %{buildroot}%{_bindir}/llama-cli

for lib in %{buildroot}%{_libdir}/libllama*.so* %{buildroot}%{_libdir}/libmtmd*.so* %{buildroot}%{_libdir}/libggml*.so*; do
    patchelf --remove-rpath "$lib"
done

%post
/usr/sbin/ldconfig

for bin in llama-server llama-cli; do
  /usr/sbin/semanage fcontext -a -t bin_t "%{_bindir}/$bin" 2>/dev/null || :
  /usr/sbin/semanage fcontext -a -t bin_t "%{_bindir}/$bin" 2>/dev/null || :
done

%preun

%postun
/usr/sbin/ldconfig

%files
%{_bindir}/llama-server
%{_bindir}/llama-cli
%{_libdir}/libllama-server-impl.so*
%{_libdir}/libllama-cli-impl.so*
%{_libdir}/libllama-common.so*
%{_libdir}/libmtmd.so*
%{_libdir}/libllama.so*
%{_libdir}/libggml.so*
%{_libdir}/libggml-cpu.so*
%{_libdir}/libggml-cuda.so*
%{_libdir}/libggml-base.so*

%changelog
%autochangelog
