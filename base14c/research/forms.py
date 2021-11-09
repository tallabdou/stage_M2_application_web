from django.forms import ModelForm
from .models import Research


class ResearchForm(ModelForm):
    class Meta:
        model = Research
        fields='__all__'