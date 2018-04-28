#!/bin/bash
celery worker \
	--broker redis://$CELERY_HOST:6379 \
	--app whatson \
	--logfile /var/log/celery.log \
	--loglevel info
