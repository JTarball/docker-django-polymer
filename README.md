# docker-django-polymer
This is a docker file for django polymer web project.


# How to get started



# Useful Commands

> docker-compose up 
 - this command will create and start containers

> docker rm $(docker ps -a -q); docker rmi $(docker images -q);
 - kill and remove all docker images and containers



> docker stop $(docker ps -a -q); docker rm $(docker ps -a -q); docker rmi $(docker images -q);
> 
> 
> 
> 
> 
> 
> 
> docker run -v /Users/danvir/Masterbox/sideprojects/github/docker-django-polymer/app_mount:/app -i -t dockerdjangopolymer_app_1


# Run tests on app
py.test --ds=project.settings.test  <app dir>
REUSE_DB=0 python manage.py test --settings=project.settings.test -s --with-queries blog