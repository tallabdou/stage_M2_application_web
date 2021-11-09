import django_filters
from .models import Prep_Step


class Prep_StepFiltre(django_filters.FilterSet):
    class Meta:
        model = Prep_Step
        fields =['work_station', 'sequence']