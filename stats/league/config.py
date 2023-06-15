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
active_seasons = [1, 2]

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
    "gmsc",
    'ppg',
    'rpg',
    'apg',
    'spg',
    'bpg',
    'tpg',
    "fpg",
    'fgp',
    '3pp',
    'ftp',
]

totals_sort_options = [
    'pts',
    'reb',
    'ast',
    'stl',
    'blk',
    'tov',
    'fouls',
    'fgm',
    'fga',
    '3pm',
    '3pa',
    'ftm',
    'fta',
]

# Find the options
sort_by_options = {
    "averages": average_sort_options, 
    "totals": totals_sort_options, 
}