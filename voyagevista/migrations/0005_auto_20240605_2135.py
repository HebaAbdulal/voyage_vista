# Generated by Django 3.2.25 on 2024-06-05 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voyagevista', '0004_auto_20240604_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='post',
            name='number_of_views',
            field=models.IntegerField(default=0),
        ),
    ]
