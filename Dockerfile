# syntax = docker/dockerfile:1.3

FROM python:3.9-slim

# ENVs are built bith buildkit and into secret ENVs


ENV POSTGRES_DB=tests
ENV POSTGRES_PORT=5432
ENV POSTGRES_USER=test
ENV POSTGRES_PASSWORD=test
ENV POSTGRES_HOST=192.168.11.149

# listening port
ENV PORT=6000

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ADD hello /hello
WORKDIR /hello

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
ENTRYPOINT ["./gunicorn.sh"]