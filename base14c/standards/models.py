from django.db import models

# Create your models here.
class Standards(models.Model):
    std_number = models.CharField(max_length=250, primary_key=True)
    standard_name = models.CharField(max_length=250, blank=True)
    F14C = models.CharField(max_length=250, blank=True)
    uncertainty_F14C = models.CharField(max_length=250, blank=True)
    age = models.CharField(max_length=250, blank=True)
    uncertainty_age = models.CharField(max_length=250, blank=True)
    d13C = models.CharField(max_length=250, blank=True)
    uncertainty_d13C = models.CharField(max_length=250,  blank=True)
    material = models.CharField(max_length=250,  blank=True)
    description = models.CharField(max_length=250, blank=True)
    comment = models.CharField(max_length=250,  blank=True)

    class Meta:
        db_table = "standards"
