# Generated by Django 4.2.19 on 2025-02-25 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_destination_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='view360',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='view360',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='view360',
            name='pano_id',
            field=models.CharField(blank=True, help_text='Google Street View Panorama ID', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='view360',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='360_views/'),
        ),
    ]
