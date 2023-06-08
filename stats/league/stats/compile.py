# Django imports
from stats.models import Game
from stats.models import Statline
from main.models import Player
from main.models import Team

# Stats imports
from stats.league.stats import calculate as stats_calculate

# Custom imports
import json


# Compile all seasons and their days (and their games)
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

# Compile one season and it's days (and it's games)
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

# Compile one player and it's stats
def player_stats(player, season, playoffs=False, career=False):
    # Create the player dictionary
    player_stats = {
        "season": season,
        "averages": {},
        "advanced": {},
        "totals": {
            "GP": 0,
        },
    }
    # Find the player's statlines based on the season type
    if career:
        player_career_stats = career_stats(player)
        return player_career_stats
    elif playoffs:
        player_stats["season"] = season + " Playoffs"
        statlines = Statline.objects.filter(player=player, game__season=season, game__game_type="PLY")
    else:
        statlines = Statline.objects.filter(player=player, game__season=season, game__game_type="REG")
    # Check if the player has any statlines
    if len(statlines) > 0:
        # Add the player totals to the dictionary
        for line in statlines:
            # Add the statline totals to the dictionary
            player_stats["totals"]["PTS"] = line.points
            player_stats["totals"]["REB"] = line.rebounds
            player_stats["totals"]["OREB"] = line.offensive_rebounds
            player_stats["totals"]["DREB"] = line.defensive_rebounds
            player_stats["totals"]["AST"] = line.assists
            player_stats["totals"]["STL"] = line.steals
            player_stats["totals"]["BLK"] = line.blocks
            player_stats["totals"]["TOV"] = line.turnovers
            player_stats["totals"]["FGM"] = line.field_goals_made
            player_stats["totals"]["FGA"] = line.field_goals_attempted
            player_stats["totals"]["3PM"] = line.three_pointers_made
            player_stats["totals"]["3PA"] = line.three_pointers_attempted
            player_stats["totals"]["FTM"] = line.free_throws_made
            player_stats["totals"]["FTA"] = line.free_throws_attempted
            player_stats["totals"]["PF"] = line.personal_fouls
            player_stats["totals"]["GP"] += 1
            # Add the statline advanced stats to the dictionary
            player_stats["totals"]["GMSC"] = stats_calculate.get_game_score(line)
        # Based on the totals, add the averages to the dictionary
        player_totals = player_stats["totals"]
        player_stats["averages"]["PPG"] = round(player_totals["PTS"] / player_totals["GP"], 2)
        player_stats["averages"]["RPG"] = round(player_totals["REB"] / player_totals["GP"], 2)
        player_stats["averages"]["OREB"] = round(player_totals["OREB"] / player_totals["GP"], 2)
        player_stats["averages"]["DREB"] = round(player_totals["DREB"] / player_totals["GP"], 2)
        player_stats["averages"]["APG"] = round(player_totals["AST"] / player_totals["GP"], 2)
        player_stats["averages"]["SPG"] = round(player_totals["STL"] / player_totals["GP"], 2)
        player_stats["averages"]["BPG"] = round(player_totals["BLK"] / player_totals["GP"], 2)
        player_stats["averages"]["TPG"] = round(player_totals["TOV"] / player_totals["GP"], 2)
        player_stats["averages"]["FGM"] = round(player_totals["FGM"] / player_totals["GP"], 2)
        player_stats["averages"]["FGA"] = round(player_totals["FGA"] / player_totals["GP"], 2)
        player_stats["averages"]["FGP"] = round(player_totals["FGM"] / player_totals["FGA"], 2)
        player_stats["averages"]["3PM"] = round(player_totals["3PM"] / player_totals["GP"], 2)
        player_stats["averages"]["3PA"] = round(player_totals["3PA"] / player_totals["GP"], 2)
        player_stats["averages"]["3PP"] = round(player_totals["3PM"] / player_totals["3PA"], 2)
        player_stats["averages"]["FTM"] = round(player_totals["FTM"] / player_totals["GP"], 2)
        player_stats["averages"]["FTA"] = round(player_totals["FTA"] / player_totals["GP"], 2)
        player_stats["averages"]["FTP"] = round(player_totals["FTM"] / player_totals["FTA"], 2)
        player_stats["averages"]["FPG"] = round(player_totals["PF"] / player_totals["GP"], 2)
        # Based on the totals, add the average advanced stats to the dictionary
        player_stats["advanced"]["GMSC"] = round(player_totals["GMSC"] / player_totals["GP"], 2)
    # Return the player dictionary
    return player_stats

# Compile one player's career stats
def career_stats(player):
    # Create the player dictionary
    player_career_stats = {}
    # Find the player's eligible seasons
    seasons = []
    for line in Statline.objects.filter(player=player):
        if line.game.season not in seasons:
            seasons.append(line.game.season)
    # Add the player's career totals to the dictionary
    for season in seasons:
        player_career_stats[season] = player_stats(player=player, season=season)
    # Return the player dictionary
    return player_career_stats