from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('voyagevista', '0009_alter_post_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.IntegerField(choices=[(0, 'Draft'), (1, 'Published'), (2, 'Pending')], default=0),
        ),
    ]