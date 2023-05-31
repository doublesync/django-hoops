from .. import config as league_config

# A function to validate a trade offer
def validate_trade(user_team, other_team, trade_players, hard_cap):
    # Define cap variables
    user_team_cap = 0
    other_team_cap = 0
    # Validate post-trade caps
    for player in user_team.player_set.all():
        if player in trade_players["user_team"]:
            other_team_cap += player.salary
        else:
            user_team_cap += player.salary
    for player in other_team.player_set.all():
        if player in trade_players["other_team"]:
            user_team_cap += player.salary
        else:
            other_team_cap += player.salary
    # Validate post-trade cap
    if user_team_cap > hard_cap or other_team_cap > hard_cap:
        return [False, f"❌ Trade would exceed hard cap. (${hard_cap})"]
    # Validate team plays in main league
    if user_team.plays_in_main_league != other_team.plays_in_main_league:
        return [False, "❌ Teams must play in the same league."]
    # Validate post-trade cap
    return [True, "✅ Trade is valid."]


# A function to find salary cap
def get_total_salary(team):
    # Define cap variables
    cap = 0
    # Validate post-trade caps
    for player in team.player_set.all():
        if not player.is_rookie:
            cap += player.salary
        else:
            cap += league_config.rookie_salary
    # Return cap
    return cap
