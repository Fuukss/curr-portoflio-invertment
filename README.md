# curr-portfolio-investment

## Running the Project Locally
First, clone the repository to your local machine:

```
$ git clone git@github.com:Fuukss/curr-portoflio-invertment.git 
```

## Run the development server: 
```
$ docker-compose up --build
```

## Error starting
```
ERROR: ... Bind for 0.0.0.0:5432 failed: port is already allocated

This 👇 works for me.
 
$ lsof -t -i tcp:5432 | xargs kill -9

or 

$ docker-compose down
$ docker rm -fv $(docker ps -aq)
$ sudo lsof -i -P -n | grep 5432

- For mac 
$ kill -9 <process id>

- For Linux
$ sudo kill <proces id>
```

## Setup
Access to admin panel: <href>localhost:8000/admin:</href>
```
$ docker exec -it django python manage.py createsuperuser
```
## Running app 
The project will be available at http://localhost:8000/

