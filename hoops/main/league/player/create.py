from ...models import Player
from ...models import HistoryList

from ...league import config as league_config
from ...league.player import physicals as league_physicals

max_players = league_config.max_players
min_max_heights = league_config.min_max_heights
min_max_weights = league_config.min_max_weights

def playerCount(user):
    return Player.objects.filter(discord_user=user).count()


def validatePlayerCreation(user, formData):
    # Check if the user has reached the max number of players
    if playerCount(user) >= max_players:
        return [False, "❌ You have reached the max number of players."]
    if (int(formData["height"])) < (min_max_heights[formData["primary_position"]]["min"]):
        return "❌ You are trying to make a player under the minimum height."
    if (int(formData["height"])) > (min_max_heights[formData["primary_position"]]["max"]):
        return "❌ You are trying to make a player over the maximum height."
    if (int(formData["weight"])) < (min_max_weights[formData["primary_position"]]["min"]):
        return "❌ You are trying to make a player under the minimum weight."
    if (int(formData["weight"])) > (min_max_weights[formData["primary_position"]]["max"]):
        return "❌ You are trying to make a player over the maximum weight."
    # If everything is good, create the player
    return [True, None]


def createPlayer(user, formData):
    # Create the player's relationship objects
    historyList = HistoryList.objects.create()
    # Create the player
    newPlayer = Player.objects.create(
        # Customs
        first_name=formData["first_name"],
        last_name=formData["last_name"],
        weight=formData["weight"],
        height=formData["height"],
        primary_position=formData["primary_position"],
        secondary_position=formData["secondary_position"],
        jersey_number=formData["jersey_number"],
        # Relationships
        discord_user=user,
        history_list=historyList,
    )
    # Update the player's starting physicals
    updatedPlayer = league_physicals.setStartingPhysicals(newPlayer)
    # Save the player
    print("Speed:" + str(updatedPlayer.attributes["Speed"]))
    print("Speed WB:" + str(updatedPlayer.attributes["Speed With Ball"]))
    print("Acceleration:" + str(updatedPlayer.attributes["Acceleration"]))
    print("Vertical:" + str(updatedPlayer.attributes["Vertical"]))
    print("Strength:" + str(updatedPlayer.attributes["Strength"]))
    historyList.save()
    updatedPlayer.save()
    # Return the player
    return updatedPlayer
