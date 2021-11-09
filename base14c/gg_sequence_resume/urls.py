from django.urls import path
from . import views

urlpatterns = [

    path('', views.list_gg_sequence_resume, name='gg_sequence_resume'),
    path('ajouter_gg_sequence_resume', views.ajouter_gg_sequence_resume, name='ajouter_gg_sequence_resume'),
    path('<str:pk>/ajouter_gg_sequence_resume', views.modifier_gg_sequence_resume, name='modifier_gg_sequence_resume'),
    path('<str:pk>/supprimer_gg_sequence_resume', views.supprimer_gg_sequence_resume, name='supprimer_gg_sequence_resume'),
    path('upload', views.uploadgg_sequence_resume, name='uploadgg_sequence_resume'),

]
