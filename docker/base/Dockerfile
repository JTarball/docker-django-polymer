FROM debian:jessie
MAINTAINER James Tarball <james.tarball@gmail.com>

# This code is inspired from the source code:
# https://github.com/smaato/docker-quickstart
# https://www.smaato.com/quickstart-a-web-development-stack-using-vagrant-docker/ 
# 

ENV DEBIAN_FRONTEND noninteractive
ENV APP_DIR /app
ENV BUILD_DIR /tmp
ENV ENV_TYPE dev

# Basic stuff...
RUN apt-get -yq update && \
    apt-get -yq install git curl net-tools sudo bzip2 libpng-dev locales-all \
        build-essential \
        postgresql-contrib \
        npm \
        vim \
        bash-completion \ 
        python-dev \
        python \
        python-pip \
        postgresql \
        python-psycopg2 \
        openssh-server \
        openssh-sftp-server

# Install node.js, then npm install yo and the generators
RUN curl -sL https://deb.nodesource.com/setup_0.12 | bash - && \
    apt-get -yq install nodejs

RUN npm install -g npm@2.13.0 && \
    npm install -g gulp && \
    npm install -g yo@1.4.7 bower@1.4.1 gulp@3.9.0 && \
    npm install -g generator-polymer git://github.com/JTarball/generator-django-polymer.git

# Set the timezone.
RUN sudo echo "Europe/London" > /etc/timezone
RUN sudo dpkg-reconfigure -f noninteractive tzdata

# Add a yeoman user because grunt etc. doesn't like being root
RUN adduser --disabled-password --gecos "" yeoman && \
  echo "yeoman ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# set HOME so 'npm install' and 'bower install' don't write to /
ENV HOME /home/yeoman
ENV LANG en_GB.UTF-8

RUN mkdir -p $APP_DIR
RUN mkdir -p $BUILD_DIR
WORKDIR $APP_DIR

RUN chown yeoman:yeoman $APP_DIR
RUN chown yeoman:yeoman $BUILD_DIR

# Always run as the yeoman user - YO commands will not work otherwises!
USER yeoman

# To stop boiler-plate code, specify some on build commands
# 1. install pip requirements  - install requirements based on environment type (dev/production)
# 2. copy generate-project.py  - generates a new project for you!
# 3. copy app folder           - code source code (you can then mount using docker-compose for development)
ONBUILD COPY requirements $BUILD_DIR/requirements
ONBUILD RUN sudo pip install -r $BUILD_DIR/requirements/$ENV_TYPE.txt
ONBUILD COPY generate-project.py $BUILD_DIR/generate-project.py
ONBUILD COPY app $APP_DIR

VOLUME $APP_DIR

CMD /bin/bash


