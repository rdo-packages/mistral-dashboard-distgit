%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  openstack-dashboard >= 1:17.1.0
BuildRequires:  python3-devel
BuildRequires:  python3-flake8
BuildRequires:  python3-mistralclient
BuildRequires:  python3-mock >= 1.2
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires: openstack-macros

BuildRequires:  python3-selenium

Requires:       openstack-dashboard >= 1:17.1.0
Requires:       python3-iso8601 >= 0.1.11
Requires:       python3-pbr
Requires:       python3-mistralclient >= 4.3.0

Requires:       python3-PyYAML >= 3.12

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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
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
