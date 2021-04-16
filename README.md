# Pawtrail API Server

## Local Development

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

> If you are using WSL2 please ensure that you have localhostForwarding=true in your .wslconfig file. If uvicorn still does not start, restart the WSL2.

## How to run

```
$ uvicorn app.main:app
```