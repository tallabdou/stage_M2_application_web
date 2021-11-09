from django.db import models
from gg_sequence_resume.models import GG_Sequence_Resume
# Create your models here.
class GG_Resume(models.Model):
    GG_nr = models.ForeignKey(GG_Sequence_Resume, null=True, blank=True, on_delete=models.PROTECT)
    GifA_nr_GG = models.CharField(max_length=100, blank=True)
    graphitisation_Date = models.DateField(null=True, blank=True)
    Operator = models.CharField(max_length=50, blank=True)
    CO2_line = models.CharField(max_length=50, blank=True)
    P_CO2 = models.CharField(max_length=50, blank=True)
    weigh_mgC = models.FloatField(null=True, blank=True, verbose_name="weigh (mgC)")
    Measured_P_CO2 = models.IntegerField(null=True, blank=True)
    graphitisation_beginning_P  = models.DateTimeField(null=True, blank=True)
    expected_Pfin = models.IntegerField(null=True, blank=True)
    Measured_Pfin = models.IntegerField(null=True, blank=True)
    beginning_hour = models.TimeField(null=True, blank=True)
    ending_hour = models.TimeField(null=True, blank=True)
    line_nr = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=200, blank=True)
    iron_mg = models.CharField(max_length=200, blank=True, verbose_name="iron (mg)")

    weighing_operator = models.CharField(max_length=50,blank=True)
    comment_weighing_operator = models.CharField(max_length=50, blank=True)
    press_date = models.DateField(null=True, blank=True)
    press_operator = models.CharField(max_length=50, blank=True)
    comment_operator = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "gg_resume"