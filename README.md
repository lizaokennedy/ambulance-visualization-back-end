# ambulance-visualization-back-end
To Set up container
```
docker run   --name pg-docker -e POSTGRES_PASSWORD=docker -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data  postgres
```

To start container
```
docker start pg-docker
```

PGadmin passowrd: docker

Login to pg-docker container

```
docker exec -it pg-docker /bin/bash
```

Login to psql
```
psql "dbname=postgres host=localhost user=postgres password=docker port=5432"
```