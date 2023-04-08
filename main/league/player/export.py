from ..extra import convert as extra_converters
import copy

json_template = [
    # NBA2K Modules go here
    {
        "module": "PLAYER",
        "tab": "VITALS",
        "data": {
            "UNIQUESIGNATUREID": "0",
            "SIGNATUREID": "0",
            "AUDIOSIGNATUREID": "0",
            "PHOTOID": "0",
            "HEADSHOTID": "0",
            "MURAL_ID": "0",
            "ACTIONSHOTID": "0",
            "NAMESID": "0",
            "MYTEAM_DUPLICATE_ID": "0",
        },
    },
    {
        "module": "PLAYER",
        "tab": "ATTRIBUTES",
        "data": {},
    },
    {
        "module": "PLAYER",
        "tab": "BADGES",
        "data": {},
    },
    {
        "module": "PLAYER",
        "tab": "HOTZONE",
        "data": {},
    },
    {
        "module": "PLAYER",
        "tab": "TENDENCIES",
        "data": {},
    },
]

mod_tools_attributes = {
    "DRIVING_LAYUP": "0",
    "POST_FADEAWAY": "0",
    "POST_HOOK": "0",
    "POST_CONTROL": "0",
    "DRAW_FOUL": "0",
    "SHOT_CLOSE": "0",
    "MID-RANGE_SHOT": "0",
    "3PT_SHOT": "0",
    "FREE_THROW": "0",
    "BALL_CONTROL": "0",
    "PASSING_IQ": "0",
    "PASSING_ACCURACY": "0",
    "OFFENSIVE_REBOUND": "0",
    "STANDING_DUNK": "0",
    "DRIVING_DUNK": "0",
    "SHOT_IQ": "0",
    "PASSING_VISION": "0",
    "HANDS": "0",
    "DEFENSIVE_REBOUND": "0",
    "INTERIOR_DEFENSE": "0",
    "PERIMETER_DEFENSE": "0",
    "BLOCK": "0",
    "STEAL": "0",
    "SHOT_CONTEST": "0",
    "LATERAL_QUICKNESS": "0",
    "SPEED": "0",
    "SPEED_WITH_BALL": "0",
    "ACCELERATION": "0",
    "VERTICAL": "0",
    "STRENGTH": "0",
    "STAMINA": "0",
    "HUSTLE": "0",
    "PASS_PERCEPTION": "0",
    "DEFENSIVE_CONSISTENCY": "0",
    "HELP_DEFENSIVE_IQ": "0",
    "OFFENSIVE_CONSISTENCY": "0",
    "PICK_AND_ROLL_DEFENSIVE_IQ": "0",
    "INTANGIBLES": "0",
    "POTENTIAL": "0",
}

mod_tools_badges = {
    "ACROBAT": "0",
    "AERIAL_WIZARD": "0",
    "BACKDOWN_PUNISHER": "0",
    "BULLY": "0",
    "DREAM_SHAKE": "0",
    "DROP-STEPPER": "0",
    "FAST_TWITCH": "0",
    "FEARLESS_FINISHER": "0",
    "GIANT_SLAYER": "0",
    "LIMITLESS_TAKEOFF": "0",
    "MASHER": "0",
    "POST_SPIN_TECHNICIAN": "0",
    "POSTERIZER": "0",
    "PRO_TOUCH": "0",
    "RISE_UP": "0",
    "SLITHERY": "0",
    "AGENT_3": "0",
    "AMPED": "0",
    "BLINDERS": "0",
    "CATCH_SHOOT": "0",
    "CLAYMORE": "0",
    "CLUTCH_SHOOTER": "0",
    "COMEBACK_KID": "0",
    "CORNER_SPECIALIST": "0",
    "DEADEYE": "0",
    "GREEN_MACHINE": "0",
    "GUARD_UP": "0",
    "LIMITLESS_RANGE": "0",
    "MIDDY_MAGICIAN": "0",
    "SLIPPERY_OFF-BALL": "0",
    "SPACE_CREATOR": "0",
    "VOLUME_SHOOTER": "0",
    "ANKLE_BREAKER": "0",
    "BAIL_OUT": "0",
    "BREAK_STARTER": "0",
    "CLAMP_BREAKER": "0",
    "KILLER_COMBOS": "0",
    "DIMER": "0",
    "FLOOR_GENERAL": "0",
    "HANDLES_FOR_DAYS": "0",
    "HYPERDRIVE": "0",
    "MISMATCH_EXPERT": "0",
    "NEEDLE_THREADER": "0",
    "POST_PLAYMAKER": "0",
    "QUICK_FIRST_STEP": "0",
    "SPECIAL_DELIVERY": "0",
    "UNPLUCKABLE": "0",
    "VICE_GRIP": "0",
    "ANCHOR": "0",
    "ANKLE_BRACES": "0",
    "CHALLENGER": "0",
    "CHASE_DOWN_ARTIST": "0",
    "CLAMPS": "0",
    "GLOVE": "0",
    "INTERCEPTOR": "0",
    "MENACE": "0",
    "OFF-BALL_PEST": "0",
    "PICK_DODGER": "0",
    "POST_LOCKDOWN": "0",
    "POGO_STICK": "0",
    "WORK_HORSE": "0",
    "BRICK_WALL": "0",
    "BOXOUT_BEAST": "0",
    "REBOUND_CHASER": "0",
}

# Cases that don't follow the standard format, need to be manually formatted
attribute_formatting_cases = {
    "THREE_POINT_SHOT": "3PT_SHOT",
    "MID_RANGE_SHOT": "MID-RANGE_SHOT",
    "HELP_DEFENSE_IQ": "HELP_DEFENSIVE_IQ",
    "POST_MOVES": "POST_CONTROL",
    "CLOSE_SHOT": "SHOT_CLOSE",
    "PICK_ROLL_DEFENSIVE_IQ": "PICK_AND_ROLL_DEFENSIVE_IQ",
}
badge_formatting_cases = {
    "DROP_STEPPER": "DROP-STEPPER",
    "AGENT_THREES": "AGENT_3",
    "CATCH_AND_SHOOT": "CATCH_SHOOT",
    "SLIPPERY_OFF_BALL": "SLIPPERY_OFF-BALL",
    "OFF_BALL_PEST": "OFF-BALL_PEST",
}
# Formats database position to game position
format_position = {"PG": "0", "SG": "1", "SF": "2", "PF": "3", "C": "4"}
format_age = (  # Why the fuck does black force this to be a tuple???
    {
        1: "2003",
        2: "2001",
        3: "1999",
        4: "1997",
        5: "1995",
        6: "1993",
        7: "1991",
        8: "1989",
    },
)


def export_player(player):
    # Gather the player's information
    database_attributes = player.attributes
    database_badges = player.badges
    database_hotzones = player.hotzones
    database_tendencies = player.tendencies
    # Create the player's in game attributes
    game_file = copy.deepcopy(json_template)

    # Set the player's vitals
    def set_vitals():
        game_file[0]["data"]["FIRSTNAME"] = str(player.first_name)
        game_file[0]["data"]["LASTNAME"] = str(player.last_name)
        game_file[0]["data"]["FACEID"] = str(player.cyberface)
        game_file[0]["data"]["HEIGHT_CM"] = str(round(player.height * 2.54, 2))
        game_file[0]["data"]["WEIGHT_LBS"] = str(player.weight)
        game_file[0]["data"]["POSITION"] = format_position[player.primary_position]
        game_file[0]["data"]["SECONDARY_POSITION"] = format_position[
            player.secondary_position
        ]
        game_file[0]["data"]["NUMBER"] = str(player.jersey_number)
        try:
            game_file[0]["data"]["BIRTHYEAR"] = format_age[0][player.years_played]
        except Exception:
            game_file[0]["data"]["BIRTHYEAR"] = "1989"

    # Set the player's attributes
    def set_attributes():
        # First,  format the attributes
        game_file[1]["data"] = extra_converters.format_dict_for_game(
            database_attributes
        )
        # Finally, format the attribute values
        for attribute, value in game_file[1]["data"].items():
            game_file[1]["data"][attribute] = str(extra_converters.game_friendly(value))
        # Format the manual cases
        for case, fix in attribute_formatting_cases.items():
            if case in game_file[1]["data"]:
                val = game_file[1]["data"][case]
                del game_file[1]["data"][case]
                game_file[1]["data"][fix] = val

    # Set the player's badges
    def set_badges():
        # Second, format the badges
        game_file[2]["data"] = extra_converters.format_dict_for_game(database_badges)
        # Finally, format the badge values
        for badge, value in game_file[2]["data"].items():
            game_file[2]["data"][badge] = str(value)
        # Format the manual cases
        for case, fix in badge_formatting_cases.items():
            if case in game_file[2]["data"]:
                val = game_file[2]["data"][case]
                del game_file[2]["data"][case]
                game_file[2]["data"][fix] = val

    # Set the player's hotzones
    def set_hotzones():
        pass  # game_file[3]["data"]

    # Set the player's tendencies
    def set_tendencies():
        # We don't need to format these, they are already formatted
        # We do, however, need to convert the values to strings
        # In other words, if the player is using website/database tendencies
        if not player.use_game_tendencies:
            for tendency, value in database_tendencies.items():
                game_file[4]["data"][tendency] = str(value)

    # Call the sub functions
    set_vitals()
    set_attributes()
    set_badges()
    set_hotzones()
    set_tendencies()
    # Return the player's file
    return game_file
