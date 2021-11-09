import django_filters
from .models import Sample_Prep


class SamplePrepFiltre(django_filters.FilterSet):
    class Meta:
        model = Sample_Prep
        fields =['sample', 'sequence']