# Generated by Django 4.0.2 on 2022-03-08 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musiclib', '0009_song_time_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='release_date',
        ),
    ]
