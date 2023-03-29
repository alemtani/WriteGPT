# Getting Started with the Backend

This will teach you how to setup the backend for development.

## Setup

Here is a brief breakdown of all the steps to setting up the backend:
1. [Create the virtual environment](#1-create-the-virtual-environment)
2. [Activate the virtual environment](#2-activate-the-virtual-environment)
3. [Install the required dependencies](#3-install-the-required-dependencies)
4. [Define the environment variables](#4-define-the-environment-variables)

### 1. Create the virtual environment

In the `api` directory, you can run:

```
python3 -m venv venv
```

Creates the virtual environment named `venv` for development.

### 2. Activate the virtual environment

After creating the virtual environment, you can run:

```
source venv/bin/activate
```

Activates the virtual environment.

### 3. Install the required dependencies

Now run:

```
pip install -r requirements.txt
```

Installs the required packages for the project.

### 4. Define the environment variables

In the current `api` directory, create an `.env` file and define the following environment variables:

#### 4a. Keys

Here are the keys you will define:

- `SECRET_KEY`
  - I would suggest choosing a key from [RandomKeygen](https://randomkeygen.com/)
- `OPENAI_API_KEY`
  - You need to get this key from the [OpenAI API](https://openai.com/blog/openai-api)

#### 4b. Integration

These are important for connecting to the database and frontend components of the application

- `DATABASE_URL`
  - This should be of the [format described on SQLAlchemy](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls)
- `CLIENT_NAME`
  - For development, set to `http://localhost:3000`
  - For production, set to the production client name

#### 4c. Email

Here are the variables you need to define below. Follow instructions from the [SendGrid tutorial](https://sendgrid.com/blog/sending-emails-from-python-flask-applications-with-twilio-sendgrid/) to learn how.

- `MAIL_SERVER`
- `MAIL_PORT`
- `MAIL_USE_TLS`
- `MAIL_USERNAME`
- `MAIL_PASSWORD`
- `MAIL_DEFAULT_SENDER`

#### 4d. Debugging

Here is an environment variable you will need to set when debugging from time-to-time:

- `DISABLE_AUTH`
  - In some cases (but **not** all), when you are debugging, you will set this to `True` (in the `.env` file, set to `1`).

## Resources

For more information on the basics of Flask and an introduction to building Flask APIs, please check out the [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

Additionally, for building a practical API and testing it out, you can get inspiration from [this public API](https://github.com/miguelgrinberg/microblog-api).
