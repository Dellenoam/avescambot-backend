# Project: AveScamBot (Backend)

### Disclaimer

All materials presented here are created solely for educational and informational purposes.

Please note that the use of any information or code from this repository for illegal purposes is strictly prohibited. 
The authors of this repository are not liable for any misuse of the material presented here.

### Requirements

This service uses PostgreSQL as its database and asyncpg asynchronous driver. Also, the Python version should be at least 3.12

## Desciption

AveScamBot is a botnet project consisting of admin panel, server and script.

This repository is a server, part of the whole AveScamBot project.
At the moment only JWT authentication is implemented. 

## Future plans

Implement storing JWT refresh tokens on Redis instead of PostgreSQL to quickly refresh access tokens.

Implement the Unit of Work pattern.

## How to use

To get started, clone the repository

```
git clone https://github.com/Dellenoam/avescambot-backend.git
```

Create an .env file and fill in the following configuration parameters using the example below

```
DB_URL = postgresql+asyncpg://username:password@host:port/database_name
COOKIE_SECURE_FLAG = False
```

Create private and public encryption keys

```
openssl genrsa -out private.pem 2048
openssl rsa -in certs/private.pem -outform PEM -pubout -out certs/public.pem
```

Create a virtual environment and install poetry. I prefer to use venv and install poetry in the virutal environment rather than the global environment.

```
python3 -m venv .venv
source .venv/bin/activate
pip install poetry
```

Install dependencies via poetry

```
poetry install --no-dev
```

Hopefully you have created a database and specified the URL to it in .env, if so apply alembic migration to it.

```
alembic upgrade head
```

Now you can try running the server through uvicorn

```
PYTHONPATH=src uvicorn src.main:app --reload
```
