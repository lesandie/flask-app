#!/bin/sh
gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 8 --timeout 0 --worker-class=gthread wsgi:app