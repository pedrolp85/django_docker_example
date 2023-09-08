from django.shortcuts import render
from django.http import HttpResponse

from .models import Question

"""
def index(request):
    return HttpResponse("Listado Preguntas")

"""

def index(request):
    listado_ultimas_preguntas = Question.objects.order_by("-publication_date")[:5]
    context = {"listado_ultimas_preguntas": listado_ultimas_preguntas}
    return render(request, "encuesta/index.html", context)

def detail(request, question_id):
    return HttpResponse(f'Estás viendo una pregunta {question_id}')


def results(request, question_id):
    response = f'Estás viendo los resultados de una pregunta'
    return HttpResponse(response.format(question_id))


def vote(request, question_id):
    return HttpResponse(f'Estás votando una pregunta {question_id}')