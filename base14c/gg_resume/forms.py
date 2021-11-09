from django.forms import ModelForm
from .models import GG_Resume



class GG_ResumeForm(ModelForm):
        class Meta:
                model = GG_Resume
                fields='__all__'

