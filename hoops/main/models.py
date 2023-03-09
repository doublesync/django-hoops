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
    first_name = models.CharField(default="Unknown", max_length=16)
    last_name = models.CharField(default="Player", max_length=16)
    height = models.SmallIntegerField(
        choices=league_config.height_choices, default=league_config.height_choices[0][0]
    )
    weight = models.IntegerField(
        validators=[
            MinValueValidator(league_config.player_weight_min),
            MaxValueValidator(league_config.player_weight_max),
        ]
    )
    primary_position = models.CharField(
        max_length=2,
        choices=league_config.position_choices,
        default=league_config.position_choices[0][0],
    )
    secondary_position = models.CharField(
        max_length=2,
        choices=league_config.position_choices,
        default=league_config.position_choices[0][0],
    )
    jersey_number = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(99)]
    )
    attributes = models.JSONField(default=league_config.get_default_attributes)
    badges = models.JSONField(default=league_config.get_default_badges)
    hotzones = models.JSONField(default=league_config.get_default_hotzones)
    # Player Currencies
    primary_currency = models.PositiveBigIntegerField(
        name="cash", default=league_config.primary_currency_start
    )
    spent = models.PositiveBigIntegerField(name="spent", default=0)
    # Relationships
    discord_user = models.ForeignKey("DiscordUser", on_delete=models.CASCADE)
    current_team = models.ForeignKey(
        "Team", blank=True, null=True, on_delete=models.CASCADE
    )
    height_limits = models.ForeignKey(
        "HeightLimit", blank=True, null=True, on_delete=models.CASCADE
    )
    weight_limits = models.ForeignKey(
        "WeightLimit", blank=True, null=True, on_delete=models.CASCADE
    )
    history_list = models.ForeignKey("HistoryList", on_delete=models.CASCADE)
    # Miscanellous
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
    offer_player = models.ForeignKey(
        "Player", on_delete=models.CASCADE
    )  # Each offer has one player
    offer_team = models.ForeignKey(
        "Team", blank=True, null=True, on_delete=models.CASCADE
    )  # Each offer has one team
    offer_length = models.SmallIntegerField(
        default=0, validators=[MinValueValidator(1), MaxValueValidator(3)]
    )
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
    # Does player or team accept/decline offer
    player_choice = models.BooleanField(default=False)
    # PlayerOffer Methods
    def __str__(self):
        return f"{self.offer_player} | {self.offer_team} for {self.offer_length} years"


# List Models (for players)
class HistoryList(models.Model):
    history = models.JSONField(default=league_config.get_default_history, blank=True)


# Team & Statistic Models
class Team(models.Model):
    name = models.CharField(max_length=32)
    logo = models.CharField(max_length=100, default=league_config.initial_team_logo)
    abbrev = models.CharField(max_length=3)
    # Relationships
    manager = models.ForeignKey("DiscordUser", on_delete=models.CASCADE)
    history_list = models.ForeignKey("HistoryList", on_delete=models.CASCADE)
    # Team Methods
    def __str__(self):
        return f"{self.name}"
