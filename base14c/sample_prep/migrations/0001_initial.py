# Generated by Django 3.2.3 on 2021-07-22 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sequence', '0001_initial'),
        ('sample', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sample_Prep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preparation_declination', models.CharField(blank=True, max_length=10)),
                ('GifA_prep', models.CharField(blank=True, editable=False, max_length=50, unique=True)),
                ('prep_warning', models.CharField(blank=True, max_length=250)),
                ('comment', models.CharField(blank=True, max_length=250)),
                ('sample', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='sample.sample')),
                ('sequence', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='sequence.sequence')),
            ],
            options={
                'db_table': 'sample_prep',
            },
        ),
    ]
