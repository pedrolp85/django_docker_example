from django.urls import path 
from . import views 


urlpatterns = [ 
               path("", views.index, name="listado_preguntas"),
               path("<str:question_id>/", views.detail, name = "detalle"),
               path("<int:question_id>/results/", views.results, name = "resultados"),
               path("<int:question_id>/vote/", views.vote, name = "vote"),
            ]