FROM jtarball/docker-base:latest
MAINTAINER James Tarball <james.tarball@gmail.com>

ENV ENV_TYPE dev
ENV APP_DIR /app

# https://github.com/docker/docker/issues/12084  HACKS FOR TIMEZONE

#ADD requirements /requirements

#RUN sudo pip install -r /requirements/$ENV_TYPE.txt

#ENTRYPOINT cp -r /app /src
    #sudo pip install -r /requirements/$ENV_TYPE.txt && \
    #psql -u root -proot -Bse "CREATE DATABASE IF NOT EXISTS backend;" && \
CMD python manage.py makemigrations && \
    python /app/backend/manage.py migrate && \
    python /app/backend/manage.py collectstatic --noinput && \
    python /app/backend/manage.py runserver_plus 0.0.0.0:8000 & gulp serve


#python -c 'import generateproject; print generateproject.create_superuser()'
#ENTRYPOINT gulp serve

#ENTRYPOINT if "$ENV_TYPE" == "dev" ; then python /app/backend/bin/run.py; else  python /app/backend/manage.py runserver_plus 0.0.0.0:8000; fi

#EXPOSE 8000