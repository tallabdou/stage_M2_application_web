import django_filters
from .models import Sample

from django.db.models import Q

class SampleFiltre(django_filters.FilterSet):
    GifA = django_filters.CharFilter(lookup_expr='icontains', label='GifA')
    user_sample_description = django_filters.CharFilter(lookup_expr='icontains', label='user_sample_description')
    country = django_filters.CharFilter(lookup_expr='icontains', label='country')
    submitter = django_filters.CharFilter(method='my_submitter_filter', label='Id submitter')

    date_inf = django_filters.CharFilter(method='my_date_inf', label='YYYY-MM-DD < ')
    date_sup = django_filters.CharFilter(method='my_date_sup', label='YYYY-MM-DD > ')
    sample_type = django_filters.CharFilter(lookup_expr='icontains', label='sample_type')
    nature_fraction_be_analyse = django_filters.CharFilter(lookup_expr='icontains', label='nature_fraction_be_analyse')
    longitude_min = django_filters.CharFilter(method='my_longitude_min', label='longitude min')
    longitude_max = django_filters.CharFilter(method='my_longitude_max', label='longitude max')
    latitude_min = django_filters.CharFilter(method='my_latitude_min', label='longitude min')
    latitude_max = django_filters.CharFilter(method='my_latitude_max', label='longitude max')
    class Meta:
        model = Sample
        fields =['GifA','sample_reference_blank', 'user_sample_description', 'submitter_1_id', 'submitter_2_id', 'submitter', 'project_id', 'date_inf', 'date_sup',
                 'research_thematic','link_comment', 'profile_core_name', 'cruise_name', 'country', 'institution_name',
                 'sample_type', 'sample_fraction_analysed', 'nature_fraction_be_analyse',
                 'longitude_min', 'longitude_max', 'latitude_min', 'latitude_max' ]

    def my_submitter_filter(self, queryset, name, value):
        return Sample.objects.filter(
        Q(submitter_1=value) | Q(submitter_2=value))

    def my_date_inf(self, queryset, name, value):
        return Sample.objects.filter(
            Q(receipt_date__lt=value))

    def my_date_sup(self, queryset, name, value):
        return Sample.objects.filter(
            Q(receipt_date__gt=value))

    def my_longitude_min(self, queryset, name, value):
        return Sample.objects.filter(longitude__lte=value)
    def my_longitude_max(self, queryset, name, value):
        return Sample.objects.filter(longitude__gte=value)
    def my_latitude_min(self, queryset, name, value):
        return Sample.objects.filter(latitude__lte=value)
    def my_latitude_max(self, queryset, name, value):
        return Sample.objects.filter(latitude__gte=value)

