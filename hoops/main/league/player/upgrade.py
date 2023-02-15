from ...models import Player
from ...league import config as league_config

import datetime

def formatFormData(player, cleanedFormData):
    # Format the cleaned form data (so it works with the database)
    formatFormData = cleanedFormData.copy()
    formatFormData = {k.title(): v for k, v in formatFormData.items()} 
    formatFormData = {k.replace("_", " "): v for k, v in formatFormData.items()}
    upgradeData = {"attributes": {}, "badges": {}}
    # Filter out values that are under minimum, over maximum or equal to current value
    for k, v in formatFormData.items():
        if (k in player.attributes):
            # Initialize the values
            currentValue = player.attributes[k]
            minimumValue = league_config.min_attribute
            maximumValue = league_config.max_attribute
            # Cases
            if (int(v) <= minimumValue): # Upgrade value is less than minimum value
                continue
            if (int(v) > maximumValue): # Upgrade value is greater than maximum value
                continue
            if (int(v) <= currentValue): # Upgrade value is less/equal to current value
                continue
            # Add the value to the upgrade data
            upgradeCost = league_config.attribute_prices["Default"] * (int(v) - currentValue) # Probably subject to change.
            upgradeData["attributes"][k] = {"cost": upgradeCost, "old": currentValue, "new": int(v)}
        if (k in player.badges):
            # Initialize the values
            currentValue = player.badges[k]
            minimumValue = league_config.min_badge
            maximumValue = league_config.max_badge
            # Cases
            if (int(v) <= minimumValue): # Upgrade value is less than minimum value
                continue
            if (int(v) > maximumValue): # Upgrade value is greater than maximum value
                continue
            if (int(v) <= currentValue): # Upgrade value is less/equal to current value
                continue
            # Add the value to the upgrade data
            upgradeCost = league_config.badge_prices[int(v)]
            upgradeData["badges"][k] = {"cost": upgradeCost, "old": currentValue, "new": int(v)}
    # Return the upgrade data
    return upgradeData

def createUpgrade(player, cleanedFormData):
    # Format the form data
    upgradeData = formatFormData(player, cleanedFormData)
    # Initialize the total cost
    totalCost = 0
    # Calculate the total cost
    for k, v in upgradeData["attributes"].items(): 
        if not (v["new"] > league_config.max_attribute) and not (v["new"] < league_config.min_attribute):
            currentValue = player.attributes[k]
            futureValue = v["new"]
            totalCost += (futureValue - currentValue) * league_config.attribute_prices["Default"] # Probably subject to change.
    for k, v in upgradeData["badges"].items():
            if not (v["new"] > league_config.max_badge) and not (v["new"] < league_config.min_badge):
                totalCost += league_config.badge_prices[v["new"]]
    # Return if cost is below zero
    if totalCost <= 0:
        return "Nothing was upgraded!"
    # Check if the player has enough cash
    if (player.cash >= totalCost):
        # Subtract the cost from the player's cash
        player.cash -= totalCost
        # Add the upgrades to the player
        for k, v in upgradeData["attributes"].items():
            player.attributes[k] = v["new"]
        for k, v in upgradeData["badges"].items():
                player.badges[k] = v["new"]
        # Add the totalCost to spent & add history list log
        currentTime = datetime.datetime.now()
        timestamp = currentTime.strftime("%Y-%m-%d %H:%M:%S")
        player.spent += totalCost
        player.history_list.history["upgrade_logs"].append({
            "cost": totalCost,
            "data": upgradeData,
            "timestamp": timestamp,
        })
        # Save the player
        player.save()
        player.history_list.save()
        # Return success message
        return f"Validated successfully! (${totalCost})"
    else:
        # Return error message
        return "Not enough cash!"