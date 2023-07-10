# Development

## Deploy the development database

Deploy usaon-vta-db (add link later) and follow instructions in that repo. 

## Symlink dev config

```ln -s docker-compose.dev.yml docker-compose.override.yml```


## Define environment variables

Define the environment variables as specified in [envvars.md](./envvars.md)  

```bash
export DB_HOST=...
export DB_PORT=...
export DB_USER=...
export DB_PASSWORD=...
```

## Start the service

Bring up the docker container 

```docker-compose up -d```


## Initialize the database

Run `./scripts/invoke_in_container.sh db.init`
