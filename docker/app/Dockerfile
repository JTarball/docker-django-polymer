FROM jtarball/docker-base:latest
MAINTAINER James Tarball <james.tarball@gmail.com>

ENV ENV_TYPE dev
ENV APP_DIR /app

ADD requirements /requirements

ENTRYPOINT sudo pip install -r /requirements/$ENV_TYPE.txt && \
    #psql -u root -proot -Bse "CREATE DATABASE IF NOT EXISTS backend;" && \
    #python $APP_DIR/manage.py migrate && \
    #python $APP_DIR/manage.py collectstatic --noinput && \
    #if [ $ENV_TYPE == "dev" ]; then python $APP_DIR/manage.py runserver_plus 0.0.0.0:8000; else  python $APP_DIR/backend/bin/run.py ; fi

EXPOSE 8000