# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.

COPY ./hello /hello
WORKDIR /hello

#ENVs for postgresql database
ARG PG_DATABASE
ARG PG_PORT
ARG PG_USER
ARG PG_PASS
ARG PG_HOST

ENV POSTGRES_DB=${PG_DATABASE}
ENV POSTGRES_PORT=${PG_PORT}
ENV POSTGRES_USER=${PG_USER}
ENV POSTGRES_PASSWORD=${PG_PASS}
ENV POSTGRES_HOST=${PG_HOST}

#
ENV PORT 6000

# Install production dependencies.
RUN pip install --no-cache-dir -r /hello/requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
#CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 helloapp:app
ENTRYPOINT ["./gunicorn.sh"]