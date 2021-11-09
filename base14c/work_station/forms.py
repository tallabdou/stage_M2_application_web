from django.forms import ModelForm
from .models import Work_Station



class Work_StationForm(ModelForm):
        class Meta:
                model = Work_Station
                fields='__all__'

