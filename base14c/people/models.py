from django.db import models
from phone_field import PhoneField


# Create your models here.

class People(models.Model):
    name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    affiliation = models.CharField(max_length=250, blank=True)
    address = models.CharField(max_length=250, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = PhoneField(null=True, blank=True)
    lsce_contact = models.BooleanField()

    class Meta:
        ordering = ['name']
        db_table = "people"

    def __str__(self):
        return f'{self.name} {self.first_name}'
