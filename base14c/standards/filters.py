import django_filters
from .models import Standards


class StandardsFiltre(django_filters.FilterSet):
    class Meta:
        model = Standards
        fields =['F14C', 'std_number']