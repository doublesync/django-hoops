# Generated by Django 4.1.5 on 2023-04-08 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_alter_coupon_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='use_game_tendencies',
            field=models.BooleanField(default=True),
        ),
    ]
