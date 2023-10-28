from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from .models import Question
from .models import Choice

"""
def index(request):
    return HttpResponse("Listado Preguntas")

"""

def index(request):
    listado_ultimas_preguntas = Question.objects.order_by("-publication_date")[:5]
    context = {"listado_ultimas_preguntas": listado_ultimas_preguntas}
    return render(request, "encuesta/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "encuesta/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "encuesta/results.html", {"question": question})


def vote(request, question_id):
    """Registra los votos de cada opción"""
    # question_id -> argumento pasado por un parámetro de la URL
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST["choice"] -> Objeto tipo diccionario que permite acceder a los datos suministrados por el formulario
        # POST -> Método elegido en el formulario
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # En caso de error, recarga la página del formulario.
        return render(
            request,
            "encuesta/detail.html",
            {
                "question": question,
                "error_message": "No ha elegido ninguna opción.",
            },
        )
    else:
        # Al objeto seleccionado le sumamos 1 voto
        selected_choice.votes += 1
        selected_choice.save()
        # Es una buena práctica generar un redirecionamiento. 
        # reverse -> Ahorra tener que codificar un URL. Argumentos: vista y la parte variable del patron url.  
        return HttpResponseRedirect(reverse("encuesta:resultados", args=(question.id,)))
