# Generated by Django 4.1.5 on 2023-01-22 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_discorduser_managers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discorduser',
            name='username',
        ),
        migrations.AlterField(
            model_name='discorduser',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]
