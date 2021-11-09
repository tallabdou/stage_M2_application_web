from django.urls import path
from . import views

urlpatterns = [

    path('', views.list_gg_resume, name='gg_resume'),
    path('ajouter_gg_resume', views.ajouter_gg_resume, name='ajouter_gg_resume'),
    path('<str:pk>/ajouter_gg_resume', views.modifier_gg_resume, name='modifier_gg_resume'),
    path('<str:pk>/supprimer_gg_resume', views.supprimer_gg_resume, name='supprimer_gg_resume'),
    path('upload', views.uploadgg_resume, name='uploadgg_resume'),

]
