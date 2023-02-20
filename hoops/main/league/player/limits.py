# Custom imports
from ...models import HeightLimit
from ...models import WeightLimit

# Finds the correct attribute limits for the player
def getPlayerLimits(player):
    # Get the possible height & weight limits
    height_limit_list = HeightLimit.objects.filter(enabled=True)
    weight_limit_list = WeightLimit.objects.filter(enabled=True)
    # Set the current height & weight limits to None
    current_height_limits = None
    current_weight_limits = None
    # Figure out which height limit to use for this player
    for option in height_limit_list:
        option_height = option.height
        if player.height == option_height:
            current_height_limits = option
            break
    # Figure out which weight limit to use for this player
    for option in weight_limit_list:
        weight_range = range(option.range1, option.range2)
        if player.weight in weight_range:
            current_weight_limits = option
            break
    # If we found a height limit, set the player's attributes based on it
    if current_height_limits != None:
        # Change the player's height limits (relationship)
        player.height_limits = current_height_limits
        # Calculate & change the player's attributes based on height (height sets the base limits)
        for name in current_height_limits.limits:
            player.attributes[name] = current_height_limits.limits[name]
    else:
        current_height_limits = []
    # If we found a weight limit, set the player's attributes based on it
    if current_weight_limits != None:
        # Change the player's weight limits (relationship)
        player.weight_limits = current_weight_limits
        # Calculate & change the player's attributes based on weight (weight adds a bonus to the height's base limits)
        for name in current_weight_limits.limits:
            player.attributes[name] += current_weight_limits.limits[name]
    else:
        current_weight_limits = []
    # Return the player
    return [player, current_height_limits, current_weight_limits]

# Validates the physical attributes included in the upgradeData
def validatePhysicals(player, upgradeData):
    # Get the possible height & weight limits
    player_limits = getPlayerLimits(player)
    height_limits = player_limits[1]
    weight_limits = player_limits[2]
    # Validate the upgradeData against the player's limits
    for k, v in upgradeData["attributes"].items():
        newValue = v["new"]
        if (k in height_limits.limits) or (k in weight_limits.limits):
            maximum = height_limits.limits[k] + weight_limits.limits[k]
            if newValue > maximum:
                return [False, "❌ The attribute '" + k + "' cannot be upgraded past " + str(maximum) + "."]
    # If we made it this far, everything is good
    return [True, None]