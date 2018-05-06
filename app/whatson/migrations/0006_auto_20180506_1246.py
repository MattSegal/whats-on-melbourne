# Generated by Django 2.0.5 on 2018-05-06 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whatson', '0005_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='website',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='source',
            name='scraped_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
