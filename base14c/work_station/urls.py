from django.urls import path
from . import views

urlpatterns = [

    path('', views.list_work_station, name='work_station'),
    path('ajouter_work_station', views.ajouter_work_station, name='ajouter_work_station'),
    path('<str:pk>/ajouter_work_station', views.modifier_work_station, name='modifier_work_station'),
    path('<str:pk>/supprimer_work_station', views.supprimer_work_station, name='supprimer_work_station'),
    path('upload', views.uploadwork_station, name='uploadwork_station'),

]
