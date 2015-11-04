FROM jtarball/docker-base:latest
MAINTAINER James Tarball <james.tarball@gmail.com>

ENV ENV_TYPE dev
ENV APP_DIR /app

#ONBUILD COPY requirements $BUILD_DIR/requirements
#ONBUILD RUN sudo pip install -r $BUILD_DIR/requirements/$ENV_TYPE.txt

#ADD requirements /requirements

#RUN sudo pip install -r /requirements/$ENV_TYPE.txt

#ENTRYPOINT cp -r /app /src
    #sudo pip install -r /requirements/$ENV_TYPE.txt && \
    #psql -u root -proot -Bse "CREATE DATABASE IF NOT EXISTS backend;" && \
ENTRYPOINT python /app/backend/manage.py migrate && \
    python /app/backend/manage.py collectstatic --noinput && \
    python /app/backend/manage.py runserver_plus 0.0.0.0:8000 
    #&& \
    #/app/gulp

#ENTRYPOINT if "$ENV_TYPE" == "dev" ; then python /app/backend/bin/run.py; else  python /app/backend/manage.py runserver_plus 0.0.0.0:8000; fi

#EXPOSE 8000