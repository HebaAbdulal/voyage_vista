# Generated by Django 5.0.6 on 2024-08-13 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voyagevista', '0015_alter_reply_options_comment_parent_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created_on']},
        ),
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
        migrations.DeleteModel(
            name='Reply',
        ),
    ]