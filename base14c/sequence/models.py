from django.db import models

# Create your models here.
class Sequence(models.Model):
    sequence_ID = models.CharField(max_length=50,primary_key=True)
    sequence_name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)
    comment = models.CharField(max_length=250, blank=True)


    def __str__(self):
        return f'{self.sequence_name} {self.description}'


    class Meta:
        db_table = "sequence"