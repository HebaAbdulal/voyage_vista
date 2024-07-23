from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('voyagevista', '0010_update_status_to_integers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.IntegerField(choices=[(0, 'Draft'), (1, 'Published'), (2, 'Pending')], default=0),
        ),
    ]