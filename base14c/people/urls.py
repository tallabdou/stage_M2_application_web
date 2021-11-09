from django.urls import path
from . import views

urlpatterns = [

    path('', views.list_people, name='people'),
    path('ajouter_people', views.ajouter_people, name='ajouter_people'),
    path('<str:pk>/ajouter_people', views.modifier_people, name='modifier_people'),
    path('<str:pk>/supprimer_people', views.supprimer_people, name='supprimer_people'),
    path('upload', views.uploadpeople, name='uploadpeople'),

]
