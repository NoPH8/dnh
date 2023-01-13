FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV WEB_CONCURRENCY 1

RUN set -ex \
    && APP_DEPS=" \
    make \
    gettext \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $APP_DEPS \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /srv/app

RUN groupadd -r dnh && useradd -r -g dnh dnh -m --uid 1000

WORKDIR /srv/app

COPY requirements.txt /requirements.txt

RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install --no-cache-dir -r /requirements.txt \
    \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

COPY . .

COPY ./contrib/docker/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# chown all the files to the app user
RUN chown -R dnh:dnh /srv/app

EXPOSE 5000

# change to the app user
USER dnh

ENV PATH /home/dnh/.local/bin:$PATH

CMD ["/start"]
