from django.urls import path
from . import views

urlpatterns = [

    path('', views.list_gis_results, name='gis_results'),
    path('ajouter_gis_results', views.ajouter_gis_results, name='ajouter_gis_results'),
    path('<str:pk>/ajouter_gis_results', views.modifier_gis_results, name='modifier_gis_results'),
    path('<str:pk>/supprimer_gis_results', views.supprimer_gis_results, name='supprimer_gis_results'),
    path('upload', views.uploadgis_results, name='uploadgis_results'),

]
