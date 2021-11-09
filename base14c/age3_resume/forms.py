from django.forms import ModelForm
from .models import Age3_Resume



class Age3_ResumeForm(ModelForm):
        class Meta:
                model = Age3_Resume
                fields='__all__'

