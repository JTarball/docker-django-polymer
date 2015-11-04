<a href="http://www.djangoproject.com/" ><img src="https://www.djangoproject.com/m/img/badges/djangoproject120x25.gif" border="0" alt="A Django project." title="A Django project." style="float: right;" /></a>
## Yeoman generator for Django Polymer projects


## How to run 
We use docker and docker compose to run insolated development and production environments.

For more on docker compose: <a href="https://docs.docker.com/compose/" />

> If on a mac OSX ensure the docker daemon is up. e.g. `boot2docker up`

from root directory 
* `docker-compose up`
    will create the docker containers



### Docker Containers
 - docker-compose.yml    describes the container structure
    backend
    frontend
    postgres
    data - allows us to save the db and load on restart






### Directory Structure

* __app/__

> this is created by __generator-polymer__ Do not move or rename to keep compatible with polymer generator commands

* __bower_components__

> this folder is also created by __generator-polymer__

* __apps/__

> Django apps folder

* __backend/__

> Django Project folder

* __tests/__

> Unit tests folder


### How to get started

