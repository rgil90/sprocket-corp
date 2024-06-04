FROM python:3.10 as base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip setuptools wheel \
    && mkdir -p /usr/src/app

WORKDIR /usr/src/app
EXPOSE 8000

FROM base AS dev
COPY ./requirements/ /usr/src/app/requirements/
RUN pip install -r requirements/dev.txt --default-timeout=100
ARG APP_VERSION
ENV APP_VERSION=$APP_VERSION
COPY . /usr/src/app/
