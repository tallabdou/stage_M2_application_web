from django.db import models

# Create your models here.
class Paper(models.Model):
    DOI = models.CharField(max_length=250, blank=True,  primary_key=True)
    first_author = models.CharField(max_length=250, blank=True)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    title = models.CharField(max_length=250, blank=True)
    revue = models.CharField(max_length=250, blank=True)

    class Meta:
        db_table = "paper"
