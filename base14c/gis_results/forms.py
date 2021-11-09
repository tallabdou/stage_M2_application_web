from django.forms import ModelForm
from .models import Gis_Results



class Gis_ResultsForm(ModelForm):
        class Meta:
                model = Gis_Results
                fields='__all__'

