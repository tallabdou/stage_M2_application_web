import django_filters
from .models import Work_Station


class Work_StationFiltre(django_filters.FilterSet):
    class Meta:
        model = Work_Station
        fields =['work_bench_description', 'localisation']