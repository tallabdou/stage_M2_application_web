from django.db import models
from age3_sequence_resume.models import Age3_Sequence_Resume

# Create your models here.
class Age3_Resume(models.Model):
    GifA_nr_age3 = models.CharField(max_length=100, blank=True)
    total_sample_weight = models.FloatField(null=True, blank=True, verbose_name="total sample weight (mg)")
    CO2_ug = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="CO2/ug")
    CO2fin_ug = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="CO2fin/ug")
    COH2_mbar = models.PositiveSmallIntegerField(null=True,  blank=True, verbose_name="COH2/mbar")
    Time_min = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Time/min")
    C_percent = models.FloatField(null=True, blank=True, verbose_name="C%")
    T_celsius  = models.IntegerField(null=True, blank=True, verbose_name="T/°C")
    Tset_celsius  = models.IntegerField(null=True, blank=True, verbose_name="Tset/°C")
    p_end_mbar = models.IntegerField(null=True, blank=True, verbose_name="p_end/mbar")
    Sample_date_age3 = models.DateTimeField(max_length=50, null=True, blank=True, verbose_name='Sample_date_age3')
    N_percent = models.FloatField(max_length=50, null=True, blank=True, verbose_name="N%")
    age_nr = models.ForeignKey(Age3_Sequence_Resume, blank=True, null=True, on_delete=models.PROTECT)
    reactor = models.IntegerField(null=True, blank=True)
    tin_capsule_nr = models.IntegerField(null=True,  blank=True)
    pre_or_not = models.BooleanField(blank=True, null=True)
    graphitisation_operator = models.CharField(max_length=50, blank=True)
    graphitisation_comment = models.CharField(max_length=250, blank=True)

    iron_mg = models.FloatField(null=True, blank=True, verbose_name="iron (mg)")
    weighing_operator = models.CharField(max_length=50, blank=True)
    comment_weighing_operator = models.CharField(max_length=50, blank=True)
    press_date = models.DateField(null=True, blank=True)
    press_operator = models.CharField(max_length=50,  blank=True)
    comment_press_operator = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = "age3_resume"
