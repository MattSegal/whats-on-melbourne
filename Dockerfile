FROM ubuntu:latest

WORKDIR /app

RUN \
	echo "Updating apt sources." && \
    apt-get -qq update && \
    echo "Installing required packages." && \
    apt-get -qq install \
        python3 \
        python3-setuptools \
        python3-dev \
       	python3-pip \
       	postgresql-client \
       	postgresql-common \
        iputils-ping \
        curl

# Install NodeJS and NPM
RUN \
  curl -sL https://deb.nodesource.com/setup_9.x | bash - && \
  apt-get -qq install nodejs build-essential  && \
  npm install npm@latest -g

# Install Python packages
COPY app/requirements.txt .
RUN \
	echo "Installing python packages..." && \
  pip3 install -r requirements.txt

# Install NPM packages
COPY app/package.json .
RUN npm install && npm cache --force clean

# Mount the codebase
ADD app /app

# Run frontend build
RUN npm run prod

ARG DJANGO_SETTINGS_MODULE=whatson.settings.prod
ARG DJANGO_SECRET_KEY=not-a-secret
RUN mkdir -p /static/ && ./manage.py collectstatic --noinput
