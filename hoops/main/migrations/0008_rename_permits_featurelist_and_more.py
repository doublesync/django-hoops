# Generated by Django 4.1.5 on 2023-01-23 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_permits_permits_alter_player_attributes_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Permits',
            new_name='FeatureList',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='permits',
            new_name='feature_list',
        ),
    ]
