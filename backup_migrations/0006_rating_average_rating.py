# Generated by Django 5.0.6 on 2024-07-06 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voyagevista', '0005_remove_rating_average_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='average_rating',
            field=models.FloatField(default=0),
        ),
    ]
