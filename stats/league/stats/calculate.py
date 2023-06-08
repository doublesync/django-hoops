# Django imports
from django.db.models import Q

# Custom imports
from stats.models import Game
from stats.models import Statline
from main.models import Player
from main.models import Team


# Custom imports
import json

# Calculates the games behind for each team
def get_games_behind(standings):
    for team in standings:
        # Find the team's wins
        team_wins = standings[team]["wins"]
        # Find the team's losses
        team_losses = standings[team]["losses"]
        # Find the team's games behind
        games_behind = 0
        # Find the team's games behind
        for team2 in standings:
            # Skip the team itself
            if team2 == team:
                continue
            # Find the team's wins
            team2_wins = standings[team2]["wins"]
            # Find the team's losses
            team2_losses = standings[team2]["losses"]
            # Find the team's games behind
            games_behind = games_behind + (team2_wins - team_wins) + (team_losses - team2_losses)
        # Add the games behind to the standings dictionary (first check if it's negative or not)
        if games_behind > 0:
            standings[team]["games_behind"] = games_behind
        else:
            # Check if the team has played any games
            standings[team]["games_behind"] = 0
    # Return the standings dictionary
    return standings

# Calculates the standings for a given season
def get_standings(season):
    # Create the standings dictionary
    standings = {}
    all_teams = Team.objects.all()
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
            standings[team.name]["avg_points_for"] = standings[team.name]["points_for"] / (standings[team.name]["home_games"] + standings[team.name]["away_games"])
            standings[team.name]["avg_points_against"] = standings[team.name]["points_against"] / (standings[team.name]["home_games"] + standings[team.name]["away_games"])
            standings[team.name]["avg_points_diff"] = standings[team.name]["points_diff"] / (standings[team.name]["home_games"] + standings[team.name]["away_games"])
            standings[team.name]["percentage"] = round(standings[team.name]["wins"] / (standings[team.name]["wins"] + standings[team.name]["losses"]), 2)
        # Order the standings dictionary by wins
        standings = dict(sorted(standings.items(), key=lambda item: item[1]["wins"], reverse=True))
        # Calculate games behind for each team
        standings = get_games_behind(standings)

    # Return the standings dictionary
    return standings

# Calculates the game score for a given game
def get_game_score(line):
    # Game score formula: PTS + 0.4 * FGM - 0.7 * FGA - 0.4*(FTA - FTM) + 0.7 * ORB + 0.3 * DRB + STL + 0.7 * AST + 0.7 * BLK - 0.4 * PF - TOV
    PTS = line.points
    REB = line.rebounds
    AST = line.assists
    STL = line.steals
    BLK = line.blocks
    TOV = line.turnovers
    FGM = line.field_goals_made
    FGA = line.field_goals_attempted
    FTM = line.free_throws_made
    FTA = line.free_throws_attempted
    ORB = line.offensive_rebounds
    DRB = line.defensive_rebounds
    PF = line.personal_fouls
    # Calculate the game score
    game_score = PTS + 0.4 * FGM - 0.7 * FGA - 0.4*(FTA - FTM) + 0.7 * ORB + 0.3 * DRB + STL + 0.7 * AST + 0.7 * BLK - 0.4 * PF - TOV
    # Return the game score
    return game_score