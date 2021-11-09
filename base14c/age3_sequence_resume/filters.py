import django_filters
from .models import Age3_Sequence_Resume


class Age3_Sequence_ResumeFiltre(django_filters.FilterSet):
    class Meta:
        model = Age3_Sequence_Resume
        fields =['age_nr', 'operator']