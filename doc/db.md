# Database


It's expected that you'll set up a DB separately from the app. The app uses a proxy
container to enable it to talk to an external DB through the hostname `db`.


## Data model

The data model is managed by SQLAlchemy. The model is at
`usaon-vta-survey/models/tables.py`


### Changes to the data model

We haven't started working on data migrations yet.

For now, it's expected that the database will be re-initialized completely to apply
changes.

To do that:

```
./scripts/invoke_in_container.sh db.init
```

> :warning: Don't forget to set USAON_VTA_SURVEY_VERSION envvar to match the running
> container (`source VERSION.env`), or a new container will be pulled.
