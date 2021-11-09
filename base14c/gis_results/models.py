from django.db import models

# Create your models here.
class Gis_Results(models.Model):
    Echo = models.IntegerField(primary_key=True, verbose_name="Echo n°")
    GifA_nr = models.CharField(max_length=100, null=True, blank=True)
    target_comment = models.CharField(max_length=100, null=True, blank=True)
    ratio_14_12 = models.CharField(max_length=100, null=True, blank=True, verbose_name="ratio 14/12")
    erreur_ratio = models.CharField(max_length=100, null=True,  blank=True, verbose_name="erreur ratio (abs)")
    F14C = models.CharField(max_length=100, null=True, blank=True, verbose_name="F14C")
    erreur_F14C = models.FloatField(null=True, blank=True, verbose_name="erreur F14C")
    C14_Age = models.DateField(null=True, blank=True, verbose_name="C14 Age (rounded according to stuiver 1977)")
    age_uncertainty = models.CharField(max_length=50, null=True, blank=True)
    current_12C = models.CharField(max_length=50, null=True, blank=True, verbose_name="12C current (µA)")
    weight_ug_C = models.CharField(max_length=50, null=True, blank=True, verbose_name="weight (µg C)")
    integration_time = models.CharField(max_length=50, null=True, blank=True)
    std_corr = models.CharField(max_length=50, null=True, blank=True)
    blc_corr_F14C = models.CharField(max_length=200, null=True, blank=True, verbose_name="blc corr (F14C)")
    const_cont_masse = models.CharField(max_length=200, null=True, blank=True)

    const_cont_ratio = models.CharField(max_length=50, null=True, blank=True)
    cross_cont = models.CharField(max_length=50, null=True, blank=True)
    d13c = models.CharField(max_length=50, null=True, blank=True)
    GIS_label = models.CharField(max_length=50, null=True, blank=True)
    expected_weight = models.CharField(max_length=200, null=True, blank=True)
    method = models.CharField(max_length=200, null=True, blank=True)
    sample_name = models.CharField(max_length=200, null=True, blank=True)
    smp_position = models.CharField(max_length=200, null=True, blank=True, verbose_name="")

    ugC_measured_bis = models.CharField(max_length=50, null=True, blank=True)
    ugC_kept_bis = models.CharField(max_length=50, null=True, blank=True)
    weighted_sample = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "gis_results"