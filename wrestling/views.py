# Django imports
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Main imports
from main.models import DiscordUser

# Python imports
import os

# Custom imports
from .models import Wrestler
from .models import Team
from .models import Show

# Create your views here.
@login_required(login_url="/login/discord/")
def index(request):
    # Find the user's wrestlers
    wrestlers = Wrestler.objects.filter(manager=request.user)
    context = {
        "wrestlers": wrestlers,
        "motd": os.environ.get("MOTD"),
    }
    return render(request, 'wrestling/league/home.html', context=context)

# Wrestler views
@login_required(login_url="/login/discord/")
def wrestler_create(request):
    context = {
        
    }
    return render(request, 'wrestling/wrestler/create.html', context=context)

def wrestler_profile(request, wrestler_id):
    return render(request, 'wrestling/wrestler_profile.html')

@login_required(login_url="/login/discord/")
def wrestler_upgrade(request, wrestler_id):
    return render(request, 'wrestling/wrestler_upgrade.html')

# Roster views
def wrestling_roster(request):
    return render(request, 'wrestling/wrestling_roster.html')

# Titles views
def wrestling_titles(request):
    return render(request, 'wrestling/wrestling_titles.html')

def wrestling_title_history(request, title_id):
    return render(request, 'wrestling/wrestling_title_history.html')

# Shows views
def wrestling_shows(request):
    return render(request, 'wrestling/wrestling_shows.html')

# HTMX views
