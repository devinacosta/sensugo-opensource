%define debug_package %{nil}
%undefine _disable_source_fetch

Name:           sensu-go
Version:        5.19.0
Release:        1%{?dist}
Summary:        A monitoring framework
Group:          Development/Languages
License:        MIT
URL:            https://github.com/sensu/sensu-go
Source0:        https://github.com/sensu/sensu-go/archive/v%{version}.zip 
Source1:        sensu-backend.service
Source2:        sensu-agent.service
Source3:        backend.yml
Source4:	sensu-build.sh
Source5:	agent.yml
%description
Sensu Go Open Source

%package backend
Summary: Sensu Go Backend Service
%description backend
Sensu Go Backend Package

%package agent
Summary: Sunsu Go Agent Service
%description agent
Sensu Go Agent Package

BuildRequires:      systemd
BuildRequires:	    golang >= 1.13

Requires(pre):      shadow-utils
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

ExclusiveArch: x86_64

%prep
%setup -q

%build
mkdir -p %{buildroot}/usr/sbin
cp %{SOURCE4} sensu-build.sh 
./sensu-build.sh -v %{version}
cp bin/* %{buildroot}/usr/sbin

%install 
mkdir -p %{buildroot}/etc/systemd/system
mkdir -p %{buildroot}/etc/sensu
mkdir -p %{buildroot}/usr/sbin
mkdir -p %{buildroot}/var/lib/sensu
mkdir -p %{buildroot}/var/cache/sensu
mkdir -p %{buildroot}/var/log/sensu
mkdir -p %{buildroot}/var/run/sensu
install -m 755 bin/sensu-agent %{buildroot}/usr/sbin/sensu-agent
install -m 755 bin/sensu-backend %{buildroot}/usr/sbin/sensu-backend
install -m 755 bin/sensuctl %{buildroot}/usr/sbin/sensuctl
install -m 0644 %{SOURCE1} %{buildroot}/etc/systemd/system/sensu-backend.service
install -m 0640 %{SOURCE3} %{buildroot}/etc/sensu/backend.yml
install -m 0644 %{SOURCE2} %{buildroot}/etc/systemd/system/sensu-agent.service
install -m 0640 %{SOURCE5} %{buildroot}/etc/sensu/agent.yml

%check

%pre backend
/usr/bin/getent group sensu || /usr/sbin/groupadd -r sensu
/usr/bin/getent passwd sensu || /usr/sbin/useradd -r -s /sbin/nologin -g sensu sensu

%pre agent
/usr/bin/getent group sensu || /usr/sbin/groupadd -r sensu
/usr/bin/getent passwd sensu || /usr/sbin/useradd -r -s /sbin/nologin -g sensu sensu

%post backend
%systemd_post sensu-backend.service 

%post agent
%systemd_post sensu-agent.service 

%preun backend
%systemd_preun sensu-backend.service

%preun agent
%systemd_preun sensu-agent.service

%postun backend
/usr/sbin/userdel sensu
rm -rf /var/cache/sensu
rm -rf /var/lib/sensu

%postun agent
/usr/sbin/userdel sensu
rm -rf /var/cache/sensu
rm -rf /var/lib/sensu


%files backend
%attr(-,sensu,sensu) %dir /var/lib/sensu/
%attr(755, sensu, sensu) %dir /etc/sensu/
%attr(755, sensu, sensu) %dir /var/cache/sensu/
%attr(755, sensu, sensu) %dir /var/log/sensu/
%attr(755, sensu, sensu) %dir /var/run/sensu/
%attr(644, sensu, sensu) /etc/sensu/backend.yml
%attr(644, root, root) /etc/systemd/system/sensu-backend.service
%attr(755, root, root) /usr/sbin/sensu-backend
%attr(755, root, root) /usr/sbin/sensuctl
%exclude /etc/sensu/agent.yml

%files agent
%attr(-,sensu,sensu) %dir /var/lib/sensu/
%attr(755, sensu, sensu) %dir /etc/sensu/
%attr(755, sensu, sensu) %dir /var/cache/sensu/
%attr(755, sensu, sensu) %dir /var/log/sensu/
%attr(755, sensu, sensu) %dir /var/run/sensu/
%attr(644, sensu, sensu) /etc/sensu/agent.yml
%attr(644, root, root) /etc/systemd/system/sensu-agent.service
%attr(755, root, root) /usr/sbin/sensu-agent
%exclude /etc/sensu/backend.yml


%changelog
* Mon Mar 30 2020 Devin Acosta <devin@linuxstack.cloud> - 1.00.0-3
- Fixed agent config in backend, and vice versus.
* Sun Mar 29 2020 Devin Acosta <devin@linuxstack.cloud> - 1.00.0-2
- Added SPEC to create sensu-go-backend/sensu-go-agent RPMS
* Sun Mar 29 2020 Devin Acosta <devin@linuxstack.cloud> - 1.00.0-1
- Initial package
