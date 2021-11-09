from django.urls import path
from . import views

urlpatterns = [

    path('', views.list_sequence, name='sequence'),
    path('ajouter_sequence', views.ajouter_sequence, name='ajouter_sequence'),
    path('<str:pk>/ajouter_sequence', views.modifier_sequence, name='modifier_sequence'),
    path('<str:pk>/supprimer_sequence', views.supprimer_sequence, name='supprimer_sequence'),
    path('upload', views.uploadsequence, name='uploadsequence'),

]
