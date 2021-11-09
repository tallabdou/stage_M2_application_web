from django.forms import ModelForm
from .models import Prep_Step



class Prep_StepForm(ModelForm):
        class Meta:
                model = Prep_Step
                fields='__all__'

