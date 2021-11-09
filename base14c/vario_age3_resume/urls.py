from django.urls import path
from . import views

urlpatterns = [

    path('', views.list_vario_age3_resume, name='vario_age3_resume'),
    path('ajouter_vario_age3_resume', views.ajouter_vario_age3_resume, name='ajouter_vario_age3_resume'),
    path('<str:pk>/ajouter_vario_age3_resume', views.modifier_vario_age3_resume, name='modifier_vario_age3_resume'),
    path('<str:pk>/supprimer_vario_age3_resume', views.supprimer_vario_age3_resume, name='supprimer_vario_age3_resume'),
    path('upload', views.uploadvario_age3_resume, name='uploadvario_age3_resume'),

]
