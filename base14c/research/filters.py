import django_filters
from .models import Research


class ResearchFiltre(django_filters.FilterSet):
    class Meta:
        model = Research
        fields =['project_leader', 'project_co_leader']