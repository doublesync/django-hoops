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
    game_score = round(PTS + 0.4 * FGM - 0.7 * FGA - 0.4*(FTA - FTM) + 0.7 * ORB + 0.3 * DRB + STL + 0.7 * AST + 0.7 * BLK - 0.4 * PF - TOV, 1)
    # Return the game score
    return game_score