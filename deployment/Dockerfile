ARG DOCKER_REGISTRY=""
FROM ${DOCKER_REGISTRY}python:3.11-slim-bookworm

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies \
  && apt-get install -y default-libmysqlclient-dev \
  && apt-get install -y pkg-config \
  && apt-get install -y gettext \
  && apt-get install -y git \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
WORKDIR /app/
ADD /config/requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
