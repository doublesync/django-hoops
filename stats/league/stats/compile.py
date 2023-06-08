# Django imports
from stats.models import Game
from stats.models import Statline
from main.models import Player
from main.models import Team

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
    # Find each game and add it to the season & day
    for game in Game.objects.filter(season=season):
        if game.day not in season_dict:
            season_dict["days"][game.day] = {
                "id": game.day,
                "games": [
                    {
                        "id": game.id,
                        "data": {
                            "home": game.home.id,
                            "away": game.away.id,
                            "home_score": game.home_points,
                            "away_score": game.away_points,
                            "winner": game.winner.abbrev,
                            "loser": game.loser.abbrev,
                        }
                    }
                ],
            }
        else:
            season_dict["days"][game.day]["games"].append(
                {
                    "id": game.id,
                    "data": {
                        "home": game.home.id,
                        "away": game.away.id,
                        "home_score": game.home_points,
                        "away_score": game.away_points,
                        "winner": game.winner.abbrev,
                        "loser": game.loser.abbrev,
                    }
                }
            )
    # Return the season dictionary
    return season_dict
