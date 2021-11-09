from django.urls import path
from . import views

urlpatterns = [

    path('', views.list_sample_prep, name='sample_prep'),
    path('ajouter_sample_prep', views.ajouter_sample_prep, name='ajouter_sample_prep'),
    path('last_sample_prep', views.last_sample_prep, name='last_sample_prep'),
    path('<str:pk>/ajouter_sample_prep', views.modifier_sample_prep, name='modifier_sample_prep'),
    path('<str:pk>/supprimer_sample_prep', views.supprimer_sample_prep, name='supprimer_sample_prep'),
    path('upload_sampleprep', views.uploadsample_prep, name='uploadsample_prep'),

]
