from django.urls import path
from . import views

urlpatterns = [

    path('', views.list_paper, name='paper'),
    path('ajouter_paper', views.ajouter_paper, name='ajouter_paper'),
    path('<str:pk>/ajouter_paper', views.modifier_paper, name='modifier_paper'),
    path('<str:pk>/supprimer_paper', views.supprimer_paper, name='supprimer_paper'),
    path('upload', views.uploadpaper, name='uploadpaper'),

]
