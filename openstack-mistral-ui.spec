
%global pypi_name mistral-dashboard
%global openstack_name mistral-ui
# oslosphinx do not work with sphinx > 2
%global with_doc 0

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
BuildRequires:  openstack-dashboard >= 1:17.1.0
BuildRequires:  python3-devel
BuildRequires:  python3-flake8
BuildRequires:  python3-mistralclient
BuildRequires:  python3-mock >= 1.2
BuildRequires:  python3-osprofiler
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires: openstack-macros

BuildRequires:  python3-selenium

Requires:       openstack-dashboard >= 1:17.1.0
Requires:       python3-django-compressor >= 2.0
Requires:       python3-django >= 1.11
Requires:       python3-iso8601 >= 0.1.11
Requires:       python3-pbr
Requires:       python3-mistralclient >= 3.1.0
Requires:       python3-osprofiler

Requires:       python3-PyYAML >= 3.10

%description
Mistral Dashboard is an extension for OpenStack Dashboard that provides a UI
for Mistral.

%if 0%{?with_doc}
# Documentation package
%package -n python3-%{openstack_name}-doc
Summary:        Documentation for OpenStack Mistral Dashboard for Horizon

BuildRequires:  python3-oslo-sphinx
BuildRequires:  python3-sphinx

%{?python_provide:%python_provide python3-%{openstack_name}-doc}

%description -n python3-%{openstack_name}-doc
Documentation for Mistral Dashboard
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version}
# Let RPM handle the dependencies
%py_req_cleanup

%build
%{py3_build}

%if 0%{?with_doc}
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

# Move config to horizon
install -p -D -m 644 mistraldashboard/enabled/_50_mistral.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_50_mistral.py

%check
export PYTHONPATH=/usr/share/openstack-dashboard/
%{__python3} manage.py test mistraldashboard --settings=mistraldashboard.test.settings ||:

%files
%doc README.rst
%license LICENSE
%{python3_sitelib}/mistraldashboard
%{python3_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_50_mistral.py*

%if 0%{?with_doc}
%files -n python3-%{openstack_name}-doc
%doc html
%endif


%changelog
