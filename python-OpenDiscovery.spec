#
# spec file for package python-OpenDiscovery
#
# Copyright (c) 2014 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/

%define _binaries_in_noarch_packages_terminate_build   0

Name:           python-OpenDiscovery
Version:        2.0.2
Release:        0
License:        GPL
Summary:        Computational Drug Discovery Software
Url:            https://github.com/iamgp/OpenDiscovery
Group:          Development/Languages/Python
Source:         http://pypi.python.org/packages/source/O/OpenDiscovery/OpenDiscovery-%{version}.tar.gz
BuildRequires:  python-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%if 0%{?suse_version} && 0%{?suse_version} <= 1110
%{!?python_sitelib: %global python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%else
BuildArch:      noarch
%endif

%description
UNKNOWN

%prep
%setup -q -n OpenDiscovery-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitelib}/*
/usr/bin/odscreen.py

%changelog