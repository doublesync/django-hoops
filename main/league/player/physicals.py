# Custom imports
from ...league import config as league_config

min_max_heights = league_config.min_max_heights
min_max_weights = league_config.min_max_weights
start_attribute = league_config.start_attribute
position_attributes = league_config.position_starting_attributes


# Finds the correct attribute limits for the player
def setStartingPhysicals(player, mock=False):
    # Find the player details
    if not mock:
        height = int(player.height)
        weight = int(player.weight)
        position = player.primary_position
    else:
        height = player["height"]
        weight = player["weight"]
        position = player["primary_position"]
    # Find height & weight multipliers
    minimum_height = min_max_heights[position]["min"]
    minimum_weight = min_max_weights[position]["min"]
    height_mult = height - minimum_height
    weight_mult = round((weight - minimum_weight) / 2)
    # Calculate the player's physicals
    speed_start = position_attributes[position]["Speed"]
    vertical_start = position_attributes[position]["Vertical"]
    strength_start = position_attributes[position]["Strength"]
    acceleration_start = position_attributes[position]["Acceleration"]
    # Update the player's physicals
    if not mock:
        player.attributes["Speed"] = speed_start - (int(3 * height_mult))
        player.attributes["Speed With Ball"] = speed_start - (int(3 * height_mult))
        player.attributes["Vertical"] = vertical_start - int(height_mult)
        player.attributes["Strength"] = strength_start + int(weight_mult)
        player.attributes["Acceleration"] = acceleration_start - int(weight_mult)
        player.attributes["Lateral Quickness"] = player.attributes["Acceleration"]
    else:
        player["attributes"]["Speed"] = speed_start - (int(3 * height_mult))
        player["attributes"]["Speed With Ball"] = speed_start - (int(3 * height_mult))
        player["attributes"]["Vertical"] = vertical_start - int(height_mult)
        player["attributes"]["Strength"] = strength_start + int(weight_mult)
        player["attributes"]["Acceleration"] = acceleration_start - int(weight_mult)
        player["attributes"]["Lateral Quickness"] = player["attributes"]["Acceleration"]
    # Return the updated player
    return player
