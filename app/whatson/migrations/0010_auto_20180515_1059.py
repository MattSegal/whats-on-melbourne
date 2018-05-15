# Generated by Django 2.0.5 on 2018-05-15 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whatson', '0009_auto_20180512_0343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(blank=True, choices=[('TRIVIA', 'Trivia'), ('JAZZ', 'Jazz'), ('ARTS', 'Arts and Theatre'), ('HIPHOP', 'Hip-Hop'), ('EDM', 'Electronic Dance Music'), ('ROCK', 'Rock'), ('FOLK', 'Folk'), ('COMEDY', 'Comedy'), ('POKER', 'Poker')], max_length=15, null=True),
        ),
    ]
