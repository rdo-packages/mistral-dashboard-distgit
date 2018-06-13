%global pypi_name mistral-dashboard
%global openstack_name mistral-ui

# tests are disabled by default
%bcond_with tests

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-%{openstack_name}
Version:        5.2.4
Release:        1%{?dist}
Summary:        OpenStack Mistral Dashboard for Horizon

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

#

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  openstack-dashboard >= 8.0.0
BuildRequires:  python2-devel
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
Requires:       python-django-openstack-auth >= 3.5.0
Requires:       python-django-compressor >= 2.0
Requires:       python-django >= 1.8
Requires:       python-iso8601 >= 0.1.11
Requires:       python-pbr
Requires:       python-mistralclient >= 3.1.0
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
* Wed Jun 13 2018 RDO <dev@lists.rdoproject.org> 5.2.4-1
- Update to 5.2.4

* Tue Feb 13 2018 RDO <dev@lists.rdoproject.org> 5.2.2-1
- Update to 5.2.2

* Mon Feb 12 2018 RDO <dev@lists.rdoproject.org> 5.2.1-1
- Update to 5.2.1

* Thu Nov 16 2017 RDO <dev@lists.rdoproject.org> 5.2.0-1
- Update to 5.2.0

* Wed Aug 30 2017 rdo-trunk <javier.pena@redhat.com> 5.0.0-1
- Update to 5.0.0

* Thu Aug 24 2017 Alfredo Moralejo <amoralej@redhat.com> 5.0.0-0.1.0rc1
- Update to 5.0.0.0rc1

