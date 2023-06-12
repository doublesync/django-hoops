# Django imports
from django.db.models import Q

# Main imports
from main.models import Player
from main.models import Team

# Stats imports
from stats.models import Game
from stats.models import Statline
from stats.league.stats import calculate as stats_calculate

# Custom imports
import json
import copy


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
            "winning_score": winning_score,
            "losing_score": losing_score,
            "winner": game_adding.winner.abbrev,
            "loser": game_adding.loser.abbrev,
        })
    # Find each game and add it to the season & day
    season_games = Game.objects.filter(season=season).order_by("day")
    for game in season_games:
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
def player_stats(player, season, playoffs=False, finals=False, career=False):
    # Create the templates
    averages_template = {
        "PPG": 0,
        "RPG": 0,
        "OREB": 0,
        "DREB": 0,
        "APG": 0,
        "SPG": 0,
        "BPG": 0,
        "TPG": 0,
        "FPG": 0,
        "FGM": 0,
        "FGA": 0,
        "3PM": 0,
        "3PA": 0,
        "FTM": 0,
        "FTA": 0,
        "FGP": 0,
        "3PP": 0,
        "FTP": 0,
    }
    advanced_template = {
        "GMSC": 0,
    }
    totals_template = {
        "GP": 0,
        "PTS": 0,
        "REB": 0,
        "OREB": 0,
        "DREB": 0,
        "AST": 0,
        "STL": 0,
        "BLK": 0,
        "TOV": 0,
        "FGM": 0,
        "FGA": 0,
        "3PM": 0,
        "3PA": 0,
        "FTM": 0,
        "FTA": 0,
        "PF": 0,
        "GMSC": 0,
    }
    # Create the player dictionary
    player_stats = {
        "id": player.id,
        "name": f"{player.first_name} {player.last_name}",
        "season": season,
        "stats": {},
        "full_year_stats": {
            "averages": {},
            "totals": {},
            "advanced": {},
        },
    }
    # Find the player's statlines based on the season type
    if career:
        player_career_stats = career_stats(player)
        return player_career_stats
    elif playoffs:
        player_stats["season"] = season + " Playoffs"
        statlines = Statline.objects.filter(player=player, game__season=season, game__game_type="PLY")
    elif finals:
        player_stats["season"] = season + " Finals"
        statlines = Statline.objects.filter(player=player, game__season=season, game__game_type="FIN")
    else:
        statlines = Statline.objects.filter(player=player, game__season=season, game__game_type="REG")
    # Check if the player has any statlines
    if len(statlines) > 0:
        # Add the player totals to the dictionary (separate by teams)
        for line in statlines:
            # Add team to the dictionary if it doesn't exist
            team_abbrev = line.team_at_time.abbrev
            if team_abbrev not in player_stats["stats"]:
                player_stats["stats"][team_abbrev] = {
                    "averages": averages_template.copy(),
                    "advanced": advanced_template.copy(),
                    "totals": totals_template.copy(),
                }
            # Add the statline totals to the dictionary
            player_stats["stats"][team_abbrev]["totals"]["GP"] += 1
            player_stats["stats"][team_abbrev]["totals"]["PTS"] += line.points
            player_stats["stats"][team_abbrev]["totals"]["REB"] += line.rebounds
            player_stats["stats"][team_abbrev]["totals"]["OREB"] += line.offensive_rebounds
            player_stats["stats"][team_abbrev]["totals"]["DREB"] += line.defensive_rebounds
            player_stats["stats"][team_abbrev]["totals"]["AST"] += line.assists
            player_stats["stats"][team_abbrev]["totals"]["STL"] += line.steals
            player_stats["stats"][team_abbrev]["totals"]["BLK"] += line.blocks
            player_stats["stats"][team_abbrev]["totals"]["TOV"] += line.turnovers
            player_stats["stats"][team_abbrev]["totals"]["FGM"] += line.field_goals_made
            player_stats["stats"][team_abbrev]["totals"]["FGA"] += line.field_goals_attempted
            player_stats["stats"][team_abbrev]["totals"]["3PM"] += line.three_pointers_made
            player_stats["stats"][team_abbrev]["totals"]["3PA"] += line.three_pointers_attempted
            player_stats["stats"][team_abbrev]["totals"]["FTM"] += line.free_throws_made
            player_stats["stats"][team_abbrev]["totals"]["FTA"] += line.free_throws_attempted
            player_stats["stats"][team_abbrev]["totals"]["PF"] += line.personal_fouls
            # Add the statline advanced stats to the dictionary
            player_stats["stats"][team_abbrev]["totals"]["GMSC"] += stats_calculate.get_game_score(line)
        # Combine the player's individual team stats into yearly stats (track who they plyed for)
        for team_at_time, stats_on_team in player_stats["stats"].items():
            # Adding the totals to the full year stats
            for stat, value in stats_on_team["totals"].items():
                if stat not in player_stats["full_year_stats"]["totals"]:
                    player_stats["full_year_stats"]["totals"][stat] = value
                else:
                    player_stats["full_year_stats"]["totals"][stat] += value
            # Update the averages for the team & full year stats
            totals_on_team = player_stats["stats"][team_at_time]["totals"]
            stats_on_team["averages"]["PPG"] = round(totals_on_team["PTS"] / totals_on_team["GP"], 1)
            stats_on_team["averages"]["RPG"] = round(totals_on_team["REB"] / totals_on_team["GP"], 1)
            stats_on_team["averages"]["OREB"] = round(totals_on_team["OREB"] / totals_on_team["GP"], 1)
            stats_on_team["averages"]["DREB"] = round(totals_on_team["DREB"] / totals_on_team["GP"], 1)
            stats_on_team["averages"]["APG"] = round(totals_on_team["AST"] / totals_on_team["GP"], 1)
            stats_on_team["averages"]["SPG"] = round(totals_on_team["STL"] / totals_on_team["GP"], 1)
            stats_on_team["averages"]["BPG"] = round(totals_on_team["BLK"] / totals_on_team["GP"], 1)
            stats_on_team["averages"]["TPG"] = round(totals_on_team["TOV"] / totals_on_team["GP"], 1)
            stats_on_team["averages"]["FGM"] = round(totals_on_team["FGM"] / totals_on_team["GP"], 1)
            stats_on_team["averages"]["FGA"] = round(totals_on_team["FGA"] / totals_on_team["GP"], 1)
            stats_on_team["averages"]["3PM"] = round(totals_on_team["3PM"] / totals_on_team["GP"], 1)
            stats_on_team["averages"]["3PA"] = round(totals_on_team["3PA"] / totals_on_team["GP"], 1)
            stats_on_team["averages"]["FTM"] = round(totals_on_team["FTM"] / totals_on_team["GP"], 1)
            stats_on_team["averages"]["FTA"] = round(totals_on_team["FTA"] / totals_on_team["GP"], 1)
            stats_on_team["averages"]["FPG"] = round(totals_on_team["PF"] / totals_on_team["GP"], 1)
            # Percentage stats may cause division by zero
            if totals_on_team["FGA"] == 0 or totals_on_team["FGA"] == 0:
                stats_on_team["averages"]["FGP"] = 0
            else:
                stats_on_team["averages"]["FGP"] = round(totals_on_team["FGM"] / totals_on_team["FGA"] * 100, 1)
            if totals_on_team["3PM"] == 0 or totals_on_team["3PA"] == 0:
                stats_on_team["averages"]["3PP"] = 0
            else:
                stats_on_team["averages"]["3PP"] = round(totals_on_team["3PM"] / totals_on_team["3PA"] * 100, 1)
            if totals_on_team["FTA"] == 0 or totals_on_team["FTM"] == 0:
                stats_on_team["averages"]["FTP"] = 0
            else:
                stats_on_team["averages"]["FTP"] = round(totals_on_team["FTM"] / totals_on_team["FTA"] * 100, 1)
            # Based on the totals, add the average advanced stats to the dictionary
            stats_on_team["advanced"]["GMSC"] = round(totals_on_team["GMSC"] / totals_on_team["GP"], 1)
        # Update the averages for the full year stats
        totals_on_team = player_stats["full_year_stats"]["totals"]
        player_stats["full_year_stats"]["averages"]["PPG"] = round(totals_on_team["PTS"] / totals_on_team["GP"], 1)
        player_stats["full_year_stats"]["averages"]["RPG"] = round(totals_on_team["REB"] / totals_on_team["GP"], 1)
        player_stats["full_year_stats"]["averages"]["OREB"] = round(totals_on_team["OREB"] / totals_on_team["GP"], 1)
        player_stats["full_year_stats"]["averages"]["DREB"] = round(totals_on_team["DREB"] / totals_on_team["GP"], 1)
        player_stats["full_year_stats"]["averages"]["APG"] = round(totals_on_team["AST"] / totals_on_team["GP"], 1)
        player_stats["full_year_stats"]["averages"]["SPG"] = round(totals_on_team["STL"] / totals_on_team["GP"], 1)
        player_stats["full_year_stats"]["averages"]["BPG"] = round(totals_on_team["BLK"] / totals_on_team["GP"], 1)
        player_stats["full_year_stats"]["averages"]["TPG"] = round(totals_on_team["TOV"] / totals_on_team["GP"], 1)
        player_stats["full_year_stats"]["averages"]["FGM"] = round(totals_on_team["FGM"] / totals_on_team["GP"], 1)
        player_stats["full_year_stats"]["averages"]["FGA"] = round(totals_on_team["FGA"] / totals_on_team["GP"], 1)
        player_stats["full_year_stats"]["averages"]["3PM"] = round(totals_on_team["3PM"] / totals_on_team["GP"], 1)
        player_stats["full_year_stats"]["averages"]["3PA"] = round(totals_on_team["3PA"] / totals_on_team["GP"], 1)
        player_stats["full_year_stats"]["averages"]["FTM"] = round(totals_on_team["FTM"] / totals_on_team["GP"], 1)
        player_stats["full_year_stats"]["averages"]["FTA"] = round(totals_on_team["FTA"] / totals_on_team["GP"], 1)
        player_stats["full_year_stats"]["averages"]["FPG"] = round(totals_on_team["PF"] / totals_on_team["GP"], 1)
        # Percentage stats may cause division by zero
        if totals_on_team["FGA"] == 0 or totals_on_team["FGA"] == 0:
            player_stats["full_year_stats"]["averages"]["FGP"] = 0
        else:
            player_stats["full_year_stats"]["averages"]["FGP"] = round(totals_on_team["FGM"] / totals_on_team["FGA"] * 100, 1)
        if totals_on_team["3PM"] == 0 or totals_on_team["3PA"] == 0:
            player_stats["full_year_stats"]["averages"]["3PP"] = 0
        else:
            player_stats["full_year_stats"]["averages"]["3PP"] = round(totals_on_team["3PM"] / totals_on_team["3PA"] * 100, 1)
        if totals_on_team["FTA"] == 0 or totals_on_team["FTM"] == 0:
            player_stats["full_year_stats"]["averages"]["FTP"] = 0
        else:
            player_stats["full_year_stats"]["averages"]["FTP"] = round(totals_on_team["FTM"] / totals_on_team["FTA"] * 100, 1)
        # Based on the totals, add the average advanced stats to the dictionary
        player_stats["full_year_stats"]["advanced"]["GMSC"] = round(totals_on_team["GMSC"] / totals_on_team["GP"], 1)
    # Return the player dictionary
    return player_stats

# Compile every player's stats
def all_player_stats(season, playoffs=False, finals=False, career=False):
    # Create the players dictionary
    player_stats_dict = {}
    # Find all of the players
    players = Player.objects.all()
    # Add each player's stats to the dictionary
    for player in players:
        one_player_stats = player_stats(player=player, season=season, playoffs=playoffs, finals=finals, career=career)
        one_player_totals = one_player_stats["full_year_stats"]["totals"]
        one_player_averages = one_player_stats["full_year_stats"]["averages"]
        one_player_advanced = one_player_stats["full_year_stats"]["advanced"]
        if one_player_totals and one_player_averages and one_player_advanced:           
            player_stats_dict[player.id] = one_player_stats
        else:
            continue
    # Return the players dictionary
    return player_stats_dict

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

# Compile player's last (x) games
def player_game_logs(player, x):
    # Create the 'player_game_logs' dictionary
    player_game_logs = []
    # Filter based on day, limit to (x)
    last_x_statlines = Statline.objects.filter(player=player).order_by("-game__day")[:x]
    # Add each statline to the dictionary
    for line in last_x_statlines:
        player_game_logs.append({
            "id": line.game.id,
            "day": line.game.day,
            "score": f"{line.game.home_points}-{line.game.away_points}",
            "winner": line.game.winner.abbrev,
            "loser": line.game.loser.abbrev,
            "stats" : {
                "PTS": line.points,
                "REB": line.rebounds,
                "OREB": line.offensive_rebounds,
                "DREB": line.defensive_rebounds,
                "AST": line.assists,
                "STL": line.steals,
                "BLK": line.blocks,
                "TOV": line.turnovers,
                "FGM": line.field_goals_made,
                "FGA": line.field_goals_attempted,
                "3PM": line.three_pointers_made,
                "3PA": line.three_pointers_attempted,
                "FTM": line.free_throws_made,
                "FTA": line.free_throws_attempted,
                "PF": line.personal_fouls,
                "GMSC": stats_calculate.get_game_score(line),
            }
        })
    # Return the player_game_logs dictionary
    return player_game_logs

# Compile team's last (x) games
def team_game_logs(team, x):
    # Create the 'team_game_logs' dictionary
    team_game_logs = []
    # Filter based on day, limit to (x)
    last_x_games = Game.objects.filter(Q(home=team) | Q(away=team)).order_by("-day")[:x]
    # Add each statline to the dictionary
    for game in last_x_games:
        team_game_logs.append({
            "id": game.id,
            "day": game.day,
            "score": f"{game.home_points}-{game.away_points}",
            "winner": game.winner.abbrev,
            "loser": game.loser.abbrev,
        })
    # Return the player_game_logs dictionary
    return team_game_logs

# Compile game of the day (for the home page)
def game_of_the_day(season, specific=None):
    # Find the latest (highest) day in the season
    latest_day = Game.objects.filter(season=season).latest("day").day if not specific else specific 
    # Find the statlines in the latest day
    day_games = Statline.objects.filter(game__day=latest_day)
    gotd = None
    # Find the game of the day
    for line in day_games:
        gmsc = stats_calculate.get_game_score(line)
        if gotd == None:
            gotd = line
        else:
            gotd_gmsc = stats_calculate.get_game_score(gotd)
            if gmsc > gotd_gmsc:
                gotd = line
    # Return the game of the day
    if gotd:
        return {
            "id": gotd.game.id,
            "pid": gotd.player.id,
            "day": gotd.game.day,
            "abbrev": gotd.team_at_time.abbrev,
            "gamescore": stats_calculate.get_game_score(gotd),
            "player": f"{gotd.player.first_name} {gotd.player.last_name}",
            "gamescore": stats_calculate.get_game_score(gotd),
            "points": gotd.points,
            "rebounds": gotd.rebounds,
            "assists": gotd.assists,
            "steals": gotd.steals,
            "blocks": gotd.blocks,
        }
    else:
        return None