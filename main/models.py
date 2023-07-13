# Django imports
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Custom imports
from .managers import DiscordAuthorizationManager
from .league import config as league_config


# DiscordUser Models
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
    last_reward = models.DateTimeField(null=True)
    # Permissions
    can_update_players = models.BooleanField(default=False)
    can_approve_trades = models.BooleanField(default=False)
    can_update_styles = models.BooleanField(default=False)
    can_edit_events = models.BooleanField(default=False)
    can_edit_scores = models.BooleanField(default=False)
    # Player Slots
    player_slots = models.SmallIntegerField(default=league_config.max_players)
    auto_collect_rewards = models.BooleanField(default=False)
    can_change_styles = models.BooleanField(default=False)

    # Discord User Methods
    def is_authenticated(self, request):
        return True

    def __str__(self):
        return f"{self.discord_tag}"


# Player Models
class Player(models.Model):
    # Player Model
    first_name = models.CharField(default="Unknown", max_length=16)
    last_name = models.CharField(default="Player", max_length=16)
    cyberface = models.SmallIntegerField(default=0)
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
    headshot = models.CharField(
        max_length=100,
        default=league_config.initial_headshot,
        blank=True,
    )
    # Archetypes & Traits
    primary_archetype = models.CharField(
        max_length=36,
        choices=league_config.archetype_choices,
        default=league_config.archetype_choices[0][0],
    )
    secondary_archetype = models.CharField(
        max_length=36,
        choices=league_config.archetype_choices,
        default=league_config.archetype_choices[0][0],
    )
    trait_one = models.CharField(
        max_length=36,
        choices=league_config.trait_choices,
        default=league_config.trait_choices[0][0],
    )
    trait_two = models.CharField(
        max_length=36,
        choices=league_config.trait_choices,
        default=league_config.trait_choices[0][0],
    )
    trait_three = models.CharField(
        max_length=36,
        choices=league_config.trait_choices,
        default=None,
        null=True,
        blank=True,
    )
    # Player Currencies
    primary_currency = models.BigIntegerField(
        name="cash", default=league_config.primary_currency_start
    )
    salary = models.PositiveBigIntegerField(name="salary", default=0)
    cap_hit = models.PositiveBigIntegerField(name="cap_hit", default=0)
    spent = models.PositiveBigIntegerField(name="spent", default=0)
    # Player Contract Details
    contract_ends_after = models.SmallIntegerField(default=1)
    contract_option = models.CharField(
        max_length=54,
        choices=league_config.contract_option_choices,
        default=league_config.contract_option_choices[0][0],
    )
    contract_benefits = models.CharField(
        max_length=54,
        choices=league_config.contract_benefit_choices,
        default=league_config.contract_benefit_choices[0][0],
    )
    contract_notes = models.CharField(max_length=100, blank=True, null=True)
    # Relationships
    discord_user = models.ForeignKey(
        "DiscordUser", blank=True, null=True, on_delete=models.CASCADE
    )
    current_team = models.ForeignKey(
        "Team", blank=True, null=True, on_delete=models.CASCADE
    )
    history_list = models.ForeignKey("HistoryList", on_delete=models.CASCADE)
    years_played = models.SmallIntegerField(default=1)
    upgrades_pending = models.BooleanField(default=False)
    free_agent = models.BooleanField(default=True)
    use_game_tendencies = models.BooleanField(default=True)
    is_rookie = models.BooleanField(default=False)
    # Attributes, Badges, & Hotzones
    styles = models.JSONField(default=league_config.get_default_styles, blank=True)
    statics = models.JSONField(default=league_config.get_default_statics)
    attributes = models.JSONField(default=league_config.get_default_attributes)
    badges = models.JSONField(default=league_config.get_default_badges)
    hotzones = models.JSONField(default=league_config.get_default_hotzones)
    tendencies = models.JSONField(default=league_config.get_default_tendencies)
    # Player Methods
    def __str__(self):
        return f"[{self.id}] {self.first_name} {self.last_name}"


# List Models (for players)
class HistoryList(models.Model):
    history = models.JSONField(default=league_config.get_default_history, blank=True)


# Team & Statistic Models
class Team(models.Model):
    # Team Model
    name = models.CharField(max_length=32)
    logo = models.CharField(max_length=100, default=league_config.initial_team_logo)
    abbrev = models.CharField(max_length=3)
    picks = models.JSONField(
        default=league_config.get_default_picks, blank=True, null=True
    )
    plays_in_main_league = models.BooleanField(default=True)
    show_on_lists = models.BooleanField(default=True)
    # Relationships
    manager = models.ForeignKey(
        "DiscordUser", blank=True, null=True, on_delete=models.CASCADE
    )
    history_list = models.ForeignKey("HistoryList", on_delete=models.CASCADE)

    # Team Methods
    def __str__(self):
        return f"{self.name}"


# Currency Transaction Models
class Transaction(models.Model):
    # Transaction Model
    transaction_type = models.CharField(
        max_length=16,
        choices=league_config.transaction_type_choices,
        default=league_config.transaction_type_choices[0][0],
    )
    amount = models.PositiveBigIntegerField()
    reason = models.CharField(max_length=100, blank=True)
    # Relationships
    giver = models.ForeignKey("DiscordUser", on_delete=models.CASCADE)
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=False)

    # Transaction Methods
    def __str__(self):
        return f"{self.transaction_type}: {self.amount}"


# Trade Models
class TradeOffer(models.Model):
    # Trade Offer Model
    offer = models.JSONField(default=league_config.get_default_trade_offer)
    accepted = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    finalized = models.BooleanField(default=False)
    notes = models.CharField(max_length=100, blank=True)
    # Relationships
    sender = models.ForeignKey("Team", on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="receiver"
    )

    # Trade Offer Methods
    def __str__(self):
        return f"{self.sender} -> {self.receiver}"


# Offer Models
class ContractOffer(models.Model):
    # Contract Offer Model
    years = models.PositiveSmallIntegerField()
    salary = models.PositiveBigIntegerField()
    option = models.CharField(
        max_length=54,
        choices=league_config.contract_option_choices,
        default=league_config.contract_option_choices[0][0],
    )
    benefits = models.CharField(
        max_length=54,
        choices=league_config.contract_benefit_choices,
        default=league_config.contract_benefit_choices[0][0],
    )
    notes = models.CharField(max_length=100, blank=True, null=True, default="No notes.")
    # Relationships
    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    # Boolean Fields
    accepted = models.BooleanField(default=False)

    # Contract Offer Methods
    def __str__(self):
        return f"{self.team.abbrev} -> {self.player.first_name} {self.player.last_name}"


# Coupon Models
class Coupon(models.Model):
    code = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=16, default="Default Coupon")
    amount = models.PositiveBigIntegerField()
    one_use = models.BooleanField(default=False)
    used = models.BooleanField(default=False)

    # Coupon Methods
    def __str__(self):
        return f"{self.code}"


# Notification Models
class Notification(models.Model):
    # Notifcation Model
    title = models.CharField(max_length=32, default="Notification")
    message = models.CharField(max_length=100, default="Content")
    read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=False)
    # Relationships
    discord_user = models.ForeignKey("DiscordUser", on_delete=models.CASCADE)


# Award Models
class Award(models.Model):
    # Award Model
    name = models.CharField(
        max_length=6,
        choices=league_config.award_name_choices,
        default=league_config.award_name_choices[0][0],
    )
    description = models.CharField(max_length=16, default="Description")
    # Relationships
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    season = models.PositiveSmallIntegerField(default=1)

    # Award Methods
    def __str__(self):
        return f"S{self.season} - {self.name} - {self.player}"
