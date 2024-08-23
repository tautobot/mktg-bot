# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10.14-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
ARG APP_PORT
ARG DEBIAN_FRONTEND=noninteractive

# Copy local code to the container image.
ENV APP_HOME1 /app1
WORKDIR $APP_HOME1

RUN echo DOCKER_BUILD_ID=2024_06_15__1443
COPY ./requirements.txt .
COPY ./.env .

# Install production dependencies.
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install apt-utils -y
RUN apt-get install curl nano rsync gcc -y
RUN apt-get update -y
RUN apt-get upgrade -y

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ensure we have APP_PORT defined
RUN cat ./.env | grep APP_PORT --color=always
RUN if [ -z $(cat ./.env | grep APP_PORT | cut -d'=' -f2) ]; then echo 'APP_PORT is required'; false; fi

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
