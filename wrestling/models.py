# Django imports
from django.db import models

# Main imports
from main.models import DiscordUser

# Wrestling models
class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    logo = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

class Wrestler(models.Model):

    # Wrestler default fields
    worker_name = models.CharField(max_length=100)
    twitch_handle = models.CharField(max_length=100)
    division = models.CharField(max_length=100) # has choices
    gimmick = models.CharField(max_length=100) # has choices
    brand = models.CharField(max_length=100) # has choices
    worker_disposition = models.CharField(max_length=100) # has choices
    size = models.CharField(max_length=100) # has choices
    gender = models.CharField(max_length=100) # has choices
    nationality = models.CharField(max_length=100) # has choices
    overall = models.SmallIntegerField(default=0)
    accolades = models.TextField(blank=True, null=True)

    # Wrestler attribute fields
    total_xp = models.SmallIntegerField()
    attributes = models.JSONField()

    # Wrestler profile fields
    profession = models.CharField(max_length=100) # has choices
    wrestler_class = models.CharField(max_length=100) # has choices
    age = models.CharField(max_length=100) # has choices
    entrance = models.CharField(max_length=100) # has choices
    victory = models.CharField(max_length=100) # has choices
    music = models.CharField(max_length=100) # has choices
    story = models.TextField(blank=True, null=True)

    # Wrestler image fields
    profile_picture = models.CharField(max_length=100)
    payback_one_picture = models.CharField(max_length=100)
    payback_two_picture = models.CharField(max_length=100)

    # wrestler move fields
    move_set = models.CharField(max_length=100) # has choices
    finishing_move_1 = models.CharField(max_length=100) # has choices
    finishing_move_2 = models.CharField(max_length=100) # has choices
    signature_move_1 = models.CharField(max_length=100) # has choices
    signature_move_2 = models.CharField(max_length=100) # has choices

    # wrestler miscanellous fields
    date_created = models.DateTimeField(auto_now_add=True)
    first_show = models.SmallIntegerField(blank=True, null=True)

    # Wrestler relationships
    team = models.ForeignKey('Team', blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(DiscordUser, on_delete=models.CASCADE)

class Show(models.Model):
    
    # Show default fields
    name = models.CharField(max_length=100)
    picture = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

class Title(models.Model):

    # Title default fields
    name = models.CharField(max_length=100)
    picture = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

class Reign(models.Model):

    # Reign default fields
    date_created = models.DateTimeField(auto_now_add=True)

    # Reign relationships
    title = models.ForeignKey('Title', on_delete=models.CASCADE)
    wrestler = models.ForeignKey('Wrestler', on_delete=models.CASCADE)
    show = models.ForeignKey('Show', on_delete=models.CASCADE)