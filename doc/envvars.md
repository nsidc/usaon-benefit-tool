# Environment variables

## Web

* `FLASK_DEBUG` (default `False`): Enable debugging within the Flask development server
    ([doc](https://flask.palletsprojects.com/en/2.2.x/config/#DEBUG)).
* `FLASK_SECRET_KEY`: For securely signing session cookie and other security needs
    ([doc](https://flask.palletsprojects.com/en/2.2.x/config/#SECRET_KEY)).


## Database

* `DB_HOST`: The host on which the database is running (NOTE: Only postgres supported)
* `DB_PORT`: The access port for the database
* `DB_USER`: Username with permissions to create tables, delete tables, insert, update,
    delete
* `DB_PASSWORD`: Password for the above user
