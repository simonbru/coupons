FROM alpine:3.6

ENV DEPLOY_PATH /app/

WORKDIR $DEPLOY_PATH

# system dependencies
RUN apk add --update \
        nginx uwsgi-python3 supervisor \
        python3 gettext \
        ca-certificates \
        # Needed by django-compressor and postcss
        # Because the compression step is done for each build, we
        # decide to sacrifice a bit of image size to save a lot of time.
        nodejs yarn libxslt \
    && rm -rf /var/cache/apk/*

# python dependencies
ADD requirements.txt $DEPLOY_PATH
RUN apk add --update --virtual=build-deps \
            g++ git python3-dev \
            libxml2-dev libxslt-dev libjpeg-turbo-dev \
    && pip3 install -r $DEPLOY_PATH/requirements.txt \
    && apk del --purge build-deps \
    && rm -rf /var/cache/apk/*

# js dependencies
ADD package.json $DEPLOY_PATH
ADD yarn.lock $DEPLOY_PATH
RUN yarn install

ADD prod $DEPLOY_PATH/prod
ADD mcdo_coupons $DEPLOY_PATH/mcdo_coupons
ADD coupons $DEPLOY_PATH/coupons
ADD manage.py $DEPLOY_PATH

RUN rm /etc/nginx/nginx.conf \
    && ln -s $DEPLOY_PATH/prod/nginx.conf /etc/nginx/ \
    && ln -s $DEPLOY_PATH/prod/supervisor.d /etc/


ARG SECRET_KEY=dummykey
RUN python3 manage.py compress --force \
    && python3 manage.py collectstatic --noinput

# prepare nginx and uWSGI to run as www-data user
RUN adduser -S www-data \
    && mkdir $DEPLOY_PATH/run \
    && chown -R www-data.www-data /var/lib/nginx $DEPLOY_PATH/run

EXPOSE 80

VOLUME $DEPLOY_PATH/db
VOLUME $DEPLOY_PATH/logs

ENTRYPOINT ["/app/prod/entrypoint.sh"]

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisord.conf"]