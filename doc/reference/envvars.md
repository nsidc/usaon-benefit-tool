---
title: "Environment variables"
---


## Deployment

* `USAON_BENEFIT_TOOL_VERSION`: Which tag on Docker Hub to deploy.


## Web

* `FLASK_SECRET_KEY`: For securely signing session cookie and other security
  needs ([doc](https://flask.palletsprojects.com/en/2.2.x/config/#SECRET_KEY)).
* `USAON_BENEFIT_TOOL_PROXY`: "True" if we are deploying with a proxy to pass the header
  `X-Forwarded-Prefix`.


### Transport Level Security (TLS)

* `TLS_CERT_FILE`: Path to `.crt` file.
* `TLS_KEY_FILE`: Path to `.key` file.


## SSO

* `USAON_BENEFIT_TOOL_GOOGLE_CLIENT_ID`: The google credential id.
* `USAON_BENEFIT_TOOL_GOOGLE_CLIENT_SECRET`: The google sso credential secret.
* `OAUTHLIB_RELAX_TOKEN_SCOPE=1`: Should always be set; hardcoded in Compose YAML.


### Development only

> [!IMPORTANT]
>
> **Do not set in production.**

* `OAUTHLIB_INSECURE_TRANSPORT=1`: Enable SSO when developing without HTTPS.


## Database

* `USAON_BENEFIT_TOOL_DB_HOST`: The host on which the database is running.
* `USAON_BENEFIT_TOOL_DB_PORT`: The access port for the database.
* `USAON_BENEFIT_TOOL_DB_USER`: Username with permissions to create tables, delete tables, insert, update,
    delete.
* `USAON_BENEFIT_TOOL_DB_PASSWORD`: Password for the above user.
