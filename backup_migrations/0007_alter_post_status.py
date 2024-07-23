# Generated by Django 5.0.6 on 2024-07-18 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voyagevista', '0006_rating_average_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending Approval'), ('approved', 'Approved')], default='pending', max_length=10),
        ),
    ]