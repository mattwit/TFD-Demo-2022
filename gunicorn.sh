#!/bin/sh

gunicorn --workers 3 --timeout 120 --bind 0.0.0.0:8000 wsgi:app