# Generated by Django 4.1.5 on 2023-06-15 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0065_team_show_on_lists'),
        ('stats', '0009_seasonaverages'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SeasonAverages',
            new_name='SeasonAverage',
        ),
    ]
