from django.forms import ModelForm
from .models import Age3_Sequence_Resume



class Age3_Sequence_ResumeForm(ModelForm):
        class Meta:
                model = Age3_Sequence_Resume
                fields='__all__'

