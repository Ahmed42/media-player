# Generated by Django 4.0.2 on 2022-02-23 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musiclib', '0004_album_artist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='artist',
        ),
    ]
