from django.db import models

# Create your models here.
class Vario_Gis_Resume(models.Model):
    measurement_name = models.CharField(max_length=50, blank=True)
    tin_capsule_lot = models.CharField(max_length=50, blank=True)
    expected_weight = models.CharField(max_length=50, blank=True, verbose_name="expected weight (mg)")
    weighing_operator =models.CharField(max_length=50, blank=True)
    weighing_date = models.DateField(null=True, blank=True, verbose_name="weighing date (DD/MM/YYYY)")
    weight = models.CharField(max_length=50, blank=True, verbose_name="weight (mg)")
    Vario_measurement_name = models.CharField(max_length=50, blank=True)
    humidity = models.FloatField(null=True,  blank=True)
    N_area = models.FloatField(null=True, blank=True, verbose_name="N area")
    C_area = models.FloatField(null=True, blank=True, verbose_name="C area")
    n_percent = models.FloatField(null=True, blank=True, verbose_name="N%")
    c_percent = models.FloatField(null=True, blank=True, verbose_name="C%")
    C_N_ratio = models.FloatField(null=True, blank=True, verbose_name="C/N ratio")
    method = models.CharField(max_length=200, null=True, blank=True)
    N_factor = models.FloatField(null=True, blank=True)
    C_factor = models.FloatField(null=True, blank=True)
    N_blk = models.FloatField(null=True, blank=True)
    C_blk = models.FloatField(null=True, blank=True)
    Memo = models.CharField(max_length=200, null=True, blank=True)
    info = models.CharField(max_length=200, null=True, blank=True)
    vario_gis_date = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = "vario_gis_resume"