# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility

%global pypi_name mistral-dashboard
%global openstack_name mistral-ui

# tests are disabled by default
%bcond_with tests

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-%{openstack_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack Mistral Dashboard for Horizon

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  openstack-dashboard >= 1:8.0.0
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-flake8
BuildRequires:  python%{pyver}-mistralclient
BuildRequires:  python%{pyver}-mock >= 1.2
BuildRequires:  python%{pyver}-osprofiler
BuildRequires:  python%{pyver}-oslo-sphinx
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-sphinx
BuildRequires: openstack-macros

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python-selenium
%else
BuildRequires:  python%{pyver}-selenium
%endif

Requires:       openstack-dashboard >= 1:8.0.0
Requires:       python%{pyver}-django-compressor >= 2.0
Requires:       python%{pyver}-django >= 1.11
Requires:       python%{pyver}-iso8601 >= 0.1.11
Requires:       python%{pyver}-pbr
Requires:       python%{pyver}-mistralclient >= 3.1.0
Requires:       python%{pyver}-osprofiler
Requires:       PyYAML >= 3.10

%description
Mistral Dashboard is an extension for OpenStack Dashboard that provides a UI
for Mistral.

# Documentation package
%package -n python%{pyver}-%{openstack_name}-doc
Summary:        Documentation for OpenStack Mistral Dashboard for Horizon
%{?python_provide:%python_provide python%{pyver}-%{openstack_name}-doc}

%description -n python%{pyver}-%{openstack_name}-doc
Documentation for Mistral Dashboard

%prep
%autosetup -n %{pypi_name}-%{upstream_version}
# Let RPM handle the dependencies
%py_req_cleanup

%build
%{pyver_build}

sphinx-build-%{pyver} doc/source html
# remove the sphinx-build-%{pyver} leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{pyver_install}

# Move config to horizon
install -p -D -m 640 mistraldashboard/enabled/_50_mistral.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_50_mistral.py

%check
export PYTHONPATH=/usr/share/openstack-dashboard/
%{pyver_bin} manage.py test mistraldashboard --settings=mistraldashboard.test.settings ||:

%files
%doc README.rst
%license LICENSE
%{pyver_sitelib}/mistraldashboard
%{pyver_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_50_mistral.py*

%files -n python%{pyver}-%{openstack_name}-doc
%doc html


%changelog
