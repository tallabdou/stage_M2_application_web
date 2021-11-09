from django.db import models

# Create your models here.
class GG_Sequence_Resume(models.Model):
    GG_nr = models.CharField(max_length=50, primary_key=True)
    graph = models.ImageField(null=True, blank=True, upload_to='images/')
    comment = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = "gg_sequence_resume"

    def __str__(self):
        return self.GG_nr
