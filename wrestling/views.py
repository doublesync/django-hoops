# Django imports
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.management import call_command
from django.db.models import Q
from django.db.models import Sum
from django.template.loader import render_to_string
from django.utils import timezone
from django.views import View
from rest_framework.decorators import api_view

# Main imports
from main.models import DiscordUser

# Python imports
import os

# Model imports
from .models import Wrestler
from .models import Team
from .models import Show

# Custom imports
from .league import config as league_config


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
def htmx_wrestler_create(request):
    # Get form data & create wrestler
    if request.method == "POST":
        # Check for max wrestlers
        discord_user = DiscordUser.objects.get(user=request.user)
        if discord_user.wrestler_set.count() >= league_config.max_wrestlers:
            return HttpResponse("You have reached the maximum number of wrestlers allowed.")
        # Get some form data
        form_data = {}
        form_data["twitch_handle"] = request.POST.get("twitch_handle")
        form_data["worker_name"] = request.POST.get("wrestler_name")
        form_data["origin_story"] = request.POST.get("origin_story")
        form_data["nationality"] = request.POST.get("nationality")
        form_data["appearance"] = request.POST.get("appearance")
        form_data["gender"] = request.POST.get("gender")
        form_data["weightclass"] = request.POST.get("weightclass")
        form_data["wrestler_class"] = request.POST.get("wrestler_class")
        form_data["former_profession"] = request.POST.get("former_profession")
        form_data["age"] = request.POST.get("age")
        form_data["attire"] = request.POST.get("attire")
        form_data["colorscheme"] = request.POST.get("colorscheme")
        form_data["entrance"] = request.POST.get("entrance")
        form_data["moveset"] = request.POST.get("moveset")
        form_data["prideful"] = request.POST.get("prideful")
        form_data["respectful"] = request.POST.get("respectful")
        form_data["perserverant"] = request.POST.get("perserverant")
        form_data["loyal"] = request.POST.get("loyal")
        form_data["bold"] = request.POST.get("bold")
        form_data["disciplined"] = request.POST.get("disciplined")
        # Validate & create the wrestler



    return render(request, 'wrestling/wrestler/htmx_create.html')