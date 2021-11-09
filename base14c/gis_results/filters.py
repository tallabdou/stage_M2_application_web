import django_filters
from .models import Gis_Results


class Gis_ResultsFiltre(django_filters.FilterSet):
    class Meta:
        model = Gis_Results
        fields =['GifA_nr', 'ratio_14_12']