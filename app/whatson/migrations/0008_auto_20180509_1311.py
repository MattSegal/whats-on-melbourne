# Generated by Django 2.0.5 on 2018-05-09 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whatson', '0007_event_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='type',
            new_name='event_type',
        ),
    ]
