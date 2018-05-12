# Generated by Django 2.0.5 on 2018-05-12 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whatson', '0008_auto_20180509_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(blank=True, choices=[('TRIVIA', 'Trivia'), ('JAZZ', 'Jazz'), ('ARTS', 'Arts and Theatre'), ('HIPHOP', 'Hip-Hop'), ('CLUB', 'Club'), ('ROCK', 'Rock'), ('FOLK', 'Folk')], max_length=15, null=True),
        ),
    ]
