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
                    continue
                elif attribute in secondary_attributes:
                    total_price += tier["secondary"]
                else:
                    total_price += tier["base"]
    # Return the upgrade cost
    return total_price


def badgeCost(player, badge, currentValue, futureValue):
    # Define some league config variables
    total_price = 0
    badge_prices = league_config.badge_prices
    trait_badge_unlocks = league_config.trait_badge_unlocks
    # Define some player variables
    trait_one_badges = trait_badge_unlocks[player.trait_one]
    trait_two_badges = trait_badge_unlocks[player.trait_two]
    # Check the badge tier (Bronze, Silver, Gold, Hof)
    for i in range((currentValue + 1), (futureValue + 1)):
        for index, tier in badge_prices.items():
            if i == index:
                if badge in trait_one_badges:
                    total_price += tier["trait_one"]
                    continue
                elif badge in trait_two_badges:
                    total_price += tier["trait_two"]
                    continue
                else:
                    total_price += tier["base"]
    # Return the upgrade cost
    return total_price


def formatAndValidate(player, cleanedFormData):
    # Format the cleaned form data (so it works with the database)
    formatFormData = cleanedFormData.copy()
    formatFormData = {k.title(): v for k, v in formatFormData.items()}
    formatFormData = {k.replace("_", " "): v for k, v in formatFormData.items()}
    # Initialize the upgrade data (will be returned to upgrade the player with)
    # Basically, we'll just be adding the values that were changed and are valid to this dictionary
    upgradeData = {"attributes": {}, "badges": {}}
    error = ""
    # Define some player variables
    trait_badge_unlocks = league_config.trait_badge_unlocks
    trait_one_badges = trait_badge_unlocks[player.trait_one]
    trait_two_badges = trait_badge_unlocks[player.trait_two]
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
            if v < minimumValue:  # Upgrade value is less than minimum value
                error = f"❌ {k} ({v}) value is less than the minimum value."
                break
            if v > maximumValue:  # Upgrade value is greater than maximum value
                error = f"❌ {k} ({v}) value is greater than the maximum value."
                break
            if v < currentValue:  # Upgrade value is less/equal to current value
                error = f"❌ {k} ({v}) value is less than the current value."
                break
            if v == currentValue:
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
            # Finding the maximum value for the badges
            if k in trait_one_badges:
                maximumValue = league_config.trait_one_max
            elif k in trait_two_badges:
                maximumValue = league_config.trait_two_max
            else:
                maximumValue = league_config.trait_none_max
            # Initialize the values
            currentValue = player.badges[k]
            minimumValue = league_config.min_badge
            # Cases
            if v < minimumValue:  # Upgrade value is less than minimum value
                error = f"❌ {k} ({v}) is less than the minimum value."
                break
            if v > maximumValue:  # Upgrade value is greater than maximum value
                error = f"❌ {k} ({v}) is greater than the maximum value."
                break
            if v < currentValue:  # Upgrade value is less/equal to current value
                error = f"❌ {k} ({v}) is less to the current value."
                break
            if v == currentValue:
                continue
            # Add the value to the upgrade data
            upgradeCost = badgeCost(player, k, currentValue, v)
            upgradeData["badges"][k] = {
                "cost": upgradeCost,
                "old": currentValue,
                "new": v,
            }
    # Return the upgrade data
    return [upgradeData, error]


def createUpgrade(player, cleanedFormData):
    # Format the form data
    formatResponse = formatAndValidate(player, cleanedFormData)
    print(formatResponse)
    upgradeData = formatResponse[0]
    upgradeError = formatResponse[1]
    # Check if there were any errors
    if upgradeError != "":
        return upgradeError
    # Initialize the total cost
    totalCost = 0
    # Calculate the total cost
    for k, v in upgradeData["attributes"].items():
        totalCost += v["cost"]
    for k, v in upgradeData["badges"].items():
        totalCost += v["cost"]
    # Return if cost is below zero, or player doesn't have enough cash
    if totalCost <= 0:
        return "😕 Nothing to upgrade!"
    if player.cash < totalCost:
        return "❌ You don't have enough cash for this upgrade!"
    # Check if the player has enough cash
    if player.cash >= totalCost:
        # Subtract the cost from the player's cash
        player.cash -= totalCost
        # Add the upgrades to the player
        for k, v in upgradeData["attributes"].items():
            # Check if the attribute is a physical attribute
            if k in league_config.attribute_categories["physical"]:
                return f"❌ '{k}' cannot be upgraded because it's a physical."
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
