from django.db import models
from people.models import People
# Create your models here.

class Research(models.Model):
    project_acronym = models.CharField(max_length=50)
    project_full_name = models.CharField(max_length=250, blank=True)
    project_leader = models.ForeignKey(People, null=True, blank=True, on_delete=models.SET_NULL)
    project_co_leader = models.ForeignKey(People,  null=True, blank=True, related_name="coleader", on_delete=models.SET_NULL)
    WP_leader = models.CharField(max_length=250, blank=True)
    funding_agency = models.CharField(max_length=250, blank=True)
    student_post_doc_name = models.CharField(max_length=250, blank=True)
    academic_level = models.CharField(max_length=250, blank=True)
    main_supervisor = models.CharField(max_length=250, blank=True)
    second_supervisor = models.CharField(max_length=250,  blank=True)

    class Meta:
        db_table = "project_list"

    def __str__(self):
        return self.project_acronym