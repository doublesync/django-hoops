# Django imports
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Sum
from django.template.loader import render_to_string
from django.utils import timezone
from django.views import View

# Custom imports
import json

# Main application imports
from main.models import Player
from main.models import Team
from stats.models import Statline
from stats.models import Game

# Actual view functions
def index(request):
    return HttpResponse("Hello, world. You're at the stats index.")

def add_game(request):
    context = {
        "teams": Team.objects.all(),
    }
    return render(request, "stats/editing/add_game.html", context)


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
        # Create the game object
        game = Game.objects.create(
            day=day,
            home=home_team_object,
            away=away_team_object,
            home_points=home_score,
            away_points=away_score,
            winner = home_team_object if home_score > away_score else away_team_object,
            loser = home_team_object if home_score < away_score else away_team_object,
        )
        game.save()
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
        # Return the success message (refresh page and clear form)
        messages.success(request, "✅ Game added successfully!")
        response = HttpResponse("")
        response['HX-Refresh'] = 'true'
        return response