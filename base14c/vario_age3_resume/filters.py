import django_filters
from .models import Vario_Age3_Resume


class Vario_Age3_ResumeFiltre(django_filters.FilterSet):
    class Meta:
        model = Vario_Age3_Resume
        fields =['measurement_name', 'tin_capsule_lot']