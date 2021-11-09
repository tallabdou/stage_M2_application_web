import django_filters
from .models import People


class PeopleFiltre(django_filters.FilterSet):
    class Meta:
        model = People
        fields =['name', 'first_name', 'affiliation', 'lsce_contact']