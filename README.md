# Pawtrails API Server

This repository contains the code for the Pawtrails Web API Server. Currently only the Backend portion of the code is planned and available. The application is built in Python/FastAPI and connected to the Neo4j Database.

## Local Start

Not recomended but you can start the application locally. Keep in mind that you will have to manually configure the dependencies and PostgreSQL instance.

1. Create an environment and activate it
```
$ python3 -m venv venv
$ source venv/bin/activate
```

2. Update pip, install poetry, install all packages
```
$ python -m pip install --upgrade pip
$ pip install poetry
$ poetry install
```

> Before actually running the application *YOU* **SHOULD** edit the **.env** file so that it points to a valid Neo4j instance.

3. Run application using Uvicorn ASGI

```
$ uvicorn app.main:app --reload
```
> If you are using WSL2 please ensure that you have localhostForwarding=true in your .wslconfig file. If uvicorn still does not start, restart the WSL2.

## Docker usage

The workflow is centered around VSCode. First go into your terminal and start the debug compose file:

```
$ docker-compose -f docker-compose.debug.yml up --build
```
Wait for both Neo4j and Pawtrails_backend to finish initializing (It is when debugpy finishes installing); then go into VSCode and hit **F5** or **Run>Start Debugging**.
> If it asks for the configuration select *"Python: Remote Attach to pawtrails_backend"*

### Prune Docker
If something went wrong, you can destroy everything using the following commands
```
$ docker system prune -af
$ docker volume prune -f
```
> Keep in mind that this assumes you only use Docker for Pawtrails.
>
>If you also have other projects depending on docker, you will have to manually search for the containers, images and volumes using *docker image/container/volume ls* command and then manuall removing them with *docker image/container/volume rm ...* command.

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

## Workflow && Code-Style

The standard development environment its Visual Studio Code with Python, Docker and Comment Anchors. The formatter is Black and linting is done by Flake8.
The allowed comment tags are the ones by Comment Anchors.


## File structure
The routes are located in the API folder.

## Pre-Commit hooks
The pre-commit hooks will run isort, black, flake8 and mypy on the code.
It will also run several other pre-commit hooks.
To test if everything will pass without commiting use the following:
```
$  pre-commit run --all-files
```
To ignore the hooks and commit without them use:
```
$ git commit -m "Bypassing pre-commit hooks" --no-verify
```
> Please do not skip pre-commit hooks :)

## TODO
Investigate mypy and type-hints
Poetry supports scripts... add them :)
Write better documentation
Pydantic config is connected to env
Deploy to AWS
