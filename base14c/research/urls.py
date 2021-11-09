from django.urls import path
from . import views

urlpatterns = [

    path('', views.list_research, name='research'),
    path('ajouter_research', views.ajouter_research, name='ajouter_research'),
    path('<str:pk>/ajouter_research', views.modifier_research, name='modifier_research'),
    path('<str:pk>/supprimer_research', views.supprimer_research, name='supprimer_research'),
    path('upload', views.uploadresearch, name='uploadresearch'),
]
