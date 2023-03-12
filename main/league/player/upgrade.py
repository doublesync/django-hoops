# Custom imports
from ...league import config as league_config

# Python imports
import datetime

# Upgrade methods


def attributeCost(player, attribute, currentValue, futureValue):
    # Define some league config variables
    total_price = 0
    attribute_prices = league_config.attribute_prices
    attribute_bonuses = league_config.archetype_attribute_bonuses
    # Define some player variables
    primary_archetype = player.primary_archetype
    secondary_archetype = player.secondary_archetype
    primary_attributes = attribute_bonuses[primary_archetype]
    secondary_attributes = attribute_bonuses[secondary_archetype]
    # Check the attribute tier (60-70, 71-80)
    for i in range((currentValue + 1), (futureValue + 1)):
        for _, tier in attribute_prices.items():
            if i in tier["range"]:
                if attribute in primary_attributes:
                    total_price += tier["primary"]
                elif attribute in secondary_attributes:
                    total_price += tier["secondary"]
                else:
                    total_price += tier["base"]
    # Return the upgrade cost
    return total_price


def formatFormData(player, cleanedFormData):
    # Format the cleaned form data (so it works with the database)
    formatFormData = cleanedFormData.copy()
    formatFormData = {k.title(): v for k, v in formatFormData.items()}
    formatFormData = {k.replace("_", " "): v for k, v in formatFormData.items()}
    # Initialize the upgrade data (will be returned to upgrade the player with)
    # Basically, we'll just be adding the values that were changed and are valid to this dictionary
    upgradeData = {"attributes": {}, "badges": {}}
    # Filter out values that are under minimum, over maximum or equal to current value
    for k, v in formatFormData.items():
        # Type cast the value to an integer
        v = int(v)
        # If the key is an attribute
        if k in player.attributes:
            # Initialize the values
            currentValue = player.attributes[k]
            minimumValue = league_config.min_attribute
            maximumValue = league_config.max_attribute
            # Cases
            if v <= minimumValue:  # Upgrade value is less than minimum value
                continue
            if v > maximumValue:  # Upgrade value is greater than maximum value
                continue
            if v <= currentValue:  # Upgrade value is less/equal to current value
                continue
            # Add the value to the upgrade data
            upgradeCost = attributeCost(player, k, currentValue, v)
            upgradeData["attributes"][k] = {
                "cost": upgradeCost,
                "old": currentValue,
                "new": v,
            }
        # If the key is a badge
        if k in player.badges:
            # Initialize the values
            currentValue = player.badges[k]
            minimumValue = league_config.min_badge
            maximumValue = league_config.max_badge
            # Cases
            if v <= minimumValue:  # Upgrade value is less than minimum value
                continue
            if v > maximumValue:  # Upgrade value is greater than maximum value
                continue
            if v <= currentValue:  # Upgrade value is less/equal to current value
                continue
            # Add the value to the upgrade data
            upgradeCost = league_config.badge_prices[v]
            upgradeData["badges"][k] = {
                "cost": upgradeCost,
                "old": currentValue,
                "new": v,
            }
    # Return the upgrade data
    return upgradeData


def createUpgrade(player, cleanedFormData):
    # Format the form data
    upgradeData = formatFormData(player, cleanedFormData)
    # Initialize the total cost
    totalCost = 0
    # Calculate the total cost
    for k, v in upgradeData["attributes"].items():
        if not (v["new"] > league_config.max_attribute) and not (
            v["new"] < league_config.min_attribute
        ):
            totalCost += v["cost"]
    for k, v in upgradeData["badges"].items():
        if not (v["new"] > league_config.max_badge) and not (
            v["new"] < league_config.min_badge
        ):
            totalCost += league_config.badge_prices[v["new"]]
    # Return if cost is below zero
    if totalCost <= 0:
        return "😕 Nothing to upgrade!"
    # Check if the player has enough cash
    if player.cash >= totalCost:
        # Subtract the cost from the player's cash
        player.cash -= totalCost
        # Add the upgrades to the player
        for k, v in upgradeData["attributes"].items():
            # Check if the attribute is a physical attribute
            if k in league_config.attribute_categories["physical"]:
                return (
                    f"❌ The attribute '{k}' cannot be upgraded because it's a physical."
                )
            else:
                player.attributes[k] = v["new"]
        for k, v in upgradeData["badges"].items():
            player.badges[k] = v["new"]
        # Add the totalCost to spent & add history list log
        currentTime = datetime.datetime.now()
        timestamp = currentTime.strftime("%Y-%m-%d | %H:%M:%S")
        player.spent += totalCost
        player.history_list.history["upgrade_logs"].append(
            {
                "cost": totalCost,
                "data": upgradeData,
                "timestamp": timestamp,
            }
        )
        # Save the player & history lists
        player.save()
        player.history_list.save()
        # Return success message
        return f"✅ Congrats, you upgraded your player for ${totalCost}!"
    else:
        # Return error message
        return "Not enough cash!"
