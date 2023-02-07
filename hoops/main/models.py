from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .managers import DiscordAuthorizationManager
from .league import config as league_config

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
    id = models.BigIntegerField(primary_key=True, serialize=False)
    first_name = models.CharField(default="Unknown", max_length=16) # Ex: LeBron
    last_name = models.CharField(default="Player", max_length=16) # Ex: James
    height = models.CharField( # Ex: 76 (in inches)
        max_length=2,
        choices = league_config.height_choices,
        default = league_config.height_choices[0][0],
    ) 
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
    primary_currency = models.PositiveBigIntegerField(
        name=league_config.primary_currency_name, 
        default=league_config.primary_currency_start,
    )
    secondary_currency = models.PositiveBigIntegerField(
        name=league_config.secondary_currency_name, 
        default=league_config.secondary_currency_start,
    )
    # Relationships
    current_team = models.ForeignKey("Team", on_delete=models.CASCADE) # Each player has one team
    discord_user = models.ForeignKey("DiscordUser", on_delete=models.CASCADE) # Each player has one discord user
    feature_list = models.OneToOneField("FeatureList", on_delete=models.CASCADE) # Each player has one features object
    history_list = models.OneToOneField("HistoryList", on_delete=models.CASCADE) # Each player has one history object
    contract_details = models.OneToOneField("Contract", null=True, blank=True, on_delete=models.CASCADE) # Each player has one contract
    # Player Methods
    def __str__(self):
        return f"[{self.id}] {self.first_name} {self.last_name}"

# List Models (for players)
class FeatureList(models.Model):
    id = models.BigIntegerField(primary_key=True, serialize=False)
    features = models.JSONField(default=league_config.get_default_features, blank=True) # Ex: {"fake_feature": True}

class HistoryList(models.Model):
    id = models.BigIntegerField(primary_key=True, serialize=False)  
    history = models.JSONField(default=league_config.get_default_history, blank=True) # Ex: {"fake_history": 0}

class Contract(models.Model):
    id = models.BigIntegerField(primary_key=True, serialize=False)
    breakdown = models.JSONField(default=league_config.get_default_contract, blank=True) 
    # Contract Methods
    def __str__(self):
        return f"Contract Entry #{self.id}"

# Team & Statistic Models
class Team(models.Model):
    id = models.BigIntegerField(primary_key=True, serialize=False)
    name = models.CharField(max_length=32) # Ex: Los Angeles Lakers
    logo = models.CharField(max_length=100, default=league_config.initial_team_logo) # Ex: https://cdn.nba.com/logos/nba/1610612747/primary/L/logo.svg
    abbrev = models.CharField(max_length=3) # Ex: LAL
    # Team Methods
    def __str__(self):
        return f"{self.name}"

# League Models
class Season(models.Model):
    id = models.BigIntegerField(primary_key=True, serialize=False)
    # Season Methods
    def __str__(self):
        return f"Season {self.id}"

class Configuration(models.Model):
    id = models.BigIntegerField(primary_key=True, serialize=False)
    name = models.CharField(max_length=32)
    settings = models.JSONField(default=league_config.get_default_settings, blank=True)
    # Relationships
    current_season = models.OneToOneField("Season", on_delete=models.CASCADE) # Each configuration has one season
    # Settings Methods
    def __str__(self):
        return f"Configuration: {self.current_season}"