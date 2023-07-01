# Django imports
from django.db import models

# Main imports
from main.models import DiscordUser

# Create your models here.
class Poll(models.Model):

    # Poll model
    question = models.CharField(max_length=200)
    date = models.DateTimeField()

    # Custom string method
    def __str__(self) -> str:
        return self.question
    
class Choice(models.Model):

    # Choice model
    agreed = models.BooleanField(default=False)
    votes = models.IntegerField(default=0)

    # Choice relationships
    related_poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    discord_user = models.ForeignKey(DiscordUser, on_delete=models.CASCADE)

    # Custom string method
    def __str__(self) -> str:
        return self.choice_text