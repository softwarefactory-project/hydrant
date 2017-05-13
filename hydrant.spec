%global         sum SF Firehose consumer storing events on ElasticSearch

Name:           hydrant
Version:        0.1.1
Release:        1%{?dist}
Summary:        %{sum}

License:        ASL 2.0
URL:            https://softwarefactory-project.io/r/p/software-factory/%{name}
Source0: HEAD.tgz

BuildArch:      noarch

Requires:       python-paho-mqtt
Requires:       PyYAML
Requires:       python-elasticsearch

Buildrequires:  python2-devel
Buildrequires:  python-setuptools
Buildrequires:  python2-pbr
Buildrequires:  python-nose
Buildrequires:	python-mock
Buildrequires:  git
Buildrequires:	PyYAML
Buildrequires:	python-paho-mqtt
Buildrequires:  python-elasticsearch

%description
SF Firehose consumer storing events on ElasticSearch

%prep
%autosetup -n %{name}-%{version}

%build
# init git for pbr
git init
%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}
install -p -D -m 644 hydrant.service %{buildroot}/%{_unitdir}/%{name}.service
mkdir -p %{buildroot}/%{_sysconfdir}/
install -p -D -m 644 etc/hydrant.yaml %{buildroot}/%{_sysconfdir}/%{name}/hydrant.yaml

%check
nosetests -v

%pre
getent group hydrant >/dev/null || groupadd -r hydrant
getent passwd hydrant >/dev/null || \
useradd -r -g hydrant -G hydrant -d /usr/bin/hydrant -s /sbin/nologin \
-c "hydrant daemon" hydrant
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files -n hydrant
%{python2_sitelib}/*
%{_bindir}/*
%{_unitdir}/*
%config(noreplace) %{_sysconfdir}/*

%changelog
* Sat May 13 2017 Matthieu Huin <mhuin@redhat.com> - 0.1.1-1
- Rename module for PyPI

* Fri May 12 2017 Matthieu Huin <mhuin@redhat.com> - 0.1.0-1
- First release

* Fri May 12 2017 Matthieu Huin <mhuin@redhat.com> - 0.0.0-1
- Initial package
