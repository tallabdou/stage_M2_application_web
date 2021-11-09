import django_filters
from .models import GG_Sequence_Resume


class GG_Sequence_ResumeFiltre(django_filters.FilterSet):
    class Meta:
        model = GG_Sequence_Resume
        fields =['GG_nr', 'comment']