import django_filters
from .models import Sequence


class SequenceFiltre(django_filters.FilterSet):
    class Meta:
        model = Sequence
        fields =['sequence_ID', 'sequence_name']