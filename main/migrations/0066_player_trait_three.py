# Generated by Django 4.1.5 on 2023-06-15 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0065_team_show_on_lists'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='trait_three',
            field=models.CharField(blank=True, choices=[('Movement Shooter', 'Movement Shooter'), ('3PT Shooter', '3PT Shooter'), ('Midrange Menace', 'Midrange Menace'), ('Finesse Finisher', 'Finesse Finisher'), ('Fierce Finisher', 'Fierce Finisher'), ('Ankle Snatcher', 'Ankle Snatcher'), ('Passing Maestro', 'Passing Maestro'), ('Rebound Hound', 'Rebound Hound'), ('Interior Anchor', 'Interior Anchor'), ('Perimeter Lockdown', 'Perimeter Lockdown'), ('Post-Up Powerhouse', 'Post-Up Powerhouse'), ('Dribble Driver', 'Dribble Driver'), ('Post-Up Conductor', 'Post-Up Conductor')], default=None, max_length=36, null=True),
        ),
    ]