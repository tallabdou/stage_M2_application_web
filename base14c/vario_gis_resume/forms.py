from django.forms import ModelForm
from .models import Vario_Gis_Resume



class Vario_Gis_ResumeForm(ModelForm):
        class Meta:
                model = Vario_Gis_Resume
                fields='__all__'

