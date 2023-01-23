from django.db import models
from .managers import DiscordAuthorizationManager
from .league import config as league_config

# Create your models here.
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

class Player(models.Model):
    # Player Model
    id = models.BigIntegerField(primary_key=True, serialize=False)
    name = models.CharField(max_length=32) # Ex: LeBron James
    height = models.CharField(max_length=6) # Ex: 188.26 (in cm)
    weight = models.CharField(max_length=3) # Ex: 226 (in lbs)
    primary_position = models.CharField(max_length=1) # (0 = PG, 1 = SG, 2 = SF, 3 = PF, 4 = C)
    secondary_position = models.CharField(max_length=1) # (0 = PG, 1 = SG, 2 = SF, 3 = PF, 4 = C)
    attributes = models.JSONField(default=league_config.get_default_attributes)
    badges = models.JSONField(default=league_config.get_default_badges)
    discord_user = models.ForeignKey("DiscordUser", on_delete=models.CASCADE) # Each player has one discord user
    feature_list = models.OneToOneField("FeatureList", on_delete=models.CASCADE) # Each player has one permits object
    # Player Methods
    def __str__(self):
        return f"{self.id} : {self.name} : {self.height} / {self.weight} : {self.discord_user}"

class FeatureList(models.Model):
    id = models.BigIntegerField(primary_key=True, serialize=False)
    permits = models.JSONField(default=league_config.get_default_permits)