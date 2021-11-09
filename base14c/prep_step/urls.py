from django.urls import path
from . import views

urlpatterns = [

    path('', views.list_prep_step, name='prep_step'),
    path('ajouter_prep_step', views.ajouter_prep_step, name='ajouter_prep_step'),
    path('<str:pk>/ajouter_prep_step', views.modifier_prep_step, name='modifier_prep_step'),
    path('<str:pk>/supprimer_prep_step', views.supprimer_prep_step, name='supprimer_prep_step'),
    path('upload', views.uploadprep_step, name='uploadprep_step'),

]
