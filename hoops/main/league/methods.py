# Python imports
from dataclasses import dataclass

# Model imports
from ..models import DiscordUser
from ..models import Player
from ..models import FeatureList
from ..models import HistoryList
from ..models import Team

# .ENV file import
import os, json
from dotenv import load_dotenv
load_dotenv()

# Helper methods
convert_stat_game_friendly = (lambda a: (a - 25) * 3)
convert_stat_user_friendly = (lambda a: (a / 3) + 25)

# Player methods
def get_player(id: int):
    try:
        return Player.objects.get(pk=id)
    except Player.DoesNotExist:
        return False