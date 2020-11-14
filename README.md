# ambulance-visualization-back-end
First the postgres database must be set up. Follow the instructions in the data repo for the postgres database.

# SQLAlchemy

After the database is set up with the docker container delete the migrations file in the src directory and follow the commands below.

1. Install Sumo using the following command.
```sh
sudo apt-get install sumo sumo-tools sumo-doc
```

2. Initializing the Database
```sh
flask db init
```
3. Then migrate the DB so it reflect your changes
```sh
flask db migrate -m "Initial migration."
```
4. Once you have made a change update
```sh
flask db upgrade
```

## To run the backend
```sh
pip3 install -r requirements.txt
```
```sh
cd src
```
```sh
flask run
```

# To run tests

```sh
cd src
```
```sh
nose2 -v app.tests.unit.test --with-coverage
```
