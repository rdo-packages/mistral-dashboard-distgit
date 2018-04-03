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
BuildRequires:  python2-devel
BuildRequires:  python2-django-nose >= 1.2
BuildRequires:  python2-flake8
BuildRequires:  python2-mistralclient
BuildRequires:  python2-mock >= 1.2
BuildRequires:  python2-mox
BuildRequires:  python2-mox3
BuildRequires:  python2-nose
BuildRequires:  python-nose-exclude
BuildRequires:  python-openstack-nose-plugin
BuildRequires:  python2-osprofiler
BuildRequires:  python2-oslo-sphinx
BuildRequires:  python2-pbr
BuildRequires:  python-selenium
BuildRequires:  python2-setuptools
BuildRequires:  python2-sphinx
BuildRequires: openstack-macros

Requires:       openstack-dashboard >= 1:8.0.0
Requires:       python2-django-compressor >= 2.0
Requires:       python2-django >= 1.8
Requires:       python2-iso8601 >= 0.1.11
Requires:       python2-pbr
Requires:       python2-mistralclient >= 3.1.0
Requires:       python2-osprofiler
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
%py_req_cleanup

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
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/mistral-dashboard/commit/?id=21f4afaf95323f7023cd626073379600f31cbba1
