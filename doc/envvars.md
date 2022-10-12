# Environment variables

## Web

* `FLASK_SECRET_KEY` (required): For securely signing session cookie and other security
  needs ([doc](https://flask.palletsprojects.com/en/2.2.x/config/#SECRET_KEY)).


## Database

All of the below environment variables are required.

* `DB_HOST`: The host on which the database is running (NOTE: Only postgres supported)
* `DB_PORT`: The access port for the database
* `DB_USER`: Username with permissions to create tables, delete tables, insert, update,
    delete
* `DB_PASSWORD`: Password for the above user
