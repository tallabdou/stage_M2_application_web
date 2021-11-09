# Generated by Django 3.2.3 on 2021-07-22 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('DOI', models.CharField(blank=True, max_length=250, primary_key=True, serialize=False)),
                ('first_author', models.CharField(blank=True, max_length=250)),
                ('year', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=250)),
                ('revue', models.CharField(blank=True, max_length=250)),
            ],
            options={
                'db_table': 'paper',
            },
        ),
    ]