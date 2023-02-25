# Django imports
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Custom imports
from .managers import DiscordAuthorizationManager
from .league import config as league_config
from .league.extra import convert as league_converters

# Player & User Models
class DiscordUser(models.Model):
    # Custom Manager
    objects = DiscordAuthorizationManager()
    # Discord User Model
    id = models.BigIntegerField(primary_key=True, serialize=False)
    discord_tag = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100)
    public_flags = models.IntegerField()
    flags = models.IntegerField()
    locale = models.CharField(max_length=100)
    mfa_enabled = models.BooleanField()
    last_login = models.DateTimeField(null=True)
    # Discord User Methods
    def is_authenticated(self, request):
        return True
    def __str__(self):
        return f"{self.discord_tag}"

class Player(models.Model):
    # Player Model
    first_name = models.CharField(default="Unknown", max_length=16) # Ex: LeBron
    last_name = models.CharField(default="Player", max_length=16) # Ex: James
    height = models.SmallIntegerField(choices=league_config.height_choices, default=league_config.height_choices[0][0]) 
    weight = models.IntegerField( # Ex: 226 (in lbs)
        validators=[
            MinValueValidator(league_config.player_weight_min), 
            MaxValueValidator(league_config.player_weight_max),
        ]
    ) 
    primary_position = models.CharField( # (0 = PG, 1 = SG, 2 = SF, 3 = PF, 4 = C)
        max_length=2,
        choices=league_config.position_choices,
        default=league_config.position_choices[0][0],
    ) 
    secondary_position = models.CharField( # (0 = PG, 1 = SG, 2 = SF, 3 = PF, 4 = C)
        max_length=2,
        choices=league_config.position_choices,
        default=league_config.position_choices[0][0],
    ) 
    jersey_number = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(99)]) # Ex: 23
    attributes = models.JSONField(default=league_config.get_default_attributes)
    badges = models.JSONField(default=league_config.get_default_badges)
    # Player Currencies
    primary_currency = models.PositiveBigIntegerField(name="cash", default=league_config.primary_currency_start)
    spent = models.PositiveBigIntegerField(name="spent", default=0)
    # Relationships
    discord_user = models.ForeignKey("DiscordUser", on_delete=models.CASCADE) # Each player has one discord user
    current_team = models.ForeignKey("Team", blank=True, null=True, on_delete=models.CASCADE) # Each player has one team
    height_limits = models.ForeignKey("HeightLimit", blank=True, null=True, on_delete=models.CASCADE) # Each player has one heightLimit object
    weight_limits = models.ForeignKey("WeightLimit", blank=True, null=True, on_delete=models.CASCADE) # Each player has one weightLimit object
    contract_details = models.ForeignKey("Contract", blank=True, null=True, on_delete=models.CASCADE) # Each player has one contract
    history_list = models.ForeignKey("HistoryList", on_delete=models.CASCADE) # Each player has one history object
    # Others
    upgrades_pending = models.BooleanField(default=False)
    free_agent = models.BooleanField(default=True)
    years_played = models.SmallIntegerField(default=1)
    # Player Methods
    def __str__(self):
        return f"[{self.id}] {self.first_name} {self.last_name}"

class HeightLimit(models.Model):
    # HeightLimit Model
    height = models.SmallIntegerField(default=0)
    limits = models.JSONField(default=league_config.get_default_limits)
    enabled = models.BooleanField(default=True)
    # HeightLimit Methods
    def __str__(self):
        return f"Limits for {league_converters.convert_to_height(self.height)}"

class WeightLimit(models.Model):
    # WeightLimit Model
    range1 = models.SmallIntegerField(default=0)
    range2 = models.SmallIntegerField(default=0)
    limits = models.JSONField(default=league_config.get_default_limits)
    enabled = models.BooleanField(default=True)
    # WeightLimit Methods
    def __str__(self):
        return f"{self.range1}lbs - {self.range2-1}lbs"

class Offer(models.Model):
    # PlayerOffer Model
    offer_player = models.ForeignKey("Player", on_delete=models.CASCADE) # Each offer has one player
    offer_team = models.ForeignKey("Team", blank=True, null=True, on_delete=models.CASCADE) # Each offer has one team
    offer_length = models.SmallIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(3)])
    # Salaries
    year_one_salary = models.SmallIntegerField(default=0)
    year_two_salary = models.SmallIntegerField(default=0)
    year_three_salary = models.SmallIntegerField(default=0)
    # Options
    player_option = models.BooleanField(default=False)
    team_option = models.BooleanField(default=False)
    # Clauses
    no_trade_clause = models.BooleanField(default=False)
    no_cut_clause = models.BooleanField(default=False)
    # Does player ot team accept/decline offer
    player_choice = models.BooleanField(default=False)
    # PlayerOffer Methods
    def __str__(self):
        return f"{self.offer_player} | {self.offer_team} for {self.offer_length} years"

# List Models (for players)
class HistoryList(models.Model):
    history = models.JSONField(default=league_config.get_default_history, blank=True)

class Contract(models.Model):
    # Contract
    contract_team = models.ForeignKey("Team", on_delete=models.CASCADE) # Each contract has one team
    contract_year = models.SmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(3)])
    contract_length = models.SmallIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(3)])
    # Salaries
    year_one_salary = models.SmallIntegerField(default=0)
    year_two_salary = models.SmallIntegerField(default=0)
    year_three_salary = models.SmallIntegerField(default=0)
    # Options
    player_option = models.BooleanField(default=False)
    team_option = models.BooleanField(default=False)
    # Clauses
    no_trade_clause = models.BooleanField(default=False)
    no_cut_clause = models.BooleanField(default=False)

# Team & Statistic Models
class Team(models.Model):
    name = models.CharField(max_length=32) # Ex: Los Angeles Lakers
    logo = models.CharField(max_length=100, default=league_config.initial_team_logo) # Ex: https://cdn.nba.com/logos/nba/1610612747/primary/L/logo.svg
    abbrev = models.CharField(max_length=3) # Ex: LAL
    # Relationships
    manager = models.ForeignKey("DiscordUser", on_delete=models.CASCADE) # Each team has one manager
    history_list = models.ForeignKey("HistoryList", on_delete=models.CASCADE) # Each team has one history object
    # Team Methods
    def __str__(self):
        return f"{self.name}"

# League Models
class Season(models.Model):
    # Season Methods
    def __str__(self):
        return f"Season {self.id}"

class Configuration(models.Model):
    name = models.CharField(max_length=32)
    settings = models.JSONField(default=league_config.get_default_settings, blank=True)
    # Relationships
    current_season = models.OneToOneField("Season", on_delete=models.CASCADE) # Each configuration has one season
    # Settings Methods
    def __str__(self):
        return f"Configuration: {self.current_season}"