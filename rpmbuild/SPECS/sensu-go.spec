%define debug_package %{nil}
%undefine _disable_source_fetch

Name:           sensu-go
Version:        5.19.0
Release:        1%{?dist}
Summary:        A monitoring framework
License:        MIT
URL:            https://github.com/sensu/sensu-go
Source0:        https://github.com/sensu/sensu-go/archive/v%{version}.zip 
Source1:        sensu-backend.service
Source2:        sensu-agent.service
Source3:        backend.yml
Source4:	    sensu-build.sh
Source5:	    agent.yml
Source6:	    %{name}-tmpfiles.conf

BuildRequires:  systemd
BuildRequires:  golang >= 1.13-0

Requires(pre):  shadow-utils

ExclusiveArch:  x86_64

%description
Sensu is an open source monitoring tool for ephemeral infrastructure and distributed
applications. It is an agent based monitoring system with built-in auto-discovery, 
making it very well-suited for cloud environments. Sensu uses service checks to 
monitor service health and collect telemetry data. It also has a number of well 
defined APIs for configuration, external data input, and to provide access to 
Sensu's data. Sensu is extremely extensible and is commonly referred to as 
"the monitoring router".

%package backend
Summary: Sensu Go Backend Service
%description backend
The Sensu backend is a service that manages check requests and event data. 
Every Sensu backend includes an integrated transport for scheduling checks 
using subscriptions, an event processing pipeline that applies filters, 
mutators, and handlers, an embedded etcd datastore for storing configuration
and state, a Sensu API, a Sensu dashboard, and the sensu-backend command line tool.

%package agent
Summary: Sunsu Go Agent Service
%description agent
The Sensu agent is a lightweight client that runs on the infrastructure 
components you want to monitor.  Agents register with the Sensu backend as
monitoring entities with type: "agent". Agent entities are responsible for 
creating check and metrics events to send to the backend event pipeline.


%prep
%setup -q

%build
mkdir -p %{buildroot}/usr/sbin
cp %{SOURCE4} sensu-build.sh 
./sensu-build.sh -v %{version}
cp bin/* %{buildroot}/usr/sbin

%install 
mkdir -p %{buildroot}%{_tmpfilesdir}
mkdir -p %{buildroot}/usr/lib/systemd/system
mkdir -p %{buildroot}/etc/sensu
mkdir -p %{buildroot}/usr/sbin
mkdir -p %{buildroot}/var/lib/sensu
mkdir -p %{buildroot}/var/cache/sensu
mkdir -p %{buildroot}/var/log/sensu
mkdir -p %{buildroot}/run/sensu
install -m 755 bin/sensu-agent %{buildroot}/usr/sbin/sensu-agent
install -m 755 bin/sensu-backend %{buildroot}/usr/sbin/sensu-backend
install -m 755 bin/sensuctl %{buildroot}/usr/sbin/sensuctl
install -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/sensu-backend.service
install -m 0640 %{SOURCE3} %{buildroot}/etc/sensu/backend.yml
install -m 0644 %{SOURCE2} %{buildroot}/usr/lib/systemd/system/sensu-agent.service
install -m 0640 %{SOURCE5} %{buildroot}/etc/sensu/agent.yml
install -m 0644 %{SOURCE6} %{buildroot}%{_tmpfilesdir}/%{name}.conf

%check

%pre backend
getent group sensu >/dev/null || groupadd -r sensu
getent passwd sensu >/dev/null || \
    useradd -r -g sensu -d /opt/sensu -s /sbin/nologin \
    -c "Sensu User" sensu
exit 0

%pre agent
getent group sensu >/dev/null || groupadd -r sensu
getent passwd sensu >/dev/null || \
    useradd -r -g sensu -d /opt/sensu -s /sbin/nologin \
    -c "Sensu User" sensu
exit 0

%post backend
%systemd_post sensu-backend.service 

%post agent
%systemd_post sensu-agent.service 

%preun backend
%systemd_preun sensu-backend.service

%preun agent
%systemd_preun sensu-agent.service

%postun backend
%systemd_postun sensu-backend.service

%postun agent
%systemd_postun sensu-agent.service

%files backend
%attr(-,sensu,sensu) %dir /var/lib/sensu/
%attr(755, sensu, sensu) %dir /etc/sensu/
%attr(755, sensu, sensu) %dir /var/cache/sensu/
%attr(755, sensu, sensu) %dir /var/log/sensu/
%ghost %attr(755, sensu, sensu) /run/sensu/
%config(noreplace) %attr(644, sensu, sensu) /etc/sensu/backend.yml
%attr(644, root, root) /usr/lib/systemd/system/sensu-backend.service
%attr(755, root, root) /usr/sbin/sensu-backend
%attr(755, root, root) /usr/sbin/sensuctl
%{_tmpfilesdir}/%{name}.conf
%exclude /etc/sensu/agent.yml

%files agent
%attr(-,sensu,sensu) %dir /var/lib/sensu/
%attr(755, sensu, sensu) %dir /etc/sensu/
%attr(755, sensu, sensu) %dir /var/cache/sensu/
%attr(755, sensu, sensu) %dir /var/log/sensu/
%ghost %attr(755, sensu, sensu) /run/sensu/
%config(noreplace) %attr(644, sensu, sensu) /etc/sensu/agent.yml
%attr(644, root, root) /usr/lib/systemd/system/sensu-agent.service
%attr(755, root, root) /usr/sbin/sensu-agent
%{_tmpfilesdir}/%{name}.conf
%exclude /etc/sensu/backend.yml


%changelog
* Wed Apr 01 2020 Devin Acosta <devin@linuxstack.cloud> - 1.00.0-3
- Fixed Configs being overwritten, added +oss_el7|8 to version
* Mon Mar 30 2020 Devin Acosta <devin@linuxstack.cloud> - 1.00.0-3
- Fixed agent config in backend, and vice versus.
* Sun Mar 29 2020 Devin Acosta <devin@linuxstack.cloud> - 1.00.0-2
- Added SPEC to create sensu-go-backend/sensu-go-agent RPMS
* Sun Mar 29 2020 Devin Acosta <devin@linuxstack.cloud> - 1.00.0-1
- Initial package
