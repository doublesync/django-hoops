from .models import Player
from .league.player import upgrade
from .league import config as league_config


def time_to_max(position, reach_value):

    contract = 75
    jobs = 200
    daily = contract + jobs
    weekly = daily * 7

    total_cost = 0
    primary_cost = 0
    secondary_cost = 0
    base_cost = 0

    plr = Player.objects.get(pk=2)
    plr.secondary_archetype = "Slasher"

    primary_attributes = league_config.archetype_attribute_bonuses[
        plr.primary_archetype
    ]
    secondary_attributes = league_config.archetype_attribute_bonuses[
        plr.secondary_archetype
    ]

    # All attributes
    for attribute, start_value in plr.attributes.items():

        # Skip physical attributes
        if attribute in league_config.attribute_categories["physical"]:
            continue

        # Total Cost
        cost = upgrade.attributeCost(plr, attribute, start_value, reach_value)
        total_cost += cost

        if attribute in primary_attributes:
            primary_cost += cost

        if attribute in secondary_attributes:
            secondary_cost += cost

        if (not attribute in primary_attributes) and (
            not attribute in secondary_attributes
        ):
            base_cost += cost

    # Position
    print("\n")
    print("Position: " + position)
    print("\n")

    # Total Cost
    print("Total Cost: " + str(total_cost))
    print("Time to Max (days): " + str(round(total_cost / daily)) + " days")
    print("Time to Max (weeks): " + str(round(total_cost / weekly, 2)) + " weeks")
    print("\n")

    # Primary Cost
    print("Primary Cost: " + str(primary_cost))
    print("Time to Max (days): " + str(round(primary_cost / daily)) + " days")
    print("Time to Max (weeks): " + str(round(primary_cost / weekly, 2)) + " weeks")
    print("\n")

    # Secondary Cost
    print("Secondary Cost: " + str(secondary_cost))
    print("Time to Max (days): " + str(round(secondary_cost / daily)) + " days")
    print("Time to Max (weeks): " + str(round(secondary_cost / weekly, 2)) + " weeks")
    print("\n")


def check_for_typos(position):

    position_starting_attributes = league_config.position_starting_attributes
    initial_attributes = league_config.initial_attributes

    for attribute, _ in initial_attributes.items():
        if not attribute in position_starting_attributes[position]:
            print(f"{attribute} is not in {position} starting attributes")

    for _, attrs in position_starting_attributes.items():
        for attribute, _ in attrs.items():
            if not attribute in initial_attributes:
                print(f"{position} {attribute} is not in inital attributes")


def badge_upg_test():
    p = Player.objects.get(pk=2)
    upg = upgrade.badgeCost(p, "Blinders", 0, 1)
    print(f"Total Cost: {upg}")
