# Django imports
from stats.models import Game
from stats.models import Statline
from main.models import Player
from main.models import Team

# Stats imports
from stats.league.stats import calculate as stats_calculate

# Custom imports
import json


# Compile functions
def all_seasons():
    # Create the seasons dictionary
    seasons = {}
    all_games = Game.objects.all()
    # Find each game and add it to the season & day
    for game in all_games:
        seasons[game.season] = {
            "id": game.season,
            "data": one_season(game.season)
        }
    # Return the seasons dictionary
    return seasons

def one_season(season):
    # Create the season dictionary
    season_dict = {
        "id": season,
        "days": {},
    }
    # Add each day to the season dictionary
    def add_game_to_day(game_adding):
        # Find the day dictionary
        day_dict = season_dict["days"][game_adding.day]["games"]
        # Find winning & losing scores
        if game_adding.winner == game_adding.home:
            winning_score = game_adding.home_points
            losing_score = game_adding.away_points
        else:
            winning_score = game_adding.away_points
            losing_score = game_adding.home_points
        # Add the game to the day dictionary
        day_dict.append({
            "id": game_adding.id,
            "home": game_adding.home.id,
            "away": game_adding.away.id,
            "winning_score": game_adding.home_points,
            "losing_score": game_adding.away_points,
            "winner": game_adding.winner.abbrev,
            "loser": game_adding.loser.abbrev,
        })
    # Find each game and add it to the season & day
    for game in Game.objects.filter(season=season):
        if game.day not in season_dict["days"]:
            season_dict["days"][game.day] = {
                "id": game.day,
                "games": [],
            }
        # Add the game to the day dictionary
        add_game_to_day(game)

    # Order each team in standings by wins
    season_dict["standings"] = stats_calculate.get_standings(season)
    # Return the season dictionary
    return season_dict
