# Django imports
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Custom imports
from stats.league import config as stats_config
from main.league import config as league_config

# Main application imports
from main.models import Player
from main.models import Team

# Create your models here.
class Statline(models.Model):

    # Manual statline fields
    rebounds = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(stats_config.max_rebounds)])
    assists = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(stats_config.max_assists)])
    steals = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(stats_config.max_steals)])
    blocks = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(stats_config.max_blocks)])
    turnovers = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(stats_config.max_turnovers)])
    field_goals_made = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(stats_config.max_made)])
    field_goals_attempted = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(stats_config.max_attempted)])
    three_pointers_made = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(stats_config.max_made)])
    three_pointers_attempted = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(stats_config.max_attempted)])
    free_throws_made = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(stats_config.max_made)])
    free_throws_attempted = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(stats_config.max_attempted)])
    offensive_rebounds = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(stats_config.max_rebounds)])
    personal_fouls = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(stats_config.max_fouls)])

    # Calculated statline fields
    points = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(stats_config.max_points)])
    defensive_rebounds = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(stats_config.max_rebounds)])

    # Relationships & other data
    season = models.PositiveSmallIntegerField(default=league_config.current_season)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team_at_time = models.ForeignKey(Team, on_delete=models.CASCADE)

    # "team_at_time" will enable us to track players who are traded mid-season

    # Overwritten save method
    def save(self, *args, **kwargs):
        self.points = ((self.field_goals_made - self.three_pointers_made) * 2) + (self.three_pointers_made * 3) + self.free_throws_made
        self.defensive_rebounds = (self.rebounds - self.offensive_rebounds)
        super().save(*args, **kwargs)

    # Overwritten str method
    def __str__(self):
        return f"{self.player} | {self.game}"

class Game(models.Model):

    # Statline fields
    home_points = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(stats_config.max_team_points)])
    away_points = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(stats_config.max_team_points)])

    # Relationships & other data
    season = models.PositiveSmallIntegerField(default=league_config.current_season)
    home = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home')
    away = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away')
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='winner')
    loser = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='loser')

    # Overwritten str method
    def __str__(self):
        return f"S{self.season} | {self.away} @ {self.home}"