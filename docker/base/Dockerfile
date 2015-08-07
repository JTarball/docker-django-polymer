FROM debian:jessie
MAINTAINER James Tarball <james.tarball@gmail.com>

# This code is inspired from the source code:
# https://github.com/smaato/docker-quickstart
# https://www.smaato.com/quickstart-a-web-development-stack-using-vagrant-docker/ 
# 

ENV DEBIAN_FRONTEND noninteractive
ENV APP_DIR /app

# Install node.js, then npm install yo and the generators
RUN apt-get -yq update && \
    apt-get -yq install git curl net-tools sudo bzip2 libpng-dev locales-all \
        build-essential \
        postgresql-contrib \
        npm \
        vim \
        python-dev \
        python \
        python-pip \
        postgresql \
        openssh-server \
        openssh-sftp-server

RUN curl -sL https://deb.nodesource.com/setup_0.12 | bash - && \
    apt-get -yq install nodejs

RUN npm install -g npm@2.13.0 && \
    npm install -g yo@1.4.7 bower@1.4.1 gulp@3.9.0 && \
    npm install -g generator-polymer git://github.com/JTarball/generator-django-polymer.git

# Add a yeoman user because grunt doesn't like being root
RUN adduser --disabled-password --gecos "" yeoman && \
  echo "yeoman ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Expose the port
EXPOSE 9000

# set HOME so 'npm install' and 'bower install' don't write to /
ENV HOME /home/yeoman

ENV LANG en_US.UTF-8

RUN mkdir $APP_DIR && chown yeoman:yeoman $APP_DIR

WORKDIR $APP_DIR 

# Always run as the yeoman user
USER yeoman

CMD /bin/bash