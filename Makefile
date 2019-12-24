#
# This Makefile contains commands which are run by developers, outside of Docker.
# Most of these commands use the Makefile at ./app/Makefile
#
# If you find yourself running the same docker-compose command over and over,
# then consider adding it here.
#
# Run Django website for local development
web:
	docker-compose up web

# Run Django website for local development
worker:
	docker-compose logs -f --tail 200 worker

# Run Django with debugging enabled
debug:
	docker-compose run --rm --service-ports web

# Get a bash shell in the docker container
bash:
	docker-compose run --rm web bash

# Get a Django shell_plus shell in the docker container
shell:
	docker-compose run --rm web ./manage.py shell_plus

# Get a Postgres shell in the docker container
psql:
	docker-compose run --rm test psql

# Lint frontend and Python code
lint:
	docker-compose run --rm test make lint

format:
	docker-compose run --rm test make format

test:
	docker-compose run --rm test make test
