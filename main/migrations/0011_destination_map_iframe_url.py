# Generated by Django 4.2.19 on 2025-03-03 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_remove_view360_latitude_remove_view360_longitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='map_iframe_url',
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
    ]
