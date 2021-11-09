from django.db import models

# Create your models here.
class Work_Station(models.Model):
    work_bench_ID = models.PositiveIntegerField(primary_key=True)
    work_bench_description = models.CharField(max_length=100, null=True, blank=True)
    localisation = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        db_table = "work_station"

    def __str__(self):
        return self.work_bench_description


