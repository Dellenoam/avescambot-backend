# Project: AveScamBot (Backend)

## Disclaimer

All materials presented here are created solely for educational and informational purposes.

Please note that the use of any information or code from this repository for illegal purposes is strictly prohibited.
The authors of this repository are not liable for any misuse of the material presented here.

## Requirements

- Python 3.12 or later
- PostgreSQL database
- OpenSSL for generating encryption keys

## Desciption

AveScamBot is a botnet project consisting of admin panel, server and script.

This repository is a server, part of the whole AveScamBot project.
At the moment only JWT authentication is implemented.

## Future plans

Implement storing JWT refresh tokens on Redis instead of PostgreSQL to quickly refresh access tokens.

Implement the Unit of Work pattern.

## How to use

To get started, clone the repository

```bash
git clone https://github.com/Dellenoam/avescambot-backend.git
```

Create an .env file and fill in the following configuration parameters using the example below

```plaintext
DB__URL = postgresql+asyncpg://username:password@host:port/database_name
COOKIE__SECURE_FLAG = False/True (Choose one)
```

Create private and public encryption keys

```bash
openssl genrsa -out certs/private.pem 4096
openssl rsa -in certs/private.pem -outform PEM -pubout -out certs/public.pem
```

Create a virtual environment and install poetry. I prefer to use venv and install poetry in the virutal environment rather than the global environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install poetry
```

Install dependencies via poetry

```bash
poetry install --only main
```

Hopefully you have created a database and specified the URL to it in .env, if so apply alembic migration to it.

```bash
alembic upgrade head
```

Now you can try to run the server in development mode via the main.py file

```bash
python manage.py runserver
```

Or you can run it on a specific host or port

```bash
python mange.py runserver --host localhost --port 8000
```

### Accessing API Documentation

If you haven't made any changes, you can access the API documentation at

```
http://localhost:8000/docs
```
