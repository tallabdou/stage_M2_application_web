from django.forms import ModelForm
from .models import Standards



class StandardsForm(ModelForm):
        class Meta:
                model = Standards
                fields='__all__'
