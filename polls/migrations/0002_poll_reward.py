# Generated by Django 4.1.5 on 2023-07-11 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='reward',
            field=models.IntegerField(default=0),
        ),
    ]
