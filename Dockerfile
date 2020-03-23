FROM python:3.8-slim as build

LABEL version="1.0.0"
LABEL maintainer="Alan Placidina Maria <placidina@protonmail.com | placidina@pm.me>"

ADD requirements.txt /tmp/s3dump/

RUN set -ex; \
    cd /tmp/s3dump \
    && pip install -r requirements.txt

ADD . /tmp/s3dump

RUN set -ex; \
    cd /tmp/s3dump \
    && python3 setup.py install

RUN set -ex; \
    rm -rf /tmp/*

ENTRYPOINT [ "s3dump" ]
CMD [ "--help" ]