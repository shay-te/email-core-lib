FROM python:3.8-slim-buster

ENV PYTHONPATH=/app

ARG UNAME=app
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME

WORKDIR app
COPY . .

RUN apt-get update && apt-get -qq -o=Dpkg::Use-Pty=0 install -y --no-install-recommends libpq-dev build-essential

RUN pip install ./dependencies_builds/core_lib-0.0.0.9-py3-none-any.whl --quiet
RUN pip install -r requirements.txt --quiet

EXPOSE 8880