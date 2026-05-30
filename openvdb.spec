%define major 13
%define libname %mklibname openvdb
%define devname %mklibname openvdb -d

%bcond ax 1
%bcond docs 1
%bcond imath 1
%bcond nanovdb 1
%bcond openexr 1
%bcond python 1
%bcond tests 1

Name:		openvdb
Version:	13.0.0
Release:	1
Summary:	Sparse volume data structure and tools
License:	Apache-2.0
Group:		System/Libraries
URL:		https://www.openvdb.org/
# upstream repo: https://github.com/AcademySoftwareFoundation/openvdb
Source0:	https://github.com/AcademySoftwareFoundation/openvdb/archive/v%{version}/%{name}-%{version}.tar.gz
Source100:	%{name}.rpmlintrc

BuildSystem:	cmake
BuildOption:	-DCMAKE_NO_SYSTEM_FROM_IMPORTED=TRUE
BuildOption:	-DDISABLE_DEPENDENCY_VERSION_CHECKS=ON
BuildOption:	-DOPENVDB_BUILD_UNITTESTS=OFF
BuildOption:	-DOPENVDB_ENABLE_RPATH=OFF
BuildOption:	-DOPENVDB_BUILD_VDB_PRINT=ON
BuildOption:	-DOPENVDB_BUILD_VDB_LOD=ON
BuildOption:	-DOPENVDB_BUILD_VDB_VIEW=ON
BuildOption:	-DOPENVDB_BUILD_VDB_RENDER=ON
BuildOption:	-DOPENVDB_BUILD_VDB_TOOL=ON
BuildOption:	-DOPENVDB_TOOL_USE_ABC:BOOL=ON
BuildOption:	-DOPENVDB_TOOL_USE_JPG:BOOL=ON
BuildOption:	-DOPENVDB_TOOL_USE_NANO:BOOL=OFF
BuildOption:	-DOPENVDB_TOOL_USE_PNG:BOOL=ON
%if %{with ax}
BuildOption:	-DHAVE_FFI_CALL=ON
BuildOption:	-DUSE_AX=ON
BuildOption:	-DLLVM_STATIC=0
BuildOption:	-DLLVM="%{_bindir}"
BuildOption:	-DOPENVDB_BUILD_VDB_AX:BOOL=ON
%endif
%if %{with docs}
BuildOption:	-DOPENVDB_BUILD_DOCS=ON
%endif
%if %{with imath}
BuildOption:	-DUSE_IMATH_HALF=ON
%endif
%if %{with nanovdb}
BuildOption:	-DUSE_NANOVDB=ON
BuildOption:	-DNANOVDB_USE_OPENVDB=OFF
%endif
%if %{with openexr}
BuildOption:	-DUSE_EXR=ON
%endif
%if %{with python}
BuildOption:	-DOPENVDB_BUILD_PYTHON_MODULE=ON
BuildOption:	-DPYOPENVDB_INSTALL_DIRECTORY="%{python_sitearch}"
BuildOption:	-DPython_EXECUTABLE="%{__python}"
BuildOption:	-Dnanobind_DIR="%{python_sitelib}/nanobind/cmake"
%endif
%if %{with tests}
BuildOption:	-DOPENVDB_BUILD_UNITTESTS:BOOL=ON
%if %{with python}
BuildOption:	-DOPENVDB_BUILD_PYTHON_UNITTESTS:BOOL=ON
%endif
%endif
BuildOption:	-GNinja


BuildRequires:	cmake
BuildRequires:	cmake(Alembic)
BuildRequires:	boost-devel
BuildRequires:	ghostscript
BuildRequires:	ninja
BuildRequires:	pkgconfig(blosc)
BuildRequires:	pkgconfig(cppunit)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glfw3)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(gtest)
BuildRequires:	pkgconfig(jemalloc)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(log4cpp)
BuildRequires:	pkgconfig(pybind11)
BuildRequires:	pkgconfig(tbb)
BuildRequires:	pkgconfig(tinfo)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	rpm-memory-constraints
%if %{with ax}
BuildRequires:	cmake(llvm)
BuildRequires:	pkgconfig(libffi)
%endif
%if %{with docs}
BuildRequires:	doxygen
BuildRequires:	texlive-latex
%endif
%if %{with imath}
BuildRequires:	pkgconfig(Imath)
%endif
%if %{with openexr}
BuildRequires:	pkgconfig(OpenEXR)
%endif
%if %{with python}
BuildRequires:	nanobind
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(numpy)
%endif

%description
OpenVDB is a C++ library comprising a hierarchical data structure and
a large suite of tools for the efficient storage and manipulation of
sparse volumetric data discretized on three-dimensional grids.

%package -n %{libname}
Summary:	Sparse volume data structure library
Group:		System/Libraries

%description -n %{libname}
OpenVDB is a C++ library comprising a hierarchical data structure and
a large suite of tools for the efficient storage and manipulation of
sparse volumetric data discretized on three-dimensional grids.

%package -n %{devname}
Summary:	Development files for %{name}
Group:	Development/Libraries/C and C++
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%if %{with nanovdb}
%package nanovdb
Summary:	GPU-optimised VDB implementation
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description nanovdb
A lightweight GPU friendly version of VDB initially
targeting rendering applications.

%package nanovdb-devel
Summary:	Development files for nanovdb
Group:	Development/Libraries/C and C++
Requires:	%{name}-nanovdb = %{version}-%{release}

%description nanovdb-devel
The %{name}-nanovdb-devel package contains libraries and header files
for developing applications that use nanovdb.
%endif

%if %{with python}
%package -n python-%{name}
Summary:	OpenVDB C++ Python bindings module
Group:		Development/Python
Requires:	%{libname} = %{version}-%{release}

%description -n python-%{name}
Python module providing OpenVDB C++ Python bindings.
%endif


%build -p
%limit_build -m 3072
export CXXFLAGS="%{optflags} -Wl,--as-needed"

%install -a
%if %{with docs}
# Let RPM pick up html documents in the files section
mv %{buildroot}%{_docdir}/OpenVDB/html .
rm -rf %{buildroot}%{_datadir}/doc
%endif
# We dont need these
find %{buildroot} -name '*.a' -delete

%if %{with tests}
%check
export PYTHONPATH="%{buildroot}%{python_sitearch}"
export LD_LIBRARY_PATH="%{buildroot}%{_libdir}"

ctest --test-dir=_OMV_rpm_build
%endif

%files
%{_bindir}/vdb_{lod,print,render,tool,view}
%if %{with ax}
%{_bindir}/vdb_ax
%endif

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*
%if %{with ax}
%{_libdir}/lib%{name}_ax.so.%{major}*
%endif

%files -n %{devname}
%{_includedir}/%{name}
%if %{with ax}
%{_includedir}/%{name}_ax
%{_libdir}/lib%{name}_ax.so
%endif
%{_libdir}/lib%{name}.so
%{_libdir}/cmake/OpenVDB
%if %{with docs}
%doc html
%endif

%if %{with nanovdb}
%files nanovdb
%{_bindir}/nanovdb_{convert,print,validate}

%files nanovdb-devel
%{_includedir}/nanovdb
%endif

%if %{with python}
%files -n python-%{name}
%{python_sitearch}/%{name}.cpython*.so
%endif
