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
BuildRequires:  openstack-dashboard >= 8.0.0
BuildRequires:  python2-devel
BuildRequires:  python-coverage >= 3.6
BuildRequires:  python-django-nose >= 1.2
BuildRequires:  python-flake8
BuildRequires:  python-mistralclient
BuildRequires:  python-mock >= 1.2
BuildRequires:  python-mox
BuildRequires:  python-mox3
BuildRequires:  python-nose
BuildRequires:  python-nose-exclude
BuildRequires:  python-openstack-nose-plugin
BuildRequires:  python-osprofiler
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-pbr
BuildRequires:  python-selenium
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx

Requires:       openstack-dashboard >= 8.0.0
Requires:       python-django-openstack-auth >= 3.1.0
Requires:       python-django-compressor >= 2.0
Requires:       python-django >= 1.8
Requires:       python-iso8601 >= 0.1.11
Requires:       python-pbr
Requires:       python-mistralclient
Requires:       python-osprofiler
Requires:       PyYAML >= 3.10

%description
Mistral Dashboard is an extension for OpenStack Dashboard that provides a UI
for Mistral.

# Documentation package
%package -n python-%{openstack_name}-doc
Summary:        Documentation for OpenStack Mistral Dashboard for Horizon

%description -n python-%{openstack_name}-doc
Documentation for Mistral Dashboard

%prep
%autosetup -n %{pypi_name}-%{upstream_version}
# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

%build
%{__python2} setup.py build

sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

# Move config to horizon
install -p -D -m 640 mistraldashboard/enabled/_50_mistral.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_50_mistral.py

%check
PYTHONPATH=/usr/share/openstack-dashboard/ ./run_tests.sh -N -P ||:

%files
%doc README.rst
%license LICENSE
%{python2_sitelib}/mistraldashboard
%{python2_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_50_mistral.py*

%files -n python-%{openstack_name}-doc
%doc html


%changelog
