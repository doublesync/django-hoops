# Django imports
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Model imports
from .models import Player
from .models import Team

# Form imports
from .forms import PlayerForm
from .forms import UpgradeForm

# Custom imports
from .discord import auth as discord_auth
from .discord import webhooks as discord_webhooks
from .league import config as league_config

# Custom packages
import copy
import json
import datetime

from .league.player import upgrade as hoops_player_upgrade
from .league.player import create as hoops_player_create
from .league.player import export as hoops_player_export
from .league.extra import convert as hoops_extra_convert

# .ENV file import
import os, json
from dotenv import load_dotenv

load_dotenv()

# Create your views here.
def home(request):
    current_user = request.user
    context = {
        "title": "Home",
        "current_user": current_user,
        "players": [],
    }
    # Send players to home page
    if current_user.is_authenticated:
        try:
            players = Player.objects.filter(discord_user=current_user)
            for p in players:
                context["players"].append(p)
        except ValueError:
            # If the user is still signed into an administration account
            redirect(logout)
    # Return the home page
    return render(request, "main/league/home.html", context)


def login(request):
    return HttpResponse("This is the login page.")


def login_discord(request):
    discord_auth_url = os.environ.get("DISCORD_AUTH_URL")
    return redirect(discord_auth_url)


def login_discord_redirect(request):
    try:
        # Get information from Discord
        code = request.GET.get("code")
        info = discord_auth.exchange_code(code)
        user = info[0]
        guilds = info[1]
        isInGuild = False
        # Check if the user is in the server
        for guild in guilds:
            if guild["id"] == os.environ.get("HOOPS_GUILD_ID"):
                isInGuild = True
                break
        # If the user is in the discord, create the user on the website
        if isInGuild:
            # Create the discord user
            discord_user = authenticate(request, user=user)
            discord_user = list(discord_user).pop()
            # Finally, log the user in
            django_login(request, discord_user, backend="main.authorize.DiscordBackend")
            # Send a success message
            messages.error(request, "You have successfully logged in!")
        else:
            # If the user isn't in the discord, redirect them to the home page with an error
            messages.error(request, "You aren't in the hoopsim discord server!")
    except:
        # Sometimes the user will be redirected to this page without a code
        messages.error(request, "Something went wrong while logging you in, try again!")
    # Redirect the user to the home page
    return redirect(home)


def logout(request):
    django_logout(request)
    return redirect("/")


def player(request, id):
    # Check if the player exists
    try:
        plr = Player.objects.get(pk=id)
    except Player.DoesNotExist:
        return HttpResponse("Sorry, this player doesn't exist!")
    # Initialize the context
    context = {
        # Page information
        "title": f"{plr.first_name} {plr.last_name}",
        "player": plr,
        "badgeEmojis": {0: "🚫", 1: "🟫", 2: "🌫️", 3: "🟨", 4: "🟪"},
        # Attribute categories
        "playmaking_attributes": league_config.attribute_categories["playmaking"],
        "shooting_attributes": league_config.attribute_categories["shooting"],
        "physical_attributes": league_config.attribute_categories["physical"],
        "defense_attributes": league_config.attribute_categories["defense"],
        "finishing_attributes": league_config.attribute_categories["finishing"],
        # Badge categories
        "finishing_badges": league_config.badge_categories["finishing"],
        "shooting_badges": league_config.badge_categories["shooting"],
        "playmaking_badges": league_config.badge_categories["playmaking"],
        "defense_badges": league_config.badge_categories["defense"],
        # Precalled methods
        "height_in_feet": hoops_extra_convert.convert_to_height(plr.height),
        "file": json.dumps(hoops_player_export.export_player(plr), indent=4),
    }
    return render(request, "main/players/player.html", context)


@login_required(login_url="/login/discord/")
def upgrade_player(request, id):
    # Collect user & player information
    user = request.user
    # Check if the player exists
    try:
        player = Player.objects.get(pk=id)
    except Player.DoesNotExist:
        return HttpResponse("Sorry, this player doesn't exist!")
    # Check if the user has permission to upgrade this player
    if not player.discord_user == user:
        return HttpResponse("Sorry, you don't have permission to upgrade this player!")
    # Process the request (if it's a POST request)
    if request.method == "POST":
        form = UpgradeForm(request.POST)
        if form.is_valid():
            # Remove unchanged attributes
            # So nothing is upgraded if the user doesn't change anything
            changed_data = {}
            cleaned_data = form.cleaned_data
            for k, v in cleaned_data.items():
                if k in player.attributes:
                    if int(v) > player.attributes[k]:
                        changed_data[k] = v
                elif k in player.badges:
                    if int(v) > player.badges[k]:
                        changed_data[k] = v
                elif k in player.tendencies:
                    if int(v) != player.tendencies[k]:
                        changed_data[k] = v
            # Attempt to upgrade the player
            response = hoops_player_upgrade.createUpgrade(player, changed_data)
            messages.success(request, response)
            # Send a webhook to Discord
            discord_webhooks.send_webhook(
                title="Player Upgrade",
                message=f"**{player.first_name} {player.last_name}** has attempted an upgrade. [View logs?](https://hoopscord.com/logs/upgrades/{player.id})\n```{response}```",
            )
            # Return to the player page
            return redirect(upgrade_player, id=id)
        else:
            messages.error(request, form.errors)
            return redirect(upgrade_player, id=id)
    else:
        # Combine attributes & badges + convert to Django form format
        prefill_info = dict(player.attributes, **player.badges, **player.tendencies)
        # Convert primary & secondary attributes to Django form format
        js_primary_attributes = league_config.archetype_attribute_bonuses[
            player.primary_archetype
        ]
        js_secondary_attributes = league_config.archetype_attribute_bonuses[
            player.secondary_archetype
        ]
        js_trait_one_badges = league_config.trait_badge_unlocks[player.trait_one]
        js_trait_two_badges = league_config.trait_badge_unlocks[player.trait_two]
        # Have to remove the 'range' function from attribute prices or javascript shits the bed
        js_attribute_prices = copy.deepcopy(league_config.attribute_prices)
        for _, v in js_attribute_prices.items():
            v["range"] = 0
        # Initialize the context
        context = {
            # Context items
            "title": "Upgrade Player",
            "player": player,
            "upgrade_player_form": UpgradeForm(initial=prefill_info),
            # Badges & attributes
            "badge_attributes": prefill_info,
            "badge_prices": league_config.badge_prices,
            "attribute_prices": js_attribute_prices,
            "attribute_bonuses": league_config.archetype_attribute_bonuses,
            "primary_attributes": js_primary_attributes,
            "secondary_attributes": js_secondary_attributes,
            # Traits
            "trait_one_badges": js_trait_one_badges,
            "trait_two_badges": js_trait_two_badges,
            # Attribute categories
            "finishing_attributes": league_config.attribute_categories["finishing"],
            "shooting_attributes": league_config.attribute_categories["shooting"],
            "playmaking_attributes": league_config.attribute_categories["playmaking"],
            "defense_attributes": league_config.attribute_categories["defense"],
            "physical_attributes": league_config.attribute_categories["physical"],
            # Badge categories
            "finishing_badges": league_config.badge_categories["finishing"],
            "shooting_badges": league_config.badge_categories["shooting"],
            "playmaking_badges": league_config.badge_categories["playmaking"],
            "defense_badges": league_config.badge_categories["defense"],
            # Tendency categories
            "initial_tendencies": league_config.initial_tendencies,
        }
        return render(request, "main/players/upgrade.html", context)


@login_required(login_url="/login/discord/")
def create_player(request):
    # Collect user & player information
    user = request.user
    # Process the request (if it's a POST request)
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            response = hoops_player_create.validatePlayerCreation(
                user, form.cleaned_data
            )
            success = response[0]
            status = response[1]
            # If the form is valid, and the player creation succeeded, redirect to the player page
            if success == True:
                playerObject = hoops_player_create.createPlayer(user, form.cleaned_data)
                # Create a discord webhook
                discord_webhooks.send_webhook(
                    title="Player Creation",
                    message=f"**{playerObject.first_name} {playerObject.last_name}** has been created. [View profile?](https://hoopscord.com/player/{playerObject.id})",
                )
                # Redirect to the player page
                return redirect(player, id=playerObject.id)
            else:
                messages.error(request, status)
                return redirect(create_player)
        # If the form is invalid, or the player creation failed, redirect to the create player page
        return redirect(create_player)
    else:
        context = {"create_player_form": PlayerForm}
        return render(request, "main/players/create.html", context)


def players(request):
    context = {
        "title": "Players",
        "players": Player.objects.all(),
    }
    return render(request, "main/players/players.html", context)


def upgrade_logs(request, id):
    # Check if the player exists
    try:
        player = Player.objects.get(pk=id)
    except Player.DoesNotExist:
        return HttpResponse("Sorry, this player doesn't exist!")
    # Get the upgrade logs
    logs = player.history_list.history["upgrade_logs"]
    logs.reverse()
    if player:
        context = {
            "name": f"{player.first_name} {player.last_name}",
            "logs": logs,
        }
        return render(request, "main/players/history.html", context)
    else:
        return HttpResponse("Sorry, this player doesn't exist!")


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


def trade(request):
    # Get the user
    user = request.user
    # Check if the user is a GM
    try:
        team = Team.objects.get(manager=user)
    except Team.DoesNotExist:
        return HttpResponse("Sorry, you don't have permission to view this page!")
    # Create the context
    context = {
        "title": "Trade",
        "my_team": team,
        "my_roster": team.player_set.all(),
    }
    return render(request, "main/teams/trade.html", context)


def daily_reward(request):
    # Get the current date
    user = request.user
    # Get the last date the daily rewards were given out
    last_reward = user.last_reward
    # If the daily rewards haven't been given out today, give them out
    if not last_reward:
        # Give the user their daily rewards
        # Update the user's last reward date
        pass
    else:
        # Check if the last reward was given out today
        # If it was, return an error
        # If it wasn't, give the user their daily rewards
        # and update the user's last reward date
        pass


def upgrades_pending(request):
    # Collect user & player information
    user = request.user
    if not user.can_update_players:
        return HttpResponse("Sorry, you don't have permission to view this page!")
    else:
        # Get the user's pending upgrades
        upgrades = Player.objects.filter(upgrades_pending=True)
        files = {}
        # Iterate through the players who have pending upgrades
        for player in upgrades:
            game_file = hoops_player_export.export_player(player)
            json_dump = json.dumps(game_file, indent=4)
            files[f"({player.id}) {player.first_name} {player.last_name}"] = json_dump
            player.upgrades_pending = False
            player.save()
        # Return the pending upgrades page
        return render(request, "main/players/pending.html", {"files": files})


def archetype_traits(request):
    context = {
        "title": "Archetypes & Traits",
        "starting": league_config.position_starting_attributes,
        "archetypes": league_config.archetype_attribute_bonuses,
        "traits": league_config.trait_badge_unlocks,
    }
    return render(request, "main/players/archetype-traits.html", context)


def build_info(request, tag):
    print(tag)
    context = {
        "title": "Archetypes & Traits",
        "use_key_and_value": False,
    }
    # Check if the tag is in the list of position starting attributes
    if tag in league_config.position_starting_attributes:
        context["header"] = tag
        context["info"] = league_config.position_starting_attributes[tag]
        context["use_key_and_value"] = True
    # Check if the tag is in archetype attribute bonuses
    elif tag in league_config.archetype_attribute_bonuses:
        context["header"] = tag.upper()
        context["info"] = league_config.archetype_attribute_bonuses[tag]
    # Check if the tag is in trait badge unlocks
    elif tag in league_config.trait_badge_unlocks:
        context["header"] = tag.upper()
        context["info"] = league_config.trait_badge_unlocks[tag]
    # Return the build info page
    return render(request, "main/players/build-info.html", context)
