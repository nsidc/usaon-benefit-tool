---
title: "Operation"
---

This application is operated by NSIDC. In the NSIDC environment, all of the values
needed are provisioned on to deployment hosts with Puppet. The secret values are pulled
from our secrets management system.


## Application version

To pull the correct image from DockerHub, the application version must be passed.
See [our environment variable reference][envvars-doc] for more.


## Session security

The application needs a randomized secret key to secure sessions. Generating a new one
every time would break all sessions every time the app is re-deployed, so we store a
persistent value and pass it in as an environment variable. This is a setting for Flask
(`FLASK_SECRET_KEY`), not something we've implemented specifically for this app.
See [our environment variable reference][envvars-doc] for more.


## Proxy switch

When the app is running, for example behind a proxy, at any path other than `/`, it
needs to be told by request headers (`X-Forwarded-Prefix`) what that path is. To enable
that behavior, set `USAON_BENEFIT_TOOL_PROXY` envvar to `true`.
See [our environment variable reference][envvars-doc] for more.


## TLS certificate

The application expects a TLS certificate to be provided to it from the host. Our
Compose YAML uses environment variables to find these files on the host.
See [our environment variable reference][envvars-doc] for more.

These files are passed in to the container as
[secrets](https://docs.docker.com/compose/use-secrets/).

:::{.callout-note}
If they expire and need to be regenerated, the application may need to be restarted to
pick up the change.
:::


## Single Sign On (SSO)

Currently, we only support Google as an SSO provider. We pass in the needed values as
environment variables.
See [our environment variable reference][envvars-doc] for more.


## Database connectivity

This application expects a PostgreSQL database to be running. The connection
information, including credentials, are passed in as environment variables.
See [our environment variable reference][envvars-doc] for more.


[envvars-doc]: /reference/envvars.md
