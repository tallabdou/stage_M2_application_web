from django.forms import ModelForm
from .models import Sequence



class SequenceForm(ModelForm):
        class Meta:
                model = Sequence
                fields='__all__'

