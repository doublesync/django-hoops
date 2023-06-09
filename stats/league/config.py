# Stats Configuration
# ------------------------------------------------
# By: doublesync
# ------------------------------------------------
# This file contains the configuration for the
# stats application.
# ------------------------------------------------

# Settings
# ------------------------------------------------
# These are the settings for the stats application.
# ------------------------------------------------
active_seasons = [2]

#  Statline Validations
# ------------------------------------------------
# These are the validations for the stats application.
# ------------------------------------------------
max_points = 60
max_assists = 30
max_rebounds = 40
max_steals = 10
max_blocks = 10
max_turnovers = 15
max_fouls = 10
max_made = 30
max_attempted = 40

# Game Validations
# ------------------------------------------------
# These are the validations for the stats application.
# ------------------------------------------------
max_team_points = 120

# Stat Choices
# ------------------------------------------------
# These are the choices for the stats application.
# ------------------------------------------------
game_types = [
    ('PRE', 'Preseason'),
    ('REG', 'Regular Season'),
    ('PLY', 'Playoffs'),
    ('FIN', 'Finals'),
]

average_sort_options = [
    'PPG',
    'RPG',
    'APG',
    'SPG',
    'BPG',
    'TPG',
    'FPG',
    'FGP',
    '3PP',
    'FTP',
]

totals_sort_options = [
    'PTS',
    'REB',
    'AST',
    'STL',
    'BLK',
    'TOV',
    'PF',
    'FGM',
    'FGA',
    '3PM',
    '3PA',
    'FTM',
    'FTA',
]

advanced_sort_options = [
    'GMSC',
]

# Find the options
sort_by_options = {
    "averages": average_sort_options, 
    "totals": totals_sort_options, 
    "advanced": advanced_sort_options
}