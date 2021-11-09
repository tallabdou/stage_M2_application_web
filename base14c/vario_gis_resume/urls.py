from django.urls import path
from . import views

urlpatterns = [

    path('', views.list_vario_gis_resume, name='vario_gis_resume'),
    path('ajouter_vario_gis_resume', views.ajouter_vario_gis_resume, name='ajouter_vario_gis_resume'),
    path('<str:pk>/ajouter_vario_gis_resume', views.modifier_vario_gis_resume, name='modifier_vario_gis_resume'),
    path('<str:pk>/supprimer_vario_gis_resume', views.supprimer_vario_gis_resume, name='supprimer_vario_gis_resume'),
    path('upload', views.uploadvario_gis_resume, name='uploadvario_gis_resume'),

]
