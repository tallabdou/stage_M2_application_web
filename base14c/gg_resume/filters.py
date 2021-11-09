import django_filters
from .models import GG_Resume


class GG_ResumeFiltre(django_filters.FilterSet):
    class Meta:
        model = GG_Resume
        fields =['GG_nr', 'GifA_nr_GG']