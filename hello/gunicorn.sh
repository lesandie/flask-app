#!/bin/sh
gunicorn --bind 0.0.0.0:6000 --workers 1 --threads 8 --timeout 0 helloapp:app