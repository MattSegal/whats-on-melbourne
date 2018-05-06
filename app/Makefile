
flower:
	celery flower \
	--app whatson \
	--broker redis://${CELERY_HOST}:6379 \
	--address=0.0.0.0 \
	--port=5553 \
	--basic_auth="${FLOWER_USER}:${FLOWER_PASSWORD}" \
	--logfile /var/log/flower.log \
	--loglevel info

worker-local:
	celery worker \
	--broker redis://${CELERY_HOST}:6379 \
	--app whatson \
	--beat

worker-prod:
	celery worker \
	--broker redis://${CELERY_HOST}:6379 \
	--app whatson \
	--beat \
	--logfile /var/log/celery.log \
	--loglevel info

webpack:
	npm run dev

web-local:
	./manage.py runserver 0.0.0.0:8000

web-prod:
	echo "Starting whatson app as `whoami`" && \
	echo "Running migrations" && \
	./manage.py migrate && \
	mkdir -p /var/log/gunicorn && \
	echo "Starting gunicorn" && \
	gunicorn whatson.wsgi:application \
	--name whatson \
	--workers 3 \
	--bind 0.0.0.0:8003 \
	--capture-output \
	--log-level info \
	--error-logfile /var/log/gunicorn/error.log \
	--access-logfile /var/log/gunicorn/access.log
