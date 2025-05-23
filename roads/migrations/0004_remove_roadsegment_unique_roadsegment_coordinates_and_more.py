# Generated by Django 5.2.1 on 2025-05-22 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roads', '0003_remove_speedreading_timestamp'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='roadsegment',
            name='unique_roadsegment_coordinates',
        ),
        migrations.AddConstraint(
            model_name='roadsegment',
            constraint=models.UniqueConstraint(fields=('lat_start', 'long_start', 'lat_end', 'long_end', 'name'), name='unique_roadsegment_coordinates'),
        ),
    ]
