from django.db import models
from sample.models import Sample
from sequence.models import Sequence

# Create your models here.
class Sample_Prep(models.Model):
    sample = models.ForeignKey(Sample, null=True, blank=True, on_delete=models.PROTECT)
    preparation_declination = models.CharField(max_length=10, blank=True)
    GifA_prep = models.CharField(max_length=50, unique=True, editable=False, blank=True)
    sequence = models.ForeignKey(Sequence, null=True, blank=True, on_delete=models.PROTECT)
    prep_warning = models.CharField(max_length=250, blank=True)
    comment = models.CharField(max_length=250, blank=True)

    class Meta:
        db_table = "sample_prep"

    def __str__(self):
        return self.GifA_prep
