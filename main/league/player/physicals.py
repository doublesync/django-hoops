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
        player.attributes["Lateral Quickness"] = player.attributes["Speed"]
    else:
        player["attributes"]["Speed"] = speed_start - (int(3 * height_mult))
        player["attributes"]["Speed With Ball"] = speed_start - (int(3 * height_mult))
        player["attributes"]["Vertical"] = vertical_start - int(height_mult)
        player["attributes"]["Strength"] = strength_start + int(weight_mult)
        player["attributes"]["Acceleration"] = acceleration_start - int(weight_mult)
        player["attributes"]["Lateral Quickness"] = player["attributes"]["Speed"]
    # Return the updated player
    return player


def updateWeight(player, new_weight):
    # Find the player's minimum & maximum weight
    price_per_pound = league_config.price_per_pound
    price = abs((player.weight - new_weight) * price_per_pound)
    pos_max_weight = min_max_weights[player.primary_position]["max"]
    pos_min_weight = min_max_weights[player.primary_position]["min"]
    # Validate the new weight based on max_weight & min_weight
    if new_weight == player.weight:
        return ["❌ New weight is the same as the current weight.", None]
    # Validate the new weight based on the player's position
    if new_weight > pos_max_weight:
        return [f"❌ New weight is too high.", None]
    if new_weight < pos_min_weight:
        return [f"❌ New weight is too low.", None]
    # Validate the player has enough cash
    if player.cash < price:
        return ["❌ Not enough cash.", None]
    # Change the weight
    player.weight = new_weight
    player.cash -= price
    # Update the player's physicals
    player = setStartingPhysicals(player)
    # Return the updated player
    return [f"✅ Weight change to {new_weight} successful!", player]
