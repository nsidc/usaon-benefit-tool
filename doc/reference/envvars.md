# Environment variables

## Web

* `FLASK_SECRET_KEY` (required): For securely signing session cookie and other security
  needs ([doc](https://flask.palletsprojects.com/en/2.2.x/config/#SECRET_KEY)).
* `USAON_BENEFIT_TOOL_PROXY`: True if we are deploying with a proxy to pass the header `X-Forwarded-Prefix`.


## SSO

* `OAUTHLIB_INSECURE_TRANSPORT=1`  NOTE: Do not set this in production.
* `OAUTHLIB_RELAX_TOKEN_SCOPE=1` Set in docker-compose YAML.
* `USAON_BENEFIT_TOOL_GOOGLE_CLIENT_ID`: The google credential id. (stored in vault)
* `USAON_BENEFIT_TOOL_GOOGLE_CLIENT_SECRET`: The google sso credential secret. (stored in vault)


## Database

All of the below environment variables are required.
* `USAON_BENEFIT_TOOL_DB_HOST`: The host on which the database is running (NOTE: Only postgres supported)
* `USAON_BENEFIT_TOOL_DB_PORT`: The access port for the database
* `USAON_BENEFIT_TOOL_DB_USER`: Username with permissions to create tables, delete tables, insert, update,
    delete
* `USAON_BENEFIT_TOOL_DB_PASSWORD`: Password for the above user
