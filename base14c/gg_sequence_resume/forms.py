from django.forms import ModelForm
from .models import GG_Sequence_Resume



class GG_Sequence_ResumeForm(ModelForm):
        class Meta:
                model = GG_Sequence_Resume
                fields='__all__'

