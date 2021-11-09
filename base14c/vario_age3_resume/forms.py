from django.forms import ModelForm
from .models import Vario_Age3_Resume



class Vario_Age3_ResumeForm(ModelForm):
        class Meta:
                model = Vario_Age3_Resume
                fields='__all__'

