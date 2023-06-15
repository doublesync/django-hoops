# Django imports
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Custom imports
from stats.league import config as stats_config
from main.league import config as league_config

# Main application imports
from main.models import Player
from main.models import Team

# Stats application imports
from stats.league.stats import advanced as stats_advanced

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

    # Overwritten save method
    def save(self, *args, **kwargs):
        self.points = ((self.field_goals_made - self.three_pointers_made) * 2) + (self.three_pointers_made * 3) + self.free_throws_made
        self.defensive_rebounds = (self.rebounds - self.offensive_rebounds)
        super().save(*args, **kwargs)

    # Overwritten str method
    def __str__(self):
        return f"{self.player} | {self.game}"

class SeasonAverage(models.Model):

    # Average fields
    gp = models.PositiveSmallIntegerField(default=0)
    ppg = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    rpg = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    apg = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    spg = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    bpg = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    tpg = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    fgm = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    fga = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    tpm = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    tpa = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    ftm = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    fta = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    orpg = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    fpg = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    gmsc = models.DecimalField(max_digits=4, decimal_places=1, default=0)

    # Average type
    game_type = models.CharField(max_length=3, choices=stats_config.game_types,default=stats_config.game_types[1][0])

    # Relationships & other data
    season = models.PositiveSmallIntegerField(default=league_config.current_season)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['season', 'team', 'player', 'game_type']]

    # Overwritten save method
    def save(self, *args, **kwargs):
        # Find statlines
        statlines = self.player.statline_set.filter(season=self.season, team_at_time=self.team, game__game_type=self.game_type)
        # Calculate averages (stop division by zero errors)
        if not len(statlines) == 0:
            self.gp = len(statlines)
            self.ppg = round(sum([line.points for line in statlines]) / len(statlines), 1)
            self.rpg = round(sum([line.rebounds for line in statlines]) / len(statlines), 1)
            self.apg = round(sum([line.assists for line in statlines]) / len(statlines), 1)
            self.spg = round(sum([line.steals for line in statlines]) / len(statlines), 1)
            self.bpg = round(sum([line.blocks for line in statlines]) / len(statlines), 1)
            self.tpg = round(sum([line.turnovers for line in statlines]) / len(statlines), 1)
            self.fgm = round(sum([line.field_goals_made for line in statlines]) / len(statlines), 1)
            self.fga = round(sum([line.field_goals_attempted for line in statlines]) / len(statlines), 1)
            self.tpm = round(sum([line.three_pointers_made for line in statlines]) / len(statlines), 1)
            self.tpa = round(sum([line.three_pointers_attempted for line in statlines]) / len(statlines), 1)
            self.ftm = round(sum([line.free_throws_made for line in statlines]) / len(statlines), 1)
            self.fta = round(sum([line.free_throws_attempted for line in statlines]) / len(statlines), 1)
            self.orpg = round(sum([line.offensive_rebounds for line in statlines]) / len(statlines), 1)
            self.fpg = round(sum([line.personal_fouls for line in statlines]) / len(statlines), 1)
            # Calculate gamescore
            self.gmsc = round(sum([stats_advanced.get_game_score(line) for line in statlines]) / len(statlines), 1)
        # Save the model
        super().save(*args, **kwargs)

    # Overwritten str method
    def __str__(self):
        return f"{self.player} | S{self.season} | {self.team}"

class SeasonTotal(models.Model):

    # Total fields
    gp = models.PositiveSmallIntegerField(default=0)
    pts = models.PositiveSmallIntegerField(default=0)
    reb = models.PositiveSmallIntegerField(default=0)
    ast = models.PositiveSmallIntegerField(default=0)
    stl = models.PositiveSmallIntegerField(default=0)
    blk = models.PositiveSmallIntegerField(default=0)
    tov = models.PositiveSmallIntegerField(default=0)
    fgm = models.PositiveSmallIntegerField(default=0)
    fga = models.PositiveSmallIntegerField(default=0)
    tpm = models.PositiveSmallIntegerField(default=0)
    tpa = models.PositiveSmallIntegerField(default=0)
    ftm = models.PositiveSmallIntegerField(default=0)
    fta = models.PositiveSmallIntegerField(default=0)
    oreb = models.PositiveSmallIntegerField(default=0)
    fouls = models.PositiveSmallIntegerField(default=0)

    # Total type
    game_type = models.CharField(max_length=3, choices=stats_config.game_types, default=stats_config.game_types[1][0])

    # Relationships & other data
    season = models.PositiveSmallIntegerField(default=league_config.current_season)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['season', 'team', 'player', 'game_type']]

    # Overwritten save method
    def save(self, *args, **kwargs):
        # Find statlines
        self.gp = len(self.player.statline_set.filter(season=self.season, team_at_time=self.team, game__game_type=self.game_type))
        self.pts = sum([line.points for line in self.player.statline_set.filter(season=self.season, team_at_time=self.team, game__game_type=self.game_type)])
        self.reb = sum([line.rebounds for line in self.player.statline_set.filter(season=self.season, team_at_time=self.team, game__game_type=self.game_type)])
        self.ast = sum([line.assists for line in self.player.statline_set.filter(season=self.season, team_at_time=self.team, game__game_type=self.game_type)])
        self.stl = sum([line.steals for line in self.player.statline_set.filter(season=self.season, team_at_time=self.team, game__game_type=self.game_type)])
        self.blk = sum([line.blocks for line in self.player.statline_set.filter(season=self.season, team_at_time=self.team, game__game_type=self.game_type)])
        self.tov = sum([line.turnovers for line in self.player.statline_set.filter(season=self.season, team_at_time=self.team, game__game_type=self.game_type)])
        self.fgm = sum([line.field_goals_made for line in self.player.statline_set.filter(season=self.season, team_at_time=self.team, game__game_type=self.game_type)])
        self.fga = sum([line.field_goals_attempted for line in self.player.statline_set.filter(season=self.season, team_at_time=self.team, game__game_type=self.game_type)])
        self.tpm = sum([line.three_pointers_made for line in self.player.statline_set.filter(season=self.season, team_at_time=self.team, game__game_type=self.game_type)])
        self.tpa = sum([line.three_pointers_attempted for line in self.player.statline_set.filter(season=self.season, team_at_time=self.team, game__game_type=self.game_type)])
        self.ftm = sum([line.free_throws_made for line in self.player.statline_set.filter(season=self.season, team_at_time=self.team, game__game_type=self.game_type)])
        self.fta = sum([line.free_throws_attempted for line in self.player.statline_set.filter(season=self.season, team_at_time=self.team, game__game_type=self.game_type)])
        self.oreb = sum([line.offensive_rebounds for line in self.player.statline_set.filter(season=self.season, team_at_time=self.team, game__game_type=self.game_type)])
        self.fouls = sum([line.personal_fouls for line in self.player.statline_set.filter(season=self.season, team_at_time=self.team, game__game_type=self.game_type)])
        # Save the model
        super().save(*args, **kwargs)

    # Overwritten str method
    def __str__(self):
        return f"{self.player} | S{self.season} | {self.team}"

class Game(models.Model):

    # Statline fields
    # Add date field with auto_now_add=True and a default value
    date = models.DateField(auto_now_add=True)
    home_points = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(stats_config.max_team_points)])
    away_points = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(stats_config.max_team_points)])
    game_type = models.CharField(max_length=3, choices=stats_config.game_types, default='R')

    # Relationships & other data
    season = models.PositiveSmallIntegerField(default=league_config.current_season)
    day = models.PositiveSmallIntegerField(default=1)
    home = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home')
    away = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away')
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='winner')
    loser = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='loser')

    # Overwritten str method
    def __str__(self):
        return f"S{self.season}D{self.day} | {self.away} @ {self.home}"