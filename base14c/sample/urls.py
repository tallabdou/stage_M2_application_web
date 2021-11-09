from django.urls import path
from . import views

urlpatterns = [

    path('', views.list_sample, name='sample'),
    path('ajouter_sample', views.ajouter_sample, name='ajouter_sample'),
    path('<str:pk>/ajouter_sample', views.modifier_sample, name='modifier_sample'),
    path('<str:pk>/supprimer_sample', views.supprimer_sample, name='supprimer_sample'),
    path('upload', views.uploadsample, name='uploadsample'),

]
