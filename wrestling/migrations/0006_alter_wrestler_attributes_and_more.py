# Generated by Django 4.1.5 on 2023-09-13 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wrestling', '0005_rename_render_wrestler_profile_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wrestler',
            name='attributes',
            field=models.JSONField(default={'Cruiserweight': {'High Flyer': {'Aerial Offense': 70, 'Aerial Range': 75, 'Aerial Reversal': 65, 'Agility': 75, 'Arm Durability': 55, 'Arm Power': 45, 'Body Durability': 55, 'Finisher': 60, 'Grapple Offense': 50, 'Grapple Reversal': 55, 'Leg Durability': 55, 'Leg Power': 45, 'Movement Speed': 75, 'Pin Escape': 55, 'Power Submission Defense': 60, 'Power Submission Offense': 30, 'Recovery': 55, 'Running Offense': 55, 'Special': 60, 'Stamina': 60, 'Strength': 55, 'Strike Reversal': 60, 'Technical Submission Defense': 60, 'Technical Submission Offense': 40}, 'Powerhouse': {'Aerial Offense': 30, 'Aerial Range': 45, 'Aerial Reversal': 35, 'Agility': 50, 'Arm Durability': 60, 'Arm Power': 65, 'Body Durability': 60, 'Finisher': 60, 'Grapple Offense': 65, 'Grapple Reversal': 35, 'Leg Durability': 60, 'Leg Power': 65, 'Movement Speed': 55, 'Pin Escape': 55, 'Power Submission Defense': 50, 'Power Submission Offense': 55, 'Recovery': 55, 'Running Offense': 60, 'Special': 60, 'Stamina': 60, 'Strength': 70, 'Strike Reversal': 40, 'Technical Submission Defense': 30, 'Technical Submission Offense': 30}, 'Striker': {'Aerial Offense': 40, 'Aerial Range': 50, 'Aerial Reversal': 50, 'Agility': 60, 'Arm Durability': 65, 'Arm Power': 60, 'Body Durability': 60, 'Finisher': 60, 'Grapple Offense': 55, 'Grapple Reversal': 60, 'Leg Durability': 65, 'Leg Power': 60, 'Movement Speed': 65, 'Pin Escape': 55, 'Power Submission Defense': 50, 'Power Submission Offense': 35, 'Recovery': 55, 'Running Offense': 50, 'Special': 60, 'Stamina': 60, 'Strength': 60, 'Strike Reversal': 60, 'Technical Submission Defense': 50, 'Technical Submission Offense': 40}, 'Technician': {'Aerial Offense': 50, 'Aerial Range': 50, 'Aerial Reversal': 50, 'Agility': 60, 'Arm Durability': 60, 'Arm Power': 50, 'Body Durability': 55, 'Finisher': 60, 'Grapple Offense': 65, 'Grapple Reversal': 55, 'Leg Durability': 60, 'Leg Power': 50, 'Movement Speed': 70, 'Pin Escape': 55, 'Power Submission Defense': 30, 'Power Submission Offense': 30, 'Recovery': 55, 'Running Offense': 50, 'Special': 60, 'Stamina': 60, 'Strength': 40, 'Strike Reversal': 50, 'Technical Submission Defense': 70, 'Technical Submission Offense': 70}}, 'Heavyweight': {'High Flyer': {'Aerial Offense': 70, 'Aerial Range': 55, 'Aerial Reversal': 60, 'Agility': 55, 'Arm Durability': 55, 'Arm Power': 45, 'Body Durability': 55, 'Finisher': 60, 'Grapple Offense': 50, 'Grapple Reversal': 55, 'Leg Durability': 55, 'Leg Power': 45, 'Movement Speed': 60, 'Pin Escape': 55, 'Power Submission Defense': 60, 'Power Submission Offense': 30, 'Recovery': 55, 'Running Offense': 55, 'Special': 60, 'Stamina': 55, 'Strength': 55, 'Strike Reversal': 60, 'Technical Submission Defense': 60, 'Technical Submission Offense': 40}, 'Powerhouse': {'Aerial Offense': 30, 'Aerial Range': 45, 'Aerial Reversal': 35, 'Agility': 50, 'Arm Durability': 60, 'Arm Power': 65, 'Body Durability': 60, 'Finisher': 60, 'Grapple Offense': 65, 'Grapple Reversal': 35, 'Leg Durability': 60, 'Leg Power': 65, 'Movement Speed': 55, 'Pin Escape': 55, 'Power Submission Defense': 50, 'Power Submission Offense': 55, 'Recovery': 55, 'Running Offense': 60, 'Special': 60, 'Stamina': 60, 'Strength': 70, 'Strike Reversal': 40, 'Technical Submission Defense': 30, 'Technical Submission Offense': 30}, 'Striker': {'Aerial Offense': 40, 'Aerial Range': 50, 'Aerial Reversal': 50, 'Agility': 60, 'Arm Durability': 65, 'Arm Power': 60, 'Body Durability': 60, 'Finisher': 60, 'Grapple Offense': 55, 'Grapple Reversal': 60, 'Leg Durability': 65, 'Leg Power': 60, 'Movement Speed': 65, 'Pin Escape': 55, 'Power Submission Defense': 50, 'Power Submission Offense': 35, 'Recovery': 55, 'Running Offense': 50, 'Special': 60, 'Stamina': 60, 'Strength': 60, 'Strike Reversal': 60, 'Technical Submission Defense': 50, 'Technical Submission Offense': 40}, 'Technician': {'Aerial Offense': 50, 'Aerial Range': 50, 'Aerial Reversal': 65, 'Agility': 60, 'Arm Durability': 60, 'Arm Power': 50, 'Body Durability': 55, 'Finisher': 60, 'Grapple Offense': 65, 'Grapple Reversal': 55, 'Leg Durability': 60, 'Leg Power': 50, 'Movement Speed': 70, 'Pin Escape': 65, 'Power Submission Defense': 30, 'Power Submission Offense': 30, 'Recovery': 55, 'Running Offense': 50, 'Special': 60, 'Stamina': 60, 'Strength': 40, 'Strike Reversal': 52, 'Technical Submission Defense': 70, 'Technical Submission Offense': 70}}, 'Light Heavyweight': {'High Flyer': {'Aerial Offense': 70, 'Aerial Range': 75, 'Aerial Reversal': 65, 'Agility': 75, 'Arm Durability': 55, 'Arm Power': 45, 'Body Durability': 55, 'Finisher': 60, 'Grapple Offense': 50, 'Grapple Reversal': 55, 'Leg Durability': 55, 'Leg Power': 45, 'Movement Speed': 75, 'Pin Escape': 55, 'Power Submission Defense': 60, 'Power Submission Offense': 30, 'Recovery': 55, 'Running Offense': 55, 'Special': 60, 'Stamina': 60, 'Strength': 55, 'Strike Reversal': 60, 'Technical Submission Defense': 60, 'Technical Submission Offense': 40}, 'Powerhouse': {'Aerial Offense': 30, 'Aerial Range': 45, 'Aerial Reversal': 35, 'Agility': 50, 'Arm Durability': 60, 'Arm Power': 65, 'Body Durability': 60, 'Finisher': 60, 'Grapple Offense': 65, 'Grapple Reversal': 35, 'Leg Durability': 60, 'Leg Power': 65, 'Movement Speed': 55, 'Pin Escape': 55, 'Power Submission Defense': 50, 'Power Submission Offense': 55, 'Recovery': 55, 'Running Offense': 60, 'Special': 60, 'Stamina': 60, 'Strength': 70, 'Strike Reversal': 40, 'Technical Submission Defense': 30, 'Technical Submission Offense': 30}, 'Striker': {'Aerial Offense': 40, 'Aerial Range': 70, 'Aerial Reversal': 50, 'Agility': 65, 'Arm Durability': 65, 'Arm Power': 60, 'Body Durability': 60, 'Finisher': 60, 'Grapple Offense': 55, 'Grapple Reversal': 60, 'Leg Durability': 65, 'Leg Power': 60, 'Movement Speed': 65, 'Pin Escape': 55, 'Power Submission Defense': 50, 'Power Submission Offense': 35, 'Recovery': 55, 'Running Offense': 50, 'Special': 60, 'Stamina': 60, 'Strength': 60, 'Strike Reversal': 60, 'Technical Submission Defense': 50, 'Technical Submission Offense': 40}, 'Technician': {'Aerial Offense': 50, 'Aerial Range': 50, 'Aerial Reversal': 65, 'Agility': 60, 'Arm Durability': 60, 'Arm Power': 50, 'Body Durability': 55, 'Finisher': 60, 'Grapple Offense': 65, 'Grapple Reversal': 55, 'Leg Durability': 60, 'Leg Power': 50, 'Movement Speed': 70, 'Pin Escape': 65, 'Power Submission Defense': 30, 'Power Submission Offense': 30, 'Recovery': 55, 'Running Offense': 50, 'Special': 60, 'Stamina': 60, 'Strength': 40, 'Strike Reversal': 50, 'Technical Submission Defense': 70, 'Technical Submission Offense': 70}}, 'Super Heavyweight': {'High Flyer': {'Aerial Offense': 70, 'Aerial Range': 55, 'Aerial Reversal': 60, 'Agility': 55, 'Arm Durability': 55, 'Arm Power': 45, 'Body Durability': 55, 'Finisher': 60, 'Grapple Offense': 50, 'Grapple Reversal': 55, 'Leg Durability': 55, 'Leg Power': 45, 'Movement Speed': 60, 'Pin Escape': 55, 'Power Submission Defense': 60, 'Power Submission Offense': 30, 'Recovery': 55, 'Running Offense': 55, 'Special': 60, 'Stamina': 55, 'Strength': 55, 'Strike Reversal': 60, 'Technical Submission Defense': 60, 'Technical Submission Offense': 40}, 'Powerhouse': {'Aerial Offense': 30, 'Aerial Range': 45, 'Aerial Reversal': 35, 'Agility': 50, 'Arm Durability': 60, 'Arm Power': 65, 'Body Durability': 60, 'Finisher': 60, 'Grapple Offense': 65, 'Grapple Reversal': 35, 'Leg Durability': 60, 'Leg Power': 65, 'Movement Speed': 55, 'Pin Escape': 55, 'Power Submission Defense': 50, 'Power Submission Offense': 55, 'Recovery': 55, 'Running Offense': 60, 'Special': 60, 'Stamina': 60, 'Strength': 70, 'Strike Reversal': 40, 'Technical Submission Defense': 30, 'Technical Submission Offense': 30}, 'Striker': {'Aerial Offense': 40, 'Aerial Range': 50, 'Aerial Reversal': 50, 'Agility': 60, 'Arm Durability': 65, 'Arm Power': 60, 'Body Durability': 60, 'Finisher': 60, 'Grapple Offense': 55, 'Grapple Reversal': 60, 'Leg Durability': 65, 'Leg Power': 60, 'Movement Speed': 65, 'Pin Escape': 55, 'Power Submission Defense': 50, 'Power Submission Offense': 35, 'Recovery': 55, 'Running Offense': 50, 'Special': 60, 'Stamina': 60, 'Strength': 60, 'Strike Reversal': 60, 'Technical Submission Defense': 50, 'Technical Submission Offense': 40}, 'Technician': {'Aerial Offense': 50, 'Aerial Range': 50, 'Aerial Reversal': 60, 'Agility': 55, 'Arm Durability': 60, 'Arm Power': 60, 'Body Durability': 55, 'Finisher': 60, 'Grapple Offense': 65, 'Grapple Reversal': 55, 'Leg Durability': 60, 'Leg Power': 50, 'Movement Speed': 60, 'Pin Escape': 65, 'Power Submission Defense': 30, 'Power Submission Offense': 30, 'Recovery': 55, 'Running Offense': 50, 'Special': 60, 'Stamina': 55, 'Strength': 50, 'Strike Reversal': 50, 'Technical Submission Defense': 70, 'Technical Submission Offense': 70}}}),
        ),
        migrations.AlterField(
            model_name='wrestler',
            name='payback_one_picture',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='wrestler',
            name='payback_two_picture',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='wrestler',
            name='profile_picture',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='wrestler',
            name='total_xp',
            field=models.SmallIntegerField(default=0),
        ),
    ]
