# django_docker_example

# Crear un Proyecto de Django

```console
djangoadmin starproject <project_name>
```


Va a crear:
- Carpeta raíz
- Archivo manage.py

Estructura:

    project_name/
        manage.py
        project_name/
            __init__.py
            settings.py -> ajustes para todo el proyecto
            urls.py     -> URLs para todo el proyecto
            asgi.py
            wsgi.py

# Crear una app

```console
python manage.py startapp <app_name>
```


Crea la estructura de la aplicación dentro del proyecto:

    project_name/
        manage.py
        project_name/
        app_name/
            admin.py -> Panel de aministración 
            apps.py ->  Config de aplicación
            test.py -> tests
            models.py -> Modelos de la base de datos
            views.py  -> Lógica de la aplicación


## Add the app to installed apps settings.py:

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'encuesta.apps.EncuestaConfig'
    ]

# Modelos

De forma muy general: 

- Cada modelo extiende de models.Model
- Cada modelo es una clase que representa una tabla de BBDD
- Cada atributo es una fila de la tabla

Ejemplo: 

    from django.db import models

    class Clientes(models.Model):
        nombre = models.CharField(max_lenght=30)

# Vistas

Son las que contienen la lógica de la aplicación
Reciben una solicitud, la procesan y devuelven una respuesta
Siempre reciben request como argumento

    from django.http import HttpResponse

    def index(request):
        return HttpResponse("Esto es el retorno")


# URLS

Los fichero urls.py asocian las URL a las que llegan las peticiones con un método vista 
La clase include de django sirve para delegar rutas en los urls.py de aplicación

### project_name/urls.py
    urlpatterns = [
        path('admin/', admin.site.urls),
        path("encuesta/", include("encuesta.urls"))
    ]

### app_name/urls.py 
    app_name = "encuesta"

    urlpatterns = [ 
                path("", views.index, name="listado_preguntas"),
                path("<str:question_id>/", views.detail, name = "detalle"),
                ]

## Mapeo de parámetros

    urlpatterns = [ 
                path("", views.index, name="listado_preguntas"),
                path("<str:question_id>/", views.detail, name = "detalle"),
                path("<int:question_id>/results/", views.results, name = "resultados"),
                path("<int:question_id>/vote/", views.vote, name = "vote"),
                ]


Esto es un mapeo de parámetros de url:

    path("<int:question_id>/", views.detail, name = "detalle"),

/polls/1/ -> tiene que ser un entero, va a invocar al método de la vista detail() y se lo pasa como parámetro en la variable question_id

Si ponemos un string: /polls/hola:

    backend_1  | Not Found: /polls/hola/
    backend_1  | [02/Sep/2023 08:49:49] "GET /polls/hola/ HTTP/1.1" 404 2879


Otros convertidores de parámetros

    <str:>
    <slug:> palabras separadas con guiones


# Crear ficheros de migraciónes de BDD

```console
python manage.py makemigrations <app_name>
```


# Translate migrations into SQL commands(Optional)

```console
$python manage.py sqlmigrate <nombre_app> <num_migration>
```


# Dry run migration (Optional)

# Run migrations

```console
python manage.py migrate <nombre_app> <num_migration>
```



# Interactuar con la shell de python(database)

```console
python manage.py shell
```

La clase Question es hija de la clase de Django Models.model, que implementa métodos para acceder al contenido de
la base de datos. Django abstrae la conexión de forma que no nos importa qué base de datos usemos

from encuesta.models import Choice, Question
Question.objects.all()
    <QuerySet []>


Choice.objects.all()
<QuerySet []>

from django.utils import timezone
q = Question(question_text="primera pregunta", publication_date=timezone.now())
dir(q)

q.save()
q.id
1

Question.objects.all()
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


# Working with Models on shell

Offical docs: https://docs.djangoproject.com/en/4.2/topics/db/queries/

# Some examples:

>>> python manage.py shell

# .all() -> Retrieve all objects from a model

(InteractiveConsole)
    >>> from encuesta.models import Question
    >>> from encuesta.models import Choice
    >>> Question.objects.all()



<QuerySet [<Question: primera pregunta>, <Question: segunda pregunta>, <Question: override question>, <Question: override attempt 2>]>

# serializers

>>> from django.core import serializers
>>> from django.core import serializers
>>> datos_json = serializers.serialize("json", Question.objects.all())

>>> datos_json
'[{"model": "encuesta.question", "pk": 1, "fields": {"question_text": "primera pregunta", "publication_date": "2023-08-18T08:05:03.961Z"}}, {"model": "encuesta.question", "pk": 2, "fields": {"question_text": "segunda pregunta", "publication_date": "2023-08-18T08:07:03.607Z"}}, {"model": "encuesta.question", "pk": 3, "fields": {"question_text": "override question", "publication_date": "2023-08-18T08:06:17.031Z"}}, {"model": "encuesta.question", "pk": 4, "fields": {"question_text": "override attempt 2", "publication_date": "2023-08-18T08:11:05.457Z"}}]'

>>> datos_xml = serializers.serialize("xml", Question.objects.all())
>>> datos_xml
'<?xml version="1.0" encoding="utf-8"?>\n<django-objects version="1.0"><object model="encuesta.question" pk="1"><field name="question_text" type="CharField">primera pregunta</field><field name="publication_date" type="DateTimeField">2023-08-18T08:05:03.961214+00:00</field></object><object model="encuesta.question" pk="2"><field name="question_text" type="CharField">segunda pregunta</field><field name="publication_date" type="DateTimeField">2023-08-18T08:07:03.607763+00:00</field></object><object model="encuesta.question" pk="3"><field name="question_text" type="CharField">override question</field><field name="publication_date" type="DateTimeField">2023-08-18T08:06:17.031877+00:00</field></object><object model="encuesta.question" pk="4"><field name="question_text" type="CharField">override attempt 2</field><field name="publication_date" type="DateTimeField">2023-08-18T08:11:05.457455+00:00</field></object></django-objects>'


# .get() -> devuelve un Objeto

>>> q = Question.objects.get(pk=1)

# .count() -> Devuelve el número de objetos

# <related_table_name>_set.all() -> Trae todos los objectos de la tabla relacionada, con la constraint de nuestra instancia

root@6949d2276765:/opt/app# python manage.py shell
(InteractiveConsole)
>>> from encuesta.models import Question
>>> from encuesta.models import Choice
>>> q = Question.objects.get(pk=1)
>>> q.choice_set.all()
<QuerySet [<Choice: Me Gusta votes: 0>, <Choice: regular votes: 0>, <Choice: Mal votes: 0>]>
>>> q.choice_set.count()
    3
>>> Choice.objects.filter(question__publication_date__year=2023)
<QuerySet [<Choice: Me Gusta votes: 0>, <Choice: regular votes: 0>, <Choice: Mal votes: 0>]>

# Crear y guardar un objeto

from django.utils import timezone

q = Question(question_text="Pregunta de ejemplo", publication_date=timezone.now())
q.save()

# Admin Panel

app/encuesta/admin.py

from django.contrib import admin
from .models import Question

admin.site.register(Question)


# Vistas basadas en métodos





## Postgres cheatsheet

### connect to container:

```console
docker exec -it <container_postgres> /bin/bash
psql -U postgres
```

### list databases:

```console
postgres=#  \l
```

### use database:

```console
postgres=# \c <nombre_db>
```
### show tables

```console
postgres=# \dt+
```
### show users

```console
postgres=# \du
```
### ver descripcion de la tabla

```console
\d <nombre_tabla>
```