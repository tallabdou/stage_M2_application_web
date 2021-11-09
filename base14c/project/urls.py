"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('login.urls')),
    path('sample/', include('sample.urls')),
    path('people/', include('people.urls')),
    path('research/', include('research.urls')),
    path('sample_prep/', include('sample_prep.urls')),
    path('age3_resume/', include('age3_resume.urls')),
    path('age3_sequence_resume/', include('age3_sequence_resume.urls')),
    path('gg_resume/', include('gg_resume.urls')),
    path('gg_sequence_resume/', include('gg_sequence_resume.urls')),
    path('gis_results/', include('gis_results.urls')),
    path('paper/', include('paper.urls')),
    path('prep_step/', include('prep_step.urls')),
    path('sequence/', include('sequence.urls')),
    path('standards/', include('standards.urls')),
    path('vario_age3_resume/', include('vario_age3_resume.urls')),
    path('vario_gis_resume/', include('vario_gis_resume.urls')),
    path('work_station/', include('work_station.urls')),
]


from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)