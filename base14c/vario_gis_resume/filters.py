import django_filters
from .models import Vario_Gis_Resume


class Vario_Gis_ResumeFiltre(django_filters.FilterSet):
    class Meta:
        model = Vario_Gis_Resume
        fields =['measurement_name', 'expected_weight']