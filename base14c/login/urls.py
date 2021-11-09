from django.urls import path
from . import views

urlpatterns = [

    path('inscription', views.InscriptionPage, name='inscription'),
    path('', views.LoginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
]