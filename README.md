# sensugo-opensource

Sensu is an open source monitoring tool for ephemeral infrastructure
and distributed applications. It is an agent based monitoring system
with built-in auto-discovery, making it very well-suited for cloud
environments. Sensu uses service checks to monitor service health and
collect telemetry data. It also has a number of well defined APIs for
configuration, external data input, and to provide access to Sensu's
data. Sensu is extremely extensible and is commonly referred to as
"the monitoring router".

To learn more about Sensu, [please visit the
website](https://sensu.io/) and [read the documentation](https://docs.sensu.io/sensu-go/latest/).

## What is Sensu Go?

Sensu Go is a complete rewrite of Sensu in Go, with new capabilities
and reduced operational overhead. It eliminates several sources of
friction for new and experienced Sensu users.

The original Sensu required external services like Redis or RabbitMQ.
Sensu Go can rely on an embedded etcd datastore for persistence, making
the product easier to get started with. External etcd services can also be
used, in the event that you already have them deployed.

Sensu Go replaces Ruby expressions with JavaScript filter expressions, by
embedding a JavaScript interpreter.

Unlike the original Sensu, Sensu Go events are always handled, unless
explicitly filtered.

## Notes

This RPMBUILD repo successfully builds Sensu Go (Open source) edition for CentOS 7 / CentOS 8.

In order for this SPEC file to work it requires:
- Internet Access (to download Go Dependencies)

```
If you have any questions, please contact me:
Devin Acosta
Red Hat Certified Architect
e: devin@linuxstack.cloud
```
