# Custom imports
from ...league import config as league_config

min_max_heights = league_config.min_max_heights
min_max_weights = league_config.min_max_weights
start_attribute = league_config.start_attribute

# Finds the correct attribute limits for the player
def setStartingPhysicals(player):
    # Find the player details
    physicals = league_config.attribute_categories["physical"]
    height = int(player.height)
    weight = int(player.weight)
    position = player.primary_position
    # Find height & weight multipliers
    minimum_height = min_max_heights[position]["min"]
    minimum_weight = min_max_weights[position]["min"]
    height_mult = (height - minimum_height)
    weight_mult = ((weight - minimum_weight) / 2)
    # Update the physicals
    player.attributes["Speed"] == start_attribute - (int(3 * height_mult))
    player.attributes["Speed With Ball"] = start_attribute -  (int(3 * height_mult))
    player.attributes["Vertical"] = start_attribute - int(height_mult)
    player.attributes["Strength"] = start_attribute - int(weight_mult)
    player.attributes["Acceleration"] = start_attribute - int(weight_mult)
    # Return the updated player
    return player