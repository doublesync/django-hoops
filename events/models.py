# Django imports
from django.db import models

# Main application imports
from main.models import Player

# Create your models here.
class Event(models.Model):

    # Event fields
    title = models.CharField(max_length=100)
    description = models.TextField()
    rookies_allowed = models.BooleanField(default=False)
    free_agents_allowed = models.BooleanField(default=False)
    active_players_allowed = models.BooleanField(default=False)
    use_spent_limit = models.BooleanField(default=False)
    spent_limit = models.IntegerField(default=0)
    max_entrees = models.IntegerField(default=0)

    # Custom str method
    def __str__(self):
        return self.title

class Entree(models.Model):
    # Entree relationships
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    # Custom str method
    def __str__(self):
        return f"{self.player} - {self.event}"