def validatePhysicals(player, upgradeData):
    # Get the physicals
    effected_attributes = player.physicals.effected_attributes
    effected_badges = player.physicals.effected_badges
    # Validate attributes
    for k, v in upgradeData["attributes"].items():
        if k in effected_attributes:
            # Initialize the values
            upgrade = v["new"]
            maximum = effected_attributes[k]["maximum"]
            minimum = effected_attributes[k]["minimum"]
            # Validate the upgrade
            if upgrade > maximum: return False
            if upgrade < minimum: return False
        else:
            return True
    # Validate badges
    for k, v in upgradeData["badges"].items():
        if k in effected_badges:
            # Initialize the values
            upgrade = v["new"]
            maximum = effected_badges[k]["maximum"]
            minimum = effected_badges[k]["minimum"]
            # Validate the upgrade
            if upgrade > maximum: return False
            if upgrade < minimum: return False
        else:
            return True