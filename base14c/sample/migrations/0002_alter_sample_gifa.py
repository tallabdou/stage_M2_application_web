# Generated by Django 3.2.3 on 2021-07-26 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='GifA',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
