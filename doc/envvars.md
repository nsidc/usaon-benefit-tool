# Environment variables

## Web

* `FLASK_SECRET_KEY` (required): For securely signing session cookie and other security
  needs ([doc](https://flask.palletsprojects.com/en/2.2.x/config/#SECRET_KEY)).

## SSO
* `OAUTHLIB_INSECURE_TRANSPORT=1`  NOTE: Do not set this in production.
* `OAUTHLIB_RELAX_TOKEN_SCOPE=1` Set in docker-compose`
* `USAON_VTA_GOOGLE_CLIENT_ID`: The google credential id. (stored in vault)
* `USAON_VTA_GOOGLE_CLIENT_SECRET`: The google sso credential secret. (stored in vault)

## Database

All of the below environment variables are required.
Todo: update to USAON_VTA_DB_HOST
* `DB_HOST`: The host on which the database is running (NOTE: Only postgres supported)
* `DB_PORT`: The access port for the database
* `DB_USER`: Username with permissions to create tables, delete tables, insert, update,
    delete
* `DB_PASSWORD`: Password for the above user
