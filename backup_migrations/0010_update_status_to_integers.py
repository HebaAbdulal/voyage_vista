from django.db import migrations

def update_status_values(apps, schema_editor):
    Post = apps.get_model('voyagevista', 'Post')
    status_mapping = {
        'draft': 0,
        'published': 1,
        'pending': 2
    }
    for old_status, new_status in status_mapping.items():
        Post.objects.filter(status=old_status).update(status=new_status)

class Migration(migrations.Migration):
    dependencies = [
        ('voyagevista', '0010_update_status_to_integers'),
    ]

    operations = [
        migrations.RunPython(update_status_values),
    ]