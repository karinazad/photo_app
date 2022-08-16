# PhotoApp
A web application with REST API built using Flask-RESTful. Connected to a PostgreSQL database. Contains an authentication server and a chat server (using web sockets). Created as a part of CS396 Web Development Course at Northwestern University (Winter 2022).

<img src="https://cs396-web-dev.github.io/winter2022/assets/images/homework/hw04/post-detail.gif" >

<br>

## Deployed to Heroku
cs396-northwestern-photoapp.herokuapp.com

<br>


## Installation
To install dependencies, navigate to your `photo-app` directory on your command line and issue the following commands:

```shell
pip3 install -r requirements.txt
```

## Running Flask Server

### On Mac / Linux
```shell
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

### On Windows
```shell
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
# alternative commands to try if "flask run" doesn't work:
# py -m flask run
# python3 -m flask run
# python -m flask run
```
