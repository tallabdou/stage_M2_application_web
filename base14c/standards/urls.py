from django.urls import path
from . import views

urlpatterns = [

    path('', views.list_standards, name='standards'),
    path('ajouter_standards', views.ajouter_standards, name='ajouter_standards'),
    path('<str:pk>/ajouter_standards', views.modifier_standards, name='modifier_standards'),
    path('<str:pk>/supprimer_standards', views.supprimer_standards, name='supprimer_standards'),


]
