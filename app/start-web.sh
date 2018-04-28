#!/bin/bash
echo "Starting whatson app as `whoami`" && \
echo "Running migrations" && \
./manage.py migrate && \
mkdir -p /var/log/gunicorn && \
echo "Starting gunicorn" && \
gunicorn whatson.wsgi:application \
  --name whatson \
  --workers 3 \
  --bind 0.0.0.0:9000 \
  --capture-output \
  --log-level info \
  --error-logfile /var/log/gunicorn/error.log \
  --access-logfile /var/log/gunicorn/access.log
