# Generated by Django 3.2.3 on 2021-07-22 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gis_Results',
            fields=[
                ('Echo', models.IntegerField(primary_key=True, serialize=False, verbose_name='Echo n°')),
                ('GifA_nr', models.CharField(blank=True, max_length=100, null=True)),
                ('target_comment', models.CharField(blank=True, max_length=100, null=True)),
                ('ratio_14_12', models.CharField(blank=True, max_length=100, null=True, verbose_name='ratio 14/12')),
                ('erreur_ratio', models.CharField(blank=True, max_length=100, null=True, verbose_name='erreur ratio (abs)')),
                ('F14C', models.CharField(blank=True, max_length=100, null=True, verbose_name='F14C')),
                ('erreur_F14C', models.FloatField(blank=True, null=True, verbose_name='erreur F14C')),
                ('C14_Age', models.DateField(blank=True, null=True, verbose_name='C14 Age (rounded according to stuiver 1977)')),
                ('age_uncertainty', models.CharField(blank=True, max_length=50, null=True)),
                ('current_12C', models.CharField(blank=True, max_length=50, null=True, verbose_name='12C current (µA)')),
                ('weight_ug_C', models.CharField(blank=True, max_length=50, null=True, verbose_name='weight (µg C)')),
                ('integration_time', models.CharField(blank=True, max_length=50, null=True)),
                ('std_corr', models.CharField(blank=True, max_length=50, null=True)),
                ('blc_corr_F14C', models.CharField(blank=True, max_length=200, null=True, verbose_name='blc corr (F14C)')),
                ('const_cont_masse', models.CharField(blank=True, max_length=200, null=True)),
                ('const_cont_ratio', models.CharField(blank=True, max_length=50, null=True)),
                ('cross_cont', models.CharField(blank=True, max_length=50, null=True)),
                ('d13c', models.CharField(blank=True, max_length=50, null=True)),
                ('GIS_label', models.CharField(blank=True, max_length=50, null=True)),
                ('expected_weight', models.CharField(blank=True, max_length=200, null=True)),
                ('method', models.CharField(blank=True, max_length=200, null=True)),
                ('sample_name', models.CharField(blank=True, max_length=200, null=True)),
                ('smp_position', models.CharField(blank=True, max_length=200, null=True, verbose_name='')),
                ('ugC_measured_bis', models.CharField(blank=True, max_length=50, null=True)),
                ('ugC_kept_bis', models.CharField(blank=True, max_length=50, null=True)),
                ('weighted_sample', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'gis_results',
            },
        ),
    ]
