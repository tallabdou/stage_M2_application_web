from django.forms import ModelForm
from .models import Sample_Prep



class SamplePrepForm(ModelForm):
        class Meta:
                model = Sample_Prep
                fields='__all__'


class SamplePrepForm2(ModelForm):
        class Meta:
                model = Sample_Prep
                fields=['sample', 'preparation_declination']
