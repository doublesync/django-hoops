from django.db import models
from .managers import DiscordAuthorizationManager

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
    def is_activate(self, request):
        return True