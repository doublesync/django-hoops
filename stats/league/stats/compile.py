# Django imports
from django.db.models import Q

# Main imports
from main.models import Player
from main.models import Team
from stats.models import Statline
from stats.models import Game

# Stats imports
from stats.models import Game
from stats.models import SeasonAverage
from stats.models import SeasonTotal
from stats.models import Statline
from stats.league.stats import calculate as stats_calculate
from stats.league.stats import advanced as stats_advanced

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
    season_games = Game.objects.filter(season=season).order_by("-day")
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

# Compile the top performers of a specific day
def top_performers(season):
    # Find days in the season
    days = Game.objects.filter(season=season).values_list("day", flat=True).distinct()
    top_performers_dict = {}
    # Find the top performers for each day
    for day in days:
        # Find the statlines in the day
        day_statlines = Statline.objects.filter(game__day=day)
        # Create the top performers dictionary
        top_performers = []
        # Find the top performers
        for line in day_statlines:
            line_gamescore = stats_advanced.get_game_score(line)
            line_dict = {
                "id": line.player.id,
                "name": f"{line.player.first_name} {line.player.last_name}",
                "pts": line.points,
                "reb": line.rebounds,
                "ast": line.assists,
                "stl": line.steals,
                "blk": line.blocks,
                "tov": line.turnovers,
                "oreb": line.offensive_rebounds,
                "fgm": line.field_goals_made,
                "fga": line.field_goals_attempted,
                "3pm": line.three_pointers_made,
                "3pa": line.three_pointers_attempted,
                "ftm": line.free_throws_made,
                "fta": line.free_throws_attempted,
                "gmsc": line_gamescore,
            }
            if len(top_performers) < 5:
                top_performers.append(line_dict)
            else:
                for index, performer in enumerate(top_performers):
                    if line_gamescore > performer["gmsc"]:
                        top_performers[index] = line_dict
                        break
        # Sort the top performers by gamescore
        top_performers = sorted(top_performers, key=lambda k: k["gmsc"], reverse=True)
        top_performers_dict[day] = top_performers
        # Limit to five top performers
        top_performers_dict[day] = top_performers_dict[day][:5]
    # Return the top performers dictionary
    return top_performers_dict

# Compile one player and it's stats
def player_stats(player, season, playoffs=False, finals=False, career=False):
    # Create the player dictionary
    player_season_stats = {
        "id": player.id,
        "name": f"{player.first_name} {player.last_name}",
        "season": season,
        "teamly_stats": {},
        "yearly_stats": {},
    }
    # Check which game type to use
    if playoffs:
        team_by_team_totals = SeasonTotal.objects.filter(player=player, season=season, game_type="PLY")
        team_by_team_averages = SeasonAverage.objects.filter(player=player, season=season, game_type="PLY")
    elif finals:
        team_by_team_totals = SeasonTotal.objects.filter(player=player, season=season, game_type="FIN")
        team_by_team_averages = SeasonAverage.objects.filter(player=player, season=season, game_type="FIN")
    elif career:
        player_career_stats = career_stats(player)
        return player_career_stats
    else:
        team_by_team_totals = SeasonTotal.objects.filter(player=player, season=season, game_type="REG")
        team_by_team_averages = SeasonAverage.objects.filter(player=player, season=season, game_type="REG")
    # Check if the totals & averages exist
    if not team_by_team_totals or not team_by_team_averages:
        return None
    # Get totals for each specific team
    for tobj in team_by_team_totals:
        # Add the team to the teamly_stats dictionary
        if not tobj.team.abbrev in player_season_stats["teamly_stats"]:
            player_season_stats["teamly_stats"][tobj.team.abbrev] = {}
            player_season_stats["teamly_stats"][tobj.team.abbrev]["totals"] = tobj
        else:
            player_season_stats["teamly_stats"][tobj.team.abbrev]["totals"] = tobj
    # Get averages for each specific team
    for aobj in team_by_team_averages:
        # Add the team to the teamly_stats dictionary
        if not aobj.team.abbrev in player_season_stats["teamly_stats"]:
            player_season_stats["teamly_stats"][aobj.team.abbrev] = {}
            player_season_stats["teamly_stats"][aobj.team.abbrev]["averages"] = aobj
        else:
            player_season_stats["teamly_stats"][aobj.team.abbrev]["averages"] = aobj

    # Combine the averages & totals (add all seasons together)
    player_season_stats["yearly_stats"] = stats_calculate.get_combined_stats(season, player_season_stats["teamly_stats"])

    # Return the player dictionary
    return player_season_stats

# Compile every player's stats
def all_player_stats(season, playoffs=False, finals=False, career=False):
    # Create the players dictionary
    players_stats = {}
    # Find all players
    all_players = Player.objects.all()
    # Add each player to the players dictionary
    for player in all_players:
        response = player_stats(player=player, season=season, playoffs=playoffs, finals=finals, career=career)
        if response:
            players_stats[player.id] = response
    # Return the players dictionary
    return players_stats

# Compile one player's career stats
def career_stats(player):
    # Create the player dictionary
    player_career_stats = {}
    # Find the player's eligible seasons
    seasons = []
    for avg in SeasonAverage.objects.filter(player=player):
        if avg.season not in seasons:
            seasons.append(avg.season)
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
                "GMSC": stats_advanced.get_game_score(line),
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
        gmsc = stats_advanced.get_game_score(line)
        if gotd == None:
            gotd = line
        else:
            gotd_gmsc = stats_advanced.get_game_score(gotd)
            if gmsc > gotd_gmsc:
                gotd = line
    # Return the game of the day
    if gotd:
        return {
            "id": gotd.game.id,
            "pid": gotd.player.id,
            "day": gotd.game.day,
            "abbrev": gotd.team_at_time.abbrev,
            "gamescore": stats_advanced.get_game_score(gotd),
            "player": f"{gotd.player.first_name} {gotd.player.last_name}",
            "gamescore": stats_advanced.get_game_score(gotd),
            "points": gotd.points,
            "rebounds": gotd.rebounds,
            "assists": gotd.assists,
            "steals": gotd.steals,
            "blocks": gotd.blocks,
        }
    else:
        return None