# Pawtrails API Server

This repository contains the code for the Pawtrails Web API Server. Currently only the Backend portion of the code is planned and available. The application is built in Python/FastAPI and connected to the PostgreSQL database.

## Local Start

Not recomended but you can start the application locally. Keep in mind that you will have to manually configure the dependencies and PostgreSQL instance.

1. Create an environment and activate it
```
$ python3 -m venv env
$ source env/bin/activate
```

2. Update pip and install required packages
```
$ python -m pip install --upgrade pip
$ pip install -r requirements.txt
```

> Before actually running the application *YOU* **SHOULD** edit the **.env** file so that it points to a valid PostgreSQL instance, or customize the application to use sqlite3 if you wish to do so.

3. Run application using Uvicorn ASGI

```
$ uvicorn app.main:app --reload
```
> If you are using WSL2 please ensure that you have localhostForwarding=true in your .wslconfig file. If uvicorn still does not start, restart the WSL2.

## Docker usage

This is the recomended way to build the application.

```
$ docker-compose up --build
```

If something went wrong, you can destroy everything using the following commands
```
$ docker system prune -af
$ docker volume prune -f
```
> Keep in mind that this assumes you only use Docker for Pawtrails.
>
>If you also have other projects depending on docker, you will have to manually search for the containers, images and volumes using *docker image/container/volume ls* command and then manuall removing them with *docker image/container/volume rm ...* command.

## pgAdmin

The server is not automatically added. You will have to add the server using the info located in the **.env** file.
> Default server host is not localhost but postgres

You can view the admin panel at:
```
http://localhost:5050
```

## View Docs

To view the swagger generated docs visit:
```
http://localhost:8000/docs
```

If you want to see redoc for some reason, you can do it at:
```
http://localhost:8000/redoc
```
> If the links are not working, use 127.0.0.1 instead of localhost