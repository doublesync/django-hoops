# Django imports
from django.db.models import Q

# Custom imports
from stats.models import Game
from stats.models import Statline
from main.models import Player
from main.models import Team

def get_standings(season):
    # Create the standings dictionary
    standings = {}
    all_teams = Team.objects.all()
    
    # Function to calculate tie-breaker score based on head-to-head matchups
    def calculate_tie_breaker(team1, team2):      
        if team1["wins"] > team2["wins"]:
            return 1
        elif team1["wins"] < team2["wins"]:
            return -1
        else:
            return 0

    for team in all_teams:
        # Check if team should show on lists
        if not team.show_on_lists:
            continue
        
        # Add the team to the standings dictionary
        standings[team.name] = {
            # Team data
            "id": team.id,
            "abbrev": team.abbrev,
            "name": team.name,
            "logo": team.logo,
            # Standings data
            "total_games": 0,
            "home_games": 0,
            "away_games": 0,
            "home_points": 0,
            "away_points": 0,
            "wins": 0,
            "losses": 0,
            "points_for": 0,
            "points_against": 0,
            "points_diff": 0,
            # Averages
            "avg_points_for": 0,
            "avg_points_against": 0,
            "avg_points_diff": 0,
            "percentage": 0,
        }
        
        # Find all of the team data based on games
        for game in Game.objects.filter(Q(home=team) | Q(away=team), season=season):
            # Winner, or loser?
            if game.winner == team:
                standings[team.name]["wins"] += 1
            else:
                standings[team.name]["losses"] += 1
            
            # Home, or away?
            if game.home == team:
                standings[team.name]["total_games"] += 1
                standings[team.name]["home_games"] += 1
                standings[team.name]["points_for"] += game.home_points
                standings[team.name]["points_against"] += game.away_points
                standings[team.name]["points_diff"] += game.home_points - game.away_points
            else:
                standings[team.name]["total_games"] += 1
                standings[team.name]["away_games"] += 1
                standings[team.name]["points_for"] += game.away_points
                standings[team.name]["points_against"] += game.home_points
                standings[team.name]["points_diff"] += game.away_points - game.home_points
            
            # Calculate averages
            standings[team.name]["avg_points_for"] = round(standings[team.name]["points_for"] / (standings[team.name]["home_games"] + standings[team.name]["away_games"]), 1)
            standings[team.name]["avg_points_against"] = round(standings[team.name]["points_against"] / (standings[team.name]["home_games"] + standings[team.name]["away_games"]), 1)
            standings[team.name]["avg_points_diff"] = round(standings[team.name]["points_diff"] / (standings[team.name]["home_games"] + standings[team.name]["away_games"]), 1)
            standings[team.name]["percentage"] = round(standings[team.name]["wins"] / (standings[team.name]["wins"] + standings[team.name]["losses"]) * 100, 1)
        
        # Order the standings dictionary by wins
        standings = dict(sorted(standings.items(), key=lambda item: item[1]["wins"], reverse=True))
        
        # Order the standings dictionary including tie breakers
        standings = dict(sorted(standings.items(), key=lambda item: (item[1]["wins"], calculate_tie_breaker(item[1], standings[next(iter(standings))])), reverse=True))
    
    return standings


# Calculate combined totals for a given season
def get_combined_stats(season, team_by_team_stats):
    # Create the combined stats dictionary
    combined_stats = {
        "totals": {
            "gp": 0,
            "pts": 0,
            "reb": 0,
            "ast": 0,
            "stl": 0,
            "blk": 0,
            "fgm": 0,
            "fga": 0,
            "tpm": 0,
            "tpa": 0,
            "ftm": 0,
            "fta": 0,
            "oreb": 0,
            "tov": 0,
            "fouls": 0,
            # Advanced totals
            "gmsc": 0,
        },
        "averages": {
            "ppg": 0,
            "rpg": 0,
            "apg": 0,
            "spg": 0,
            "bpg": 0,
            "fgm": 0,
            "fga": 0,
            "tpm": 0,
            "tpa": 0,
            "ftm": 0,
            "fta": 0,
            "orpg": 0,
            "tpg": 0,
            "fpg": 0,
            # Advanced averages
            "gmsc": 0,
        }
    }
    # Add totals from each team
    for _, team_stats in team_by_team_stats.items():
        combined_stats["totals"]["gp"] += team_stats["totals"].gp
        combined_stats["totals"]["pts"] += team_stats["totals"].pts
        combined_stats["totals"]["reb"] += team_stats["totals"].reb
        combined_stats["totals"]["ast"] += team_stats["totals"].ast
        combined_stats["totals"]["stl"] += team_stats["totals"].stl
        combined_stats["totals"]["blk"] += team_stats["totals"].blk
        combined_stats["totals"]["tov"] += team_stats["totals"].tov
        combined_stats["totals"]["fgm"] += team_stats["totals"].fgm
        combined_stats["totals"]["fga"] += team_stats["totals"].fga
        combined_stats["totals"]["tpm"] += team_stats["totals"].tpm
        combined_stats["totals"]["tpa"] += team_stats["totals"].tpa
        combined_stats["totals"]["ftm"] += team_stats["totals"].ftm
        combined_stats["totals"]["fta"] += team_stats["totals"].fta
        combined_stats["totals"]["oreb"] += team_stats["totals"].oreb
        combined_stats["totals"]["fouls"] += team_stats["totals"].fouls
        # Advanced totals
        combined_stats["totals"]["gmsc"] += (team_stats["averages"].gmsc) * (team_stats["totals"].gp)
    # Add averages based on totals
    if not combined_stats["totals"]["gp"] == 0:
        combined_stats["averages"]["ppg"] = round(combined_stats["totals"]["pts"] / combined_stats["totals"]["gp"], 1)
        combined_stats["averages"]["rpg"] = round(combined_stats["totals"]["reb"] / combined_stats["totals"]["gp"], 1)
        combined_stats["averages"]["apg"] = round(combined_stats["totals"]["ast"] / combined_stats["totals"]["gp"], 1)
        combined_stats["averages"]["spg"] = round(combined_stats["totals"]["stl"] / combined_stats["totals"]["gp"], 1)
        combined_stats["averages"]["bpg"] = round(combined_stats["totals"]["blk"] / combined_stats["totals"]["gp"], 1)
        combined_stats["averages"]["tpg"] = round(combined_stats["totals"]["tov"] / combined_stats["totals"]["gp"], 1)
        combined_stats["averages"]["fgm"] = round(combined_stats["totals"]["fgm"] / combined_stats["totals"]["gp"], 1)
        combined_stats["averages"]["fga"] = round(combined_stats["totals"]["fga"] / combined_stats["totals"]["gp"], 1)
        combined_stats["averages"]["tpm"] = round(combined_stats["totals"]["tpm"] / combined_stats["totals"]["gp"], 1)
        combined_stats["averages"]["tpa"] = round(combined_stats["totals"]["tpa"] / combined_stats["totals"]["gp"], 1)
        combined_stats["averages"]["ftm"] = round(combined_stats["totals"]["ftm"] / combined_stats["totals"]["gp"], 1)
        combined_stats["averages"]["fta"] = round(combined_stats["totals"]["fta"] / combined_stats["totals"]["gp"], 1)
        combined_stats["averages"]["orpg"] = round(combined_stats["totals"]["oreb"] / combined_stats["totals"]["gp"], 1)
        combined_stats["averages"]["fpg"] = round(combined_stats["totals"]["fouls"] / combined_stats["totals"]["gp"], 1)
        # Add advanced averages
        combined_stats["averages"]["gmsc"] = round(combined_stats["totals"]["gmsc"] / combined_stats["totals"]["gp"], 1) 
    # Add percentages
    if combined_stats["totals"]["fga"] == 0:
        combined_stats["averages"]["fgp"] = 0
    else:
        combined_stats["averages"]["fgp"] = round(combined_stats["totals"]["fgm"] / combined_stats["totals"]["fga"] * 100, 1)
    if combined_stats["totals"]["tpa"] == 0:
        combined_stats["averages"]["tpp"] = 0
    else:
        combined_stats["averages"]["tpp"] = round(combined_stats["totals"]["tpm"] / combined_stats["totals"]["tpa"] * 100, 1)
    if combined_stats["totals"]["fta"] == 0:
        combined_stats["averages"]["ftp"] = 0
    else:
        combined_stats["averages"]["ftp"] = round(combined_stats["totals"]["ftm"] / combined_stats["totals"]["fta"] * 100, 1)
    # Return the combined stats dictionary
    return combined_stats