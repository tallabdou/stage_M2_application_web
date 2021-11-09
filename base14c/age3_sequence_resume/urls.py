from django.urls import path
from . import views

urlpatterns = [

    path('', views.list_age3_sequence_resume, name='age3_sequence_resume'),
    path('ajouter_age3_sequence_resume', views.ajouter_age3_sequence_resume, name='ajouter_age3_sequence_resume'),
    path('<str:pk>/ajouter_age3_sequence_resume', views.modifier_age3_sequence_resume, name='modifier_age3_sequence_resume'),
    path('<str:pk>/supprimer_age3_sequence_resume', views.supprimer_age3_sequence_resume, name='supprimer_age3_sequence_resume'),
    path('upload', views.uploadage3_sequence_resume, name='uploadage3_sequence_resume'),

]
