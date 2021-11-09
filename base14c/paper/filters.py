import django_filters
from .models import Paper


class PaperFiltre(django_filters.FilterSet):
    class Meta:
        model = Paper
        fields =['DOI', 'first_author']