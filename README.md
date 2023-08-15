# django_docker_example

#Postgres cheatsheet

connect to container:
    docker exec -it <container_postgres> /bin/bash
    $psql -U postgres

list databases:
postgres=#  \l

use database:
postgres=# \c <nombre_db>

show tables
postgres=# \dt+

show users
postgres=# \du


#Create an app

$python manage.py startapp <app_name>

#Add the app to installed apps settings.py:

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'encuesta.apps.EncuestaConfig'
]


#Create new models at <app_name.models.py>

#Create migration files:

$python manage.py makemigrations <app_name>

#Translate migrations into SQL commands

$

#Run migrations

$python manage.py migrate 
