from ...models import Player
from ...models import HistoryList

from ...league import config as league_config
from ...league.player import physicals as league_physicals

max_players = league_config.max_players
min_max_heights = league_config.min_max_heights
min_max_weights = league_config.min_max_weights

position_attributes = league_config.position_starting_attributes
trait_unlocks = league_config.trait_badge_unlocks
archetype_bonuses = league_config.archetype_attribute_bonuses
primary_bonus = league_config.archetype_primary_bonus
secondary_bonus = league_config.archetype_secondary_bonus


def playerCount(user):
    return Player.objects.filter(discord_user=user).count()


def validatePlayerCreation(user, formData):
    # Check if the user has reached the max number of players
    if playerCount(user) >= max_players:
        return [False, "❌ You have reached the max number of players."]
    # Check if the user is trying to make a player with a height or weight that is not allowed (primary position)
    if (int(formData["height"])) < (
        min_max_heights[formData["primary_position"]]["min"]
    ):
        return [False, "❌ You are trying to make a player under the minimum height."]
    if (int(formData["height"])) > (
        min_max_heights[formData["primary_position"]]["max"]
    ):
        return [False, "❌ You are trying to make a player over the maximum height."]
    if (int(formData["weight"])) < (
        min_max_weights[formData["primary_position"]]["min"]
    ):
        return [False, "❌ You are trying to make a player under the minimum weight."]
    if (int(formData["weight"])) > (
        min_max_weights[formData["primary_position"]]["max"]
    ):
        return [False, "❌ You are trying to make a player over the maximum weight."]
    # Check if the user is trying to make a player with a height or weight that is not allowed (secondary position)
    if (int(formData["height"])) < (
        min_max_heights[formData["secondary_position"]]["min"]
    ):
        return [False, "❌ You are trying to make a player under the minimum height."]
    if (int(formData["height"])) > (
        min_max_heights[formData["secondary_position"]]["max"]
    ):
        return [False, "❌ You are trying to make a player over the maximum height."]
    if (int(formData["weight"])) < (
        min_max_weights[formData["secondary_position"]]["min"]
    ):
        return [False, "❌ You are trying to make a player under the minimum weight."]
    if (int(formData["weight"])) > (
        min_max_weights[formData["secondary_position"]]["max"]
    ):
        return [False, "❌ You are trying to make a player over the maximum weight."]
    # Check if the user is trying to make a player with duplicate traits
    selected_traits = [
        formData["trait_one"],
        formData["trait_two"],
    ]
    if len(selected_traits) != len(set(selected_traits)):
        return [False, "❌ You are trying to make a player with duplicate traits."]
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
        cyberface=formData["cyberface"],
        weight=formData["weight"],
        height=formData["height"],
        primary_position=formData["primary_position"],
        secondary_position=formData["secondary_position"],
        jersey_number=formData["jersey_number"],
        # Relationships
        discord_user=user,
        history_list=historyList,
    )
    # Update the player's archetypes & traits
    newPlayer.primary_archetype = formData["primary_archetype"]
    newPlayer.secondary_archetype = formData["secondary_archetype"]
    newPlayer.trait_one = formData["trait_one"]
    newPlayer.trait_two = formData["trait_two"]
    # Update the player's starting attributes
    for attribute in newPlayer.attributes:
        new_attributes = position_attributes[newPlayer.primary_position]
        newPlayer.attributes[attribute] = new_attributes[attribute]
    # Update the player's bonus attributes
    for attribute in archetype_bonuses[newPlayer.primary_archetype]:
        newPlayer.attributes[attribute] += primary_bonus
    for attribute in archetype_bonuses[newPlayer.secondary_archetype]:
        newPlayer.attributes[attribute] += secondary_bonus
    # Update the player's starting physicals
    updatedPlayer = league_physicals.setStartingPhysicals(newPlayer)
    # Save the player
    historyList.save()
    updatedPlayer.save()
    # Return the player
    return updatedPlayer
