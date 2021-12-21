# Image-api

## Run the app 
```
$ docker-compose up --build
```

## Error starting
```
ERROR: ... Bind for 0.0.0.0:5432 failed: port is already allocated

This 👇 works for me.
 
$ docker-compose down
$ docker rm -fv $(docker ps -aq)
$ sudo lsof -i -P -n | grep 5432

- For mac 
$ kill -9 <process id>

- For Linux
$ sudo kill <proces id>

- or 
$ lsof -t -i tcp:8000 | xargs kill -9
```

## Setup
To run this project:
```
$ docker exec -it django python manage.py createsuperuser
```

