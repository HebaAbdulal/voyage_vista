from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('voyagevista', '0008_alter_post_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('pending', 'Pending')], default='draft', max_length=10),
        ),
    ]