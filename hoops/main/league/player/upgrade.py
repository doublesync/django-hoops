from ...models import Player
from ...league import config as league_config

def formatFormData(player, cleanedFormData):
    # Format the cleaned form data (so it works with the database)
    formatFormData = cleanedFormData.copy()
    formatFormData = {k.title(): v for k, v in formatFormData.items()} 
    formatFormData = {k.replace("_", " "): v for k, v in formatFormData.items()}
    upgradeData = {}
    # Filter out values that are under minimum, over maximum or equal to current value
    for k, v in formatFormData.items():
        if (k in player.attributes):
            # Initialize the values
            currentValue = player.attributes[k]
            minimumValue = league_config.min_attribute
            maximumValue = league_config.max_attribute
            # Cases
            if (int(v) <= minimumValue):
                continue
            if (int(v) > maximumValue):
                continue
            if (int(v) == currentValue):
                continue
            if (int(v) < currentValue):
                continue
            # Add the value to the upgrade data
            upgradeData[k] = int(v)
        if (k in player.badges):
            # Initialize the values
            currentValue = player.badges[k]
            minimumValue = league_config.min_badge
            maximumValue = league_config.max_badge
            # Cases
            if (int(v) <= minimumValue):
                continue
            if (int(v) > maximumValue):
                continue
            if (int(v) == currentValue):
                continue
            if (int(v) < currentValue):
                continue
            # Add the value to the upgrade data
            upgradeData[k] = int(v)
    # Return the upgrade data
    return upgradeData

def createUpgrade(player, cleanedFormData):
    # Format the form data
    upgradeData = formatFormData(player, cleanedFormData)
    print(upgradeData)
    # Initialize the total cost
    totalCost = 0
    # Calculate the total cost
    for k, v in upgradeData.items():
        if (k in player.attributes):
            if not (v > league_config.max_attribute) and not (v < league_config.min_attribute):
                currentValue = player.attributes[k]
                futureValue = v
                totalCost += (futureValue - currentValue) * league_config.attribute_prices["Default"] # Probably subject to change.
        elif (k in player.badges):
            if not (v > league_config.max_badge) and not (v < league_config.min_badge):
                totalCost += league_config.badge_prices[v]
    # Check if the player has enough cash
    if (player.cash >= totalCost):
        # Subtract the cost from the player's cash
        player.cash -= totalCost
        # Add the upgrades to the player
        for k, v in upgradeData.items():
            if (k in player.attributes):
                player.attributes[k] = v
            elif (k in player.badges):
                player.badges[k] = v
        # Add the totalCost to the history list spent
        player.spent += totalCost
        # Save the player
        player.save()
        # Return success message
        return f"Validated successfully! (${totalCost})"
    else:
        # Return error message
        return "Not enough cash!"