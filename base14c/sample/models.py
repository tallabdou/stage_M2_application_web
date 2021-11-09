from django.db import models
from research.models import Research
from people.models import People
from paper.models import Paper
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Sample(models.Model):
    theme=(('archeology', 'archeology'),('continental', 'continental'), ('marine (paleoclimatology)', 'marine (paleoclimatology)'),
           ('heritage sciences', 'heritage sciences'),('cycle-in-natura', 'cycle-in-natura'), ('cycle-ex-natura', 'cycle-ex-natura'),
           ('other', 'other'),('standard', 'standard'))
    GifA = models.IntegerField(primary_key=True)
    sample_reference_blank = models.CharField(max_length=50, blank=True)
    user_sample_description = models.CharField(max_length=250, blank=True)
    submitter_1_id = models.ForeignKey(People,  null=True, blank=True, on_delete=models.SET_NULL)
    submitter_2_id = models.ForeignKey(People,  null=True, blank=True, related_name="submitter2", on_delete=models.SET_NULL)
    project_id = models.ForeignKey(Research,   null=True, on_delete=models.SET_NULL, blank=True)
    contact_lsce_id = models.ForeignKey(People,  null=True, blank=True, related_name="contact_lsce", on_delete=models.SET_NULL, limit_choices_to = {'lsce_contact': True})
    receipt_date = models.DateField(null=True, blank=True, verbose_name="Receipt date (YYYY-MM-DD)")
    expected_age = models.CharField(max_length=50, blank=True)
    expected_F14C = models.CharField(max_length=50, blank=True)
    further_information_concerning_sample = models.CharField(max_length=50, blank=True)
    research_thematic = models.CharField(max_length=50, blank=True, choices=theme)
    link_between_GifAs = models.PositiveIntegerField(null=True, blank=True)
    link_comment = models.CharField(max_length=200, blank=True)
    collec_science = models.CharField(max_length=200, blank=True)
    paper = models.ForeignKey(Paper,  null=True, blank=True, on_delete=models.SET_NULL)

    ocean_sea = models.CharField(max_length=250, blank=True)
    profile_core_name = models.CharField(max_length=250, blank=True, verbose_name="profile/core name")
    sampling_core_depth_cm = models.PositiveIntegerField(null=True, blank=True)
    cruise_name = models.CharField(max_length=250, blank=True)
    vessel = models.CharField(max_length=250, blank=True)
    country = CountryField(null=True, blank=True)
    state_province_departement = models.CharField(max_length=250, blank=True, verbose_name="state/province/département")
    city = models.CharField(max_length=250, blank=True)
    site_name = models.CharField(max_length=250, blank=True, verbose_name="site name / institution name")


    longitude = models.FloatField(validators=[MaxValueValidator(180),MinValueValidator(-180)], blank=True,  null=True, verbose_name="Longitude (-180°(W) to +180°(E))")
    latitude = models.FloatField(validators=[MaxValueValidator(90),MinValueValidator(-90)], blank=True,  null=True, verbose_name="Latitude (-90°(S) to +90°(N))")
    altitude = models.IntegerField(null=True, blank=True, verbose_name="Altitude [m]")
    depth = models.PositiveIntegerField(null=True, blank=True, verbose_name="Depth [m]")
    short_geographical_description = models.CharField(max_length=250, blank=True, verbose_name="Short geographical description (inc. geological settlement)")
    associated_documents = models.URLField(max_length=250, blank=True,  null=True, verbose_name="Associated documents (inc. article, fieldwork report, project proposal, …")
    further_information = models.CharField(max_length=250, blank=True,  null=True)

    fieldwork_cruise_date = models.DateField(null=True, blank=True, verbose_name="fieldwork/cruise_date (DD/MM/YYYY)")
    collected_field_by = models.CharField(max_length=250, blank=True, verbose_name="Collected on field by")

    experiment_type= models.CharField(max_length=250, blank=True, verbose_name="Experiment_type (incubation, greenhouse, …)")
    experiment_leader = models.CharField(max_length=250, blank=True)
    short_experiment_description = models.CharField(max_length=250, blank=True)
    managing_organization = models.CharField(max_length=250, blank=True)
    institution_name = models.CharField(max_length=250, blank=True)
    further_information_2 = models.CharField(max_length=250, blank=True)


    sampling_depth = models.CharField(max_length=250, blank=True, verbose_name="Sampling depth (cm)")
    object_ID = models.CharField(max_length=250, blank=True)
    description = models.CharField(max_length=250, blank=True)
    sample_type = models.CharField(max_length=250, blank=True, verbose_name="Sample's type")
    sample_fraction_analysed = models.CharField(max_length=250, blank=True, verbose_name="Sample fraction to be analysed")
    additional_information_material = models.CharField(max_length=250, blank=True, verbose_name="Additional information about material")
    raw_sample_weight = models.FloatField(null=True, blank=True, verbose_name="raw_sample_weight [mg]")
    potential_contamination = models.CharField(max_length=250, blank=True)
    collection_protocol = models.CharField(max_length=250, blank=True, verbose_name="Collection protocol (inc. chemicals description)")
    further_information_3 = models.CharField(max_length=250, blank=True)

    sub_sampling_date = models.DateField(max_length=250,  null=True, blank=True)
    sub_sample_collected_by = models.CharField(max_length=250, blank=True)
    sub_sample_identified_by = models.CharField(max_length=250, blank=True)
    nature_fraction_be_analyse = models.CharField(max_length=250, blank=True, verbose_name="Nature fraction to be analyse")
    date_sub_sampling = models.DateField(max_length=250, null=True, blank=True, verbose_name="Date of sub-sampling")
    sub_sample_collection_protocol = models.CharField(max_length=250, blank=True)
    subsample_weight_mg = models.CharField(max_length=250, blank=True, verbose_name="Subsample_weight_[mg]")

    class Meta:
        db_table = "sample"


    def __str__(self):
        return str(self.GifA)
