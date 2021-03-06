# Generated by Django 4.0.2 on 2022-02-21 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musiclib', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='album',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='musiclib.album'),
        ),
        migrations.AlterField(
            model_name='song',
            name='artist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='musiclib.artist'),
        ),
    ]
