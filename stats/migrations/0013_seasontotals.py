# Generated by Django 4.1.5 on 2023-06-15 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0065_team_show_on_lists'),
        ('stats', '0012_seasonaverage_average_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeasonTotals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gp', models.PositiveSmallIntegerField(default=0)),
                ('pts', models.PositiveSmallIntegerField(default=0)),
                ('reb', models.PositiveSmallIntegerField(default=0)),
                ('ast', models.PositiveSmallIntegerField(default=0)),
                ('stl', models.PositiveSmallIntegerField(default=0)),
                ('blk', models.PositiveSmallIntegerField(default=0)),
                ('tov', models.PositiveSmallIntegerField(default=0)),
                ('fgm', models.PositiveSmallIntegerField(default=0)),
                ('fga', models.PositiveSmallIntegerField(default=0)),
                ('tpm', models.PositiveSmallIntegerField(default=0)),
                ('tpa', models.PositiveSmallIntegerField(default=0)),
                ('ftm', models.PositiveSmallIntegerField(default=0)),
                ('fta', models.PositiveSmallIntegerField(default=0)),
                ('oreb', models.PositiveSmallIntegerField(default=0)),
                ('fouls', models.PositiveSmallIntegerField(default=0)),
                ('gmsc', models.PositiveSmallIntegerField(default=0)),
                ('total_type', models.CharField(choices=[('PRE', 'Preseason'), ('REG', 'Regular Season'), ('PLY', 'Playoffs'), ('FIN', 'Finals')], default='R', max_length=3)),
                ('season', models.PositiveSmallIntegerField(default=2, unique=True)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.player')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.team')),
            ],
        ),
    ]
