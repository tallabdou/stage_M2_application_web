from django.db import models

# Create your models here.
class Age3_Sequence_Resume(models.Model):
    age_nr = models.CharField(primary_key=True, max_length=50)
    age_graph = models.ImageField(null=True, blank=True, upload_to='images/')
    operator = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=200, blank=True)
    maintenance_date = models.DateField(null=True, blank=True)
    operator_maintenance = models.CharField(max_length=50, blank=True)
    ash = models.IntegerField(null=True, blank=True)
    combustion_colomn = models.IntegerField(null=True, blank=True)
    regenerated_copper_reduction_colomn = models.IntegerField(null=True, blank=True)
    new_copper_reduction_colomn = models.IntegerField(null=True, blank=True)
    sicapent = models.CharField(max_length=250, null=True, blank=True)
    ball_valve = models.FloatField(null=True, blank=True)
    comments = models.CharField(max_length=250, null=True, blank=True)
    O2_pressure = models.CharField(max_length=250, null=True, blank=True)
    He_pressure = models.CharField(max_length=250, null=True, blank=True)
    H2_pressure = models.CharField(max_length=250, null=True, blank=True)
    Ar_pressure = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        db_table = "age3_sequence_resume"

    def __str__(self):
        return self.age_nr