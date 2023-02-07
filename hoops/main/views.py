# Django imports
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required

# Model imports
from .models import DiscordUser
from .models import Player
from .models import FeatureList
from .models import HistoryList
from .models import Team

# Form imports
from .forms import PlayerForm
from .forms import UpgradeForm

# Custom imports
from .discord import auth as discord_auth
from .league import config as league_config
from .league import methods as league_methods

# .ENV file import
import os, json
from dotenv import load_dotenv
load_dotenv()

# Create your views here.
# @login_required(login_url="/login/discord/")
def home(request):
    current_user = request.user
    context = {
        "title": "Home",
        "current_user": current_user,
    }
    return render(request, "main/league/home.html", context)

def login(request):
    return HttpResponse("Hello, world. This is the login page.")

def login_discord(request):
    discord_auth_url = os.environ.get("DISCORD_AUTH_URL")
    return redirect(discord_auth_url)

def login_discord_redirect(request):
    # Get information from Discord
    code = request.GET.get('code')
    info = discord_auth.exchange_code(code)
    user = info[0]
    guilds = info[1]
    # Create the discord user
    discord_user = authenticate(request, user=user)
    discord_user = list(discord_user).pop()
    # Finally, log the user in
    django_login(request, discord_user, backend="main.authorize.DiscordBackend")
    return redirect(home)

def logout(request):
    django_logout(request)
    return redirect("/")

def player(request, id):
    player_object = Player.objects.get(pk=id)
    context = {
        "title": f"{player_object.first_name} {player_object.last_name}",
        "player": player_object,
        "player_currency": {
            "primary_currency_name": (league_config.primary_currency_name).capitalize(),
            "secondary_currency_name": (league_config.secondary_currency_name).capitalize(),
            "primary_currency": getattr(player_object, league_config.primary_currency_name),
            "secondary_currency": getattr(player_object, league_config.secondary_currency_name),
        }
    }
    return render(request, "main/players/player.html", context)

@login_required(login_url="/login/discord/")
def upgrade_player(request, id):
    # Collect user & player information
    # Quick Note: The player attributes & badges are formatted differently in the database
    # than they are in the game. The database stores them with more user-friendly names,
    # while the game stores them with more game-friendly names. This is why we have to
    # convert the attributes & badges from the database to the game-friendly names
    # before we can export them for game use.
    user = request.user
    player = league_methods.get_player(id)
    # Check if the player exists (or not)
    if player:
        if player.discord_user == user:
            # Initialize the prefill information
            prefill_info = dict(player.attributes, **player.badges) # Combine the attributes & badges into one dictionary
            prefill_info = {k.lower(): v for k, v in prefill_info.items()} # To match field names in the form (lowercase)
            prefill_info = {k.replace(" ", "_"): v for k, v in prefill_info.items()} # To match field names in the form (underscores)
            # Initialize the context
            context = {
                "title": "Upgrade Player", 
                "player": player, 
                "upgrade_player_form": UpgradeForm(initial=prefill_info),
            }
            return render(request, "main/players/upgrade.html", context)
        else:
            return HttpResponse(f"Sorry, you don't own {player.first_name} {player.last_name}!")
    else:
        return HttpResponse("Sorry, this player doesn't exist!")

@login_required(login_url="/login/discord/")
def create_player(request):
    context = {
        "title": "Create Player",
        "create_player_form": PlayerForm,
    }
    return render(request, "main/players/create.html", context)

def players(request):
    context = {
        "title": "Players",
        "players": Player.objects.all(),
    }
    return render(request, "main/players/players.html", context)

def team(request, id):
    team_object = Team.objects.get(pk=id)
    context = {
        "title": team_object.name,
        "team": team_object,
    }
    return render(request, "main/teams/team.html", context)

def teams(request):
    context = {
        "title": "Teams",
        "teams": Team.objects.all(),
    }
    return render(request, "main/teams/teams.html", context)