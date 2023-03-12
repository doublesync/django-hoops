# Generated by Django 4.1.5 on 2023-03-12 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_player_primary_archetype_player_secondary_archetype_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='salary',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='primary_archetype',
            field=models.CharField(choices=[('Shooter', 'Shooter'), ('Slasher', 'Slasher'), ('Playmaker', 'Playmaker'), ('Post Scorer', 'Post Scorer'), ('Rebounder', 'Rebounder'), ('Perimeter Defender', 'Perimeter Defender'), ('Interior Defender', 'Interior Defender')], default='Shooter', max_length=36),
        ),
        migrations.AlterField(
            model_name='player',
            name='secondary_archetype',
            field=models.CharField(choices=[('Shooter', 'Shooter'), ('Slasher', 'Slasher'), ('Playmaker', 'Playmaker'), ('Post Scorer', 'Post Scorer'), ('Rebounder', 'Rebounder'), ('Perimeter Defender', 'Perimeter Defender'), ('Interior Defender', 'Interior Defender')], default='Shooter', max_length=36),
        ),
    ]
