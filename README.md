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

ver descripcion de la tabla

\d <nombre_tabla>


# Create a Django Project

$python manage.py starproject <project_name>

# Create an app

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


# Translate migrations into SQL commands(Optional)

$python manage.py sqlmigrate <nombre_app> <num_migration>


# Dry run migration (Optional)

#Run migrations

$python manage.py migrate <nombre_app> <num_migration>

#Interactuar con la shell de python(database)

$python manage.py shell

La clase Question es hija de la clase de Django Models.model, que implementa métodos para acceder al contenido de
la base de datos. Django abstrae la conexión de forma que no nos importa qué base de datos usemos

    >>>from encuesta.models import Choice, Question
    >>>Question.objects.all()
        <QuerySet []>

    >>>Choice.objects.all()
        <QuerySet []>

    >>> from django.utils import timezone
    >>> q = Question(question_text="primera pregunta", publication_date=timezone.now())
    >>> dir(q)

    >>> q.save()
    >>> q.id
        1

    >>> Question.objects.all()
        <QuerySet [<Question: Question object (1)>, <Question: Question object (2)>]>

# Cambiamos el método str para ver los objetos human readable

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    publication_date = models.DateTimeField("data published")
    
    def __str__(self):
        return self.question_text

NOTA:
hay que salir de la shell y volver a importar al editar el modelo

    >>> from encuesta.models import Question
    >>> Question.objects.all()
        <QuerySet [<Question: primera pregunta>, <Question: segunda pregunta>, <Question: override question>, <Question: override attempt 2>]>

    >>> Question.objects.filter(id=1)
        <QuerySet [<Question: primera pregunta>]>
    >>> Question.objects.filter(id=2)
        <QuerySet [<Question: segunda pregunta>]>
    >>> Question.objects.filter(question_text="segunda pregunta")
        <QuerySet [<Question: segunda pregunta>]>

