import django_filters
from .models import Age3_Resume


class Age3_ResumeFiltre(django_filters.FilterSet):
    class Meta:
        model = Age3_Resume
        fields =['GifA_nr_age3', 'total_sample_weight']