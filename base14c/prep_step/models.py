from django.db import models
from sequence.models import Sequence
from people.models import People
from work_station.models import Work_Station
# Create your models here.

class Prep_Step(models.Model):
    work_station = models.ForeignKey(Work_Station, on_delete=models.PROTECT)
    sequence = models.ForeignKey(Sequence, null=True, blank=True, on_delete=models.SET_NULL)
    operator = models.ForeignKey(People, null=True, blank=True, on_delete=models.SET_NULL)
    ending_date = models.DateField(null=True, blank=True, verbose_name="Ending date (DD/MM/YYYY)")


    class Meta:
        db_table = "prep_step"


