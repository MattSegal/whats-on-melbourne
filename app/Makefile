
flower-local:
	celery flower \
	--app whatson \
	--broker redis://${CELERY_HOST}:6379 \
	--address=0.0.0.0 \
	--port=5553 \
	--basic_auth="${FLOWER_USER}:${FLOWER_PASSWORD}" \
	--logfile /var/log/flower.log \
	--loglevel info

flower-prod:
	echo "Starting remote syslog" && \
	touch /var/log/flower.log && \
	remote_syslog \
	--hostname $PAPERTRAIL_HOSTNAME \
	--dest-port $PAPERTRAIL_PORT \
	--dest-host $PAPERTRAIL_URL \
	--pid-file /var/run/remote_syslog.pid \
	/var/log/flower.log && \
	echo "Starting celery flower" && \
	celery flower \
	--app whatson \
	--broker redis://${CELERY_HOST}:6379 \
	--address=0.0.0.0 \
	--port=5553 \
	--basic_auth="${FLOWER_USER}:${FLOWER_PASSWORD}" \
	--logfile /var/log/flower.log \
	--loglevel info \
	--url_prefix=flower


worker-local:
	watchmedo \
	auto-restart \
	--directory /app/whatson/ \
	--directory /app/scrapers/ \
	--recursive \
	--pattern '*.py' \
	-- \
	celery worker \
	--broker redis://${CELERY_HOST}:6379 \
	--app whatson \
	--concurrency 10 \
	--beat \
	--loglevel info

worker-prod:
	echo "Starting remote syslog" && \
	touch /var/log/celery.log && \
	remote_syslog \
	--hostname $PAPERTRAIL_HOSTNAME \
	--dest-port $PAPERTRAIL_PORT \
	--dest-host $PAPERTRAIL_URL \
	--pid-file /var/run/remote_syslog.pid \
	/var/log/celery.log && \
	echo "Starting celery" && \
	celery worker \
	--broker redis://${CELERY_HOST}:6379 \
	--app whatson \
	--concurrency 10 \
	--beat \
	--logfile /var/log/celery.log \
	--loglevel info

webpack:
	npm run dev

web-local:
	./manage.py runserver 0.0.0.0:8000

web-prod:
	echo "Starting whatson app as `whoami`" && \
	echo "Starting remote syslog" && \
	mkdir -p /var/log/gunicorn && \
	touch /var/log/gunicorn/access.log && \
	touch /var/log/gunicorn/error.log && \
	remote_syslog \
	--hostname $PAPERTRAIL_HOSTNAME \
	--dest-port $PAPERTRAIL_PORT \
	--dest-host $PAPERTRAIL_URL \
	--pid-file /var/run/remote_syslog.pid \
	/var/log/gunicorn/access.log \
	/var/log/gunicorn/error.log && \
	echo "Running migrations" && \
	./manage.py migrate && \
	echo "Starting gunicorn" && \
	gunicorn whatson.wsgi:application \
	--name whatson \
	--workers 3 \
	--bind 0.0.0.0:8003 \
	--capture-output \
	--log-level info \
	--error-logfile /var/log/gunicorn/error.log \
	--access-logfile /var/log/gunicorn/access.log
