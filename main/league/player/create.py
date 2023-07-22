from ...models import Player
from ...models import HistoryList

from ...league import config as league_config
from ...league.player import physicals as league_physicals

max_players = league_config.max_players
min_max_heights = league_config.min_max_heights
min_max_weights = league_config.min_max_weights

position_attributes = league_config.position_starting_attributes


def playerCount(user):
    return Player.objects.filter(discord_user=user).count()

def validateAttributesBadges(formData):
    # Check the weights of the primary and secondary attributes & badges
    primary_attributes_spent = 0
    secondary_attributes_spent = 0
    primary_badges_spent = 0
    secondary_badges_spent = 0
    # Add the total spent
    for attribute in formData["primary_attributes"]:
        primary_attributes_spent += league_config.attribute_weights[attribute]
    for attribute in formData["secondary_attributes"]:
        secondary_attributes_spent += league_config.attribute_weights[attribute]
    for badge in formData["primary_badges"]:
        primary_badges_spent += league_config.badge_weights[badge]
    for badge in formData["secondary_badges"]:
        secondary_badges_spent += league_config.badge_weights[badge]
    # Validate the total spent
    if primary_attributes_spent != league_config.max_primary_attributes:
        return [False, "❌ You have spent too many/few points on primary attributes."]
    if secondary_attributes_spent != league_config.max_secondary_attributes:
        return [False, "❌ You have spent too many/few points on secondary attributes."]
    if primary_badges_spent != league_config.max_primary_badges:
        return [False, "❌ You have spent too many/few points on primary badges."]
    if secondary_badges_spent != league_config.max_secondary_badges:
        return [False, "❌ You have spent too many/few points on secondary badges."]
    # Check if the player has duplicate attributes selected
    matching_attributes = set(formData["primary_attributes"]).intersection(formData["secondary_attributes"])
    if matching_attributes:
        return [False, "❌ You have duplicate attributes selected."]
    # Check if the player has duplicate badges selected
    matching_badges = set(formData["primary_badges"]).intersection(formData["secondary_badges"])
    if matching_badges:
        return [False, "❌ You have duplicate badges selected."]
    # If everything is good, return True
    return [True, None]

def validatePlayerCreation(user, formData):
    # Check if the user has reached the max number of players
    if playerCount(user) >= user.player_slots:
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
    # Check if the attributes and badges the user selected are validated
    validation_response = validateAttributesBadges(formData)
    if validation_response[0] == False:
        return validation_response
    # Check if the user is trying to make a player with an existing cyberface
    if Player.objects.filter(cyberface=formData["cyberface"]).exists():
        if int(formData["cyberface"]) != 1:
            return [False, "❌ You are trying to make a player with an existing cyberface."]
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
    # Update the player's attributes & badges
    newPlayer.primary_attributes = formData["primary_attributes"]
    newPlayer.secondary_attributes = formData["secondary_attributes"]
    newPlayer.primary_badges = formData["primary_badges"]
    newPlayer.secondary_badges = formData["secondary_badges"]
    # Update the player's starting attributes
    for attribute in newPlayer.attributes:
        new_attributes = position_attributes[newPlayer.primary_position]
        newPlayer.attributes[attribute] = new_attributes[attribute]
    # Update the player's starting physicals
    updatedPlayer = league_physicals.setStartingPhysicals(newPlayer)
    # Save the player
    historyList.save()
    updatedPlayer.save()
    # Return the player
    return updatedPlayer
