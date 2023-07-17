# Django imports
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.template.loader import render_to_string
from django.db.utils import IntegrityError

from rest_framework.response import Response
from rest_framework.decorators import api_view

# Custom imports
import json

# Main imports
from main.league import config as league_config

# Stat imports
from stats.models import SeasonAverage
from stats.models import SeasonTotal
from stats.league import config as stats_config
from stats.league.stats import compile as stats_compile

# Serializers
from stats.serializers import SeasonAverageSerializer
from stats.serializers import SeasonTotalSerializer

# Main application imports
from main.models import Player
from main.models import Team
from stats.models import Statline
from stats.models import Game

# Index function
def index(request):
    # Create the context
    context = {
        "active_seasons": stats_config.active_seasons,
        "recent_games": Game.objects.all().order_by("-day")[:8],
        "current_season": stats_compile.one_season(league_config.current_season),
        "season_id": league_config.current_season,
    }
    # Get standing based on current_season
    return render(request, "stats/viewing/view_home.html", context)

# Game statistic functions
def add_game(request):
    context = {
        "teams": Team.objects.all(),
    }
    return render(request, "stats/editing/add_game.html", context)

def view_game(request, id):
    # Attempt to find the game
    try:
        game_viewing = Game.objects.get(id=id)
    except:
        return HttpResponse("❌ Game does not exist!")
    # Find the statlines of home & away players
    home_statlines = Statline.objects.filter(game=game_viewing, team_at_time=game_viewing.home)
    away_statlines = Statline.objects.filter(game=game_viewing, team_at_time=game_viewing.away)
    # Create the context
    context = {
        "game": game_viewing,
        "home_statlines": home_statlines,
        "away_statlines": away_statlines,
    }
    return render(request, "stats/viewing/view_game.html", context)

def view_season(request, id):
    # Attempt to find the season
    if not Game.objects.filter(season=id).exists():
        return HttpResponse("❌ Season does not exist!")
    # Create the context
    context = {
        "season": Game.objects.filter(season=id),
        "season_viewing": stats_compile.one_season(id),
        "top_performers": stats_compile.top_performers(id),
    }
    return render(request, "stats/viewing/view_season.html", context)

def view_season_stats(request, id):
    # Get the season stats
    sorted_stats = stats_compile.all_player_stats(id)
    sorted_stats = list(sorted_stats.items())
    # Paginate sorted_stats
    paginator = Paginator(sorted_stats, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Create the context
    context = {
        "season": id,
        "sorted_stats": page_obj,
        "sort_options": stats_config.average_sort_options,
        "page": page_obj,
    }
    return render(request, "stats/viewing/view_stats.html", context)

# HTMX check functions
def check_stats_roster(request):
    if request.method == "POST":
        # Get the form data
        home_team = request.POST.get("home_team")
        away_team = request.POST.get("away_team")
        # Validate both teams
        if home_team and away_team:
            # Get the team roster
            home_team_object = Team.objects.get(id=home_team)
            away_team_object = Team.objects.get(id=away_team)
            # Send roster back
            context = {
                "teams": Team.objects.all(),
                "home_team": home_team_object,
                "away_team": away_team_object,
            }
            html = render_to_string("stats/ajax/team_list_fragment.html", context)
            return HttpResponse(html)
    else:
        return HttpResponse("❌ Invalid request!")

def validate_game(request):
    if request.method == "POST":
        # Get the form data
        day = request.POST.get("day")
        home_team = request.POST.get("home_team")
        away_team = request.POST.get("away_team")
        home_score = request.POST.get("home_score")
        away_score = request.POST.get("away_score")
        game_type = request.POST.get("game_type")
        game_data = {
            "home": {},
            "away": {},
        }
        game_stats = ["reb", "ast", "stl", "blk", "tov", "fgm", "fga", "3pm", "3pa", "ftm", "fta", "oreb", "fouls"]
        # Validate both teams
        if not day:
            return HttpResponse("❌ Day is missing!")
        if not home_team or not away_team:
            return HttpResponse("❌ Home or away team does not exist!")
        if home_team == away_team:
            return HttpResponse("❌ Home and away team cannot be the same!")
        if not home_score or not away_score:
            return HttpResponse("❌ Home or away score is missing!")
        if home_score == away_score:
            return HttpResponse("❌ Home and away score cannot be the same!")
        # If everything is ok, get the teams
        home_team_object = Team.objects.get(id=home_team)
        away_team_object = Team.objects.get(id=away_team)
        # If everything is ok, get the home players' stats
        for home_player in home_team_object.player_set.all():
            game_data["home"][home_player.id] = {}
            hps = game_data["home"][home_player.id]
            for stat in game_stats:
                value = request.POST.get(f"{home_player.id}_{stat}")
                if not value:
                    return HttpResponse(f"❌ {home_player.first_name} {home_player.last_name} is missing {stat}!")
                hps[stat] = int(value)
        # If everything is ok, get the away players' stats
        for away_player in away_team_object.player_set.all():
            game_data["away"][away_player.id] = {}
            hps = game_data["away"][away_player.id]
            for stat in game_stats:
                value = request.POST.get(f"{away_player.id}_{stat}")
                if not value:
                    return HttpResponse(f"❌ {away_player.first_name} {away_player.last_name} is missing {stat}!")
                hps[stat] = int(value)
        # Check if a game with the same teams and day exists (even if they are different home/away)
        if Game.objects.filter(
            Q(home=home_team_object, away=away_team_object, day=day) | 
            Q(home=away_team_object, away=home_team_object, day=day)
        ).exists():
            return HttpResponse("❌ Game already exists!")
        # Create the game object
        game = Game.objects.create(
            day=day,
            home=home_team_object,
            away=away_team_object,
            home_points=home_score,
            away_points=away_score,
            winner=home_team_object if home_score > away_score else away_team_object,
            loser=home_team_object if home_score < away_score else away_team_object,
            game_type=game_type,
        )
        game.save()
        # Create a list of players to update their stats
        players_to_update = []
        # Try to create the statline objects
        try:
            # Create the statline objects for the home team
            for id, stats in game_data["home"].items():
                # Find some player information
                id = int(id)
                player = Player.objects.get(id=id)
                # Create the statline
                statline = Statline.objects.create(
                    rebounds=stats["reb"],
                    assists=stats["ast"],
                    steals=stats["stl"],
                    blocks=stats["blk"],
                    turnovers=stats["tov"],
                    field_goals_made=stats["fgm"],
                    field_goals_attempted=stats["fga"],
                    three_pointers_made=stats["3pm"],
                    three_pointers_attempted=stats["3pa"],
                    free_throws_made=stats["ftm"],
                    free_throws_attempted=stats["fta"],
                    offensive_rebounds=stats["oreb"],
                    personal_fouls=stats["fouls"],
                    game=game,
                    player=player,
                    team_at_time=home_team_object,
                )
                statline.save()
                players_to_update.append(player)
            # Create the statline objects for the away team
            for id, stats in game_data["away"].items():
                # Find some player information
                id = int(id)
                player = Player.objects.get(id=id)
                # Create the statline
                statline = Statline.objects.create(
                    rebounds=stats["reb"],
                    assists=stats["ast"],
                    steals=stats["stl"],
                    blocks=stats["blk"],
                    turnovers=stats["tov"],
                    field_goals_made=stats["fgm"],
                    field_goals_attempted=stats["fga"],
                    three_pointers_made=stats["3pm"],
                    three_pointers_attempted=stats["3pa"],
                    free_throws_made=stats["ftm"],
                    free_throws_attempted=stats["fta"],
                    offensive_rebounds=stats["oreb"],
                    personal_fouls=stats["fouls"],
                    game=game,
                    player=player,
                    team_at_time=away_team_object,
                )
                statline.save()
                players_to_update.append(player)
        except IntegrityError:
            # Delete the game object
            game.delete()
            # Return the error message
            return HttpResponse("❌ You have a statistic that is too high!")
        # Check for 'SeasonAverage' and 'SeasonTotal' objects (this updates the averages & totals for the specific game type in a season)
        for player_updating in players_to_update:
            # Try to add the 'SeasonAverage' object
            try:
                # Create the season average object
                season_average = SeasonAverage.objects.create(
                    season=game.season,
                    team=player_updating.current_team,
                    player=player_updating,
                    game_type=game_type,
                )
                season_average.save()
            except:
                SeasonAverage.objects.get(player=player_updating, season=game.season, team=player_updating.current_team, game_type=game_type).save()
            # Try to add the 'SeasonTotal' object
            try:
                # Create the season total object
                season_total = SeasonTotal.objects.create(
                    season=game.season,
                    team=player_updating.current_team,
                    player=player_updating,
                    game_type=game_type,
                )
                season_total.save()
            except:
                SeasonTotal.objects.get(player=player_updating, season=game.season, team=player_updating.current_team, game_type=game_type).save()
        # Return the success message (refresh page and clear form)
        messages.success(request, f"✅ Game added successfully! [#{game.id}]")
        response = HttpResponse()
        response['HX-Refresh'] = "true"
        return response

# This needs to be more efficient
# Serialize the data first
# Include (all_player_stats) in the htmx request
# The only time compilation should happen is in (view_season_stats)
# Use the data sent from the htmx request to sort the stats
# Instead of accessing the database every htmx request
def sort_stats(request, page):
    # Get the form data
    season = request.POST.get("season")
    season_type = request.POST.get("season_type")
    sort_by = request.POST.get("sort_by")
    pos_type = request.POST.get("pos_type")
    arch_type = request.POST.get("arch_type")
    trait_type = request.POST.get("trait_type")
    status_type = request.POST.get("status_type")
    # Validate both teams
    if not sort_by or not season or not season_type:
        return HttpResponse("❌ Sort by, season, or season type is missing or wrong!")
    # Build the queryset
    queryset = Player.objects.all()
    # Filter the queryset
    if pos_type and pos_type != "ALL":
        queryset = queryset.filter(Q(primary_position=pos_type))
    if arch_type and arch_type != "ALL":
        queryset = queryset.filter(Q(primary_archetype=arch_type))
    if trait_type and trait_type != "ALL":
        queryset = queryset.filter(Q(trait_one=trait_type) | Q(trait_two=trait_type) | Q(trait_three=trait_type))
    if status_type and status_type != "ALL":
        if status_type == "ACTIVE":
            queryset = queryset.filter(Q(current_team__isnull=False))
        elif status_type == "FREEAGENT":
            queryset = queryset.filter(Q(current_team__isnull=True))
        elif status_type == "ROOKIE":
            queryset = queryset.filter(Q(years_played=1))
    # Filtering the statistics to show
    show_playoffs = False
    show_finals = False
    if season_type == "PLY": 
        show_playoffs = True
    elif season_type == "FIN":
        show_finals = True
    # If everything is ok, find the sorted stats
    season_player_stats = stats_compile.all_player_stats(season=int(season), all_players=queryset, custom_query=True, playoffs=show_playoffs, finals=show_finals)
    # Deciding which index to use
    index_to_use = "averages"
    if sort_by in stats_config.totals_sort_options:
        index_to_use = "totals"
    # Set 'index_to_use'
    # Sort the stats by the sort_by
    # Must make the sort_by options equivalent to the keys in the season_player_stats
    sorted_stats = sorted(season_player_stats.values(), key=lambda x: x["yearly_stats"][index_to_use][sort_by], reverse=True)
    sorted_stats = {player["id"]: player for player in sorted_stats}
    sorted_stats = list(sorted_stats.items())
    # Paginate sorted_stats
    paginator = Paginator(sorted_stats, 10)
    page_obj = paginator.get_page(page)
    # Send the sorted stats back
    context = {
        "index_to_use": index_to_use,
        "sorted_stats": page_obj,
        "sort_options": stats_config.sort_by_options[index_to_use],
        "page": page_obj,
    }
    html = render_to_string("stats/ajax/sort_stats_fragment.html", context)
    # Return the sorted stats fragment
    return HttpResponse(html)
    
def find_options(request):
    if request.method == "POST":
        # Get the form data
        season = request.POST.get("season")
        sort_type = request.POST.get("sort_type")
        # Validate the sort type
        if not sort_type or sort_type not in stats_config.sort_by_options:
            return HttpResponse("❌ Sort type is missing or wrong!")
        # If everything is ok, find the options
        options = stats_config.sort_by_options[sort_type]
        # Send the options back
        context = {
            "sort_options": options,
        }
        html = render_to_string("stats/ajax/sort_options_fragment.html", context)
        # Return the options fragment
        return HttpResponse(html)
    
# API functions
@api_view(['GET'])
def season_stats_api(request):
    if request.method == "GET":
        # Get the form data
        season = request.GET.get("season")
        # Validate the season
        if not season:
            return HttpResponse("❌ Season is missing!")
        # If everything is ok, find the stats
        season_player_stats = stats_compile.all_player_stats(int(season))
        yearly_player_stats = {}
        # Iterate through each player and serialize their SeasonAverage and SeasonTotal objects
        for id, player in season_player_stats.items():
            # Try to find the player's discord id
            try:
                player_object = Player.objects.get(id=int(id))
                player_discord_id = player_object.discord_user.id
            except:
                player_discord_id = None
            # Add the player's stats to the yearly_player_stats
            yearly_player_stats[player["name"]] = {
                "id": id,
                "discord_id": player_discord_id,
                "name": player["name"],
                "season": player["season"],
                "averages": player["yearly_stats"]["averages"],
                "totals": player["yearly_stats"]["totals"],
            }
        # Return the stats
        return Response(yearly_player_stats)
    else:
        return HttpResponse("❌ Invalid request!")