# Title : League configuration file
# Description : A configuration file for the league.

max_players = 100
primary_currency_start = 1000

start_attribute = 65
start_badge = 0
min_attribute = 0
max_attribute = 99
min_badge = 0
max_badge = 4
oak_start_attribute = 65
syp_start_attribute = 65
attribute_prices = {"Default": 10}
badge_prices = {0: 0, 1: 10, 2: 25, 3: 50, 4: 75}

contract_salary_min = 25
contract_salary_rook = 50
contract_salary_max = 100
contract_years_min = 1
contract_years_rook = 2
contract_years_max = 3

player_weight_min = 150
player_weight_max = 270

# Descriptions: For height & weight limits

min_max_heights = {
    "PG": {"min": 72, "max": 76},
    "SG": {"min": 74, "max": 78},
    "SF": {"min": 76, "max": 80},
    "PF": {"min": 78, "max": 82},
    "C": {"min": 80, "max": 84}
}

min_max_weights = {
    "PG": {"min": 150, "max": 250},
    "SG": {"min": 155, "max": 255},
    "SF": {"min": 160, "max": 260},
    "PF": {"min": 165, "max": 265},
    "C": {"min": 170, "max": 270}
}

# Description: Initials for models

initial_attributes = {
    "Driving Layup": start_attribute,
    "Post Fadeaway": start_attribute,
    "Post Hook": start_attribute,
    "Post Control": start_attribute,
    "Draw Foul": start_attribute,
    "Shot Close": start_attribute,
    "Mid Range Shot": start_attribute,
    "Three Point Shot": start_attribute,
    "Free Throw": start_attribute,
    "Ball Control": start_attribute,
    "Passing Iq": start_attribute,
    "Passing Vision": start_attribute,
    "Passing Accuracy": start_attribute,
    "Defensive Rebound": start_attribute,
    "Offensive Rebound": start_attribute,
    "Standing Dunk": start_attribute,
    "Driving Dunk": start_attribute,
    "Shot Iq": start_attribute,
    "Hands": start_attribute,
    "Interior Defense": start_attribute,
    "Perimeter Defense": start_attribute,
    "Block": start_attribute,
    "Steal": start_attribute,
    "Shot Contest": start_attribute,
    "Lateral Quickness": start_attribute,
    "Speed": start_attribute,
    "Speed With Ball": start_attribute,
    "Acceleration": start_attribute,
    "Vertical": start_attribute,
    "Strength": start_attribute,
}
initial_badges = {
    "Acrobat": start_badge,
    "Aerial Wizard": start_badge,
    "Backdown Punisher": start_badge,
    "Bully": start_badge,
    "Dream Shake": start_badge,
    "Drop Stepper": start_badge,
    "Fast Twitch": start_badge,
    "Fearless Finisher": start_badge,
    "Giant Slayer": start_badge,
    "Limitless Takeoff": start_badge,
    "Masher": start_badge,
    "Post Spin Technician": start_badge,
    "Posterizer": start_badge,
    "Pro Touch": start_badge,
    "Rise Up": start_badge,
    "Slithery": start_badge,
    "Agent Threes": start_badge,
    "Amped": start_badge,
    "Blinders": start_badge,
    "Catch And Shoot": start_badge,
    "Claymore": start_badge,
    "Corner Specialist": start_badge,
    "Deadeye": start_badge,
    "Green Machine": start_badge,
    "Guard Up": start_badge,
    "Limitless Range": start_badge,
    "Middy Magician": start_badge,
    "Slippery Off Ball": start_badge,
    "Space Creator": start_badge,
    "Volume Shooter": start_badge,
    "Ankle Breaker": start_badge,
    "Bail Out": start_badge,
    "Break Starter": start_badge,
    "Clamp Breaker": start_badge,
    "Killer Combos": start_badge,
    "Dimer": start_badge,
    "Floor General": start_badge,
    "Handles For Days": start_badge,
    "Hyperdrive": start_badge,
    "Mismatch Expert": start_badge,
    "Needle Threader": start_badge,
    "Post Playmaker": start_badge,
    "Quick First Step": start_badge,
    "Special Delivery": start_badge,
    "Unpluckable": start_badge,
    "Vice Grip": start_badge,
    "Anchor": start_badge,
    "Ankle Braces": start_badge,
    "Challenger": start_badge,
    "Chase Down Artist": start_badge,
    "Clamps": start_badge,
    "Glove": start_badge,
    "Interceptor": start_badge,
    "Menace": start_badge,
    "Off Ball Pest": start_badge,
    "Pick Dodger": start_badge,
    "Post Lockdown": start_badge,
    "Pogo Stick": start_badge,
    "Work Horse": start_badge,
    "Brick Wall": start_badge,
    "Boxout Beast": start_badge,
    "Rebound Chaser": start_badge,
}
initial_history = {
    "upgrade_logs": [],
    "contract_logs": [],
    "trade_logs": [],
}
initial_settings = {
    "test": False,
}
initial_limits = {
    "Speed": start_attribute,
    "Speed With Ball": start_attribute,
    "Acceleration": start_attribute,
    "Vertical": start_attribute,
    "Strength": start_attribute,
}
initial_hotzones = {
    "Left Corner Three": False,
    "Left Wing Three": False,
    "Middle Three": False,
    "Right Wing Three": False,
    "Right Corner Three": False,
    "Left Corner Midrange": False,
    "Left Wing Midrange": False,
    "Middle Midrange": False,
    "Right Wing Midrange": False,
    "Right Corner Midrange": False,
    "Inside Left": False,
    "Inside Middle": False,
    "Inside Right": False,
    "Inside Center": False,
}
initial_team_logo = "https://cdn.simplystamps.com/media/catalog/product/5/8/5802-n-a-stock-stamp-hcb.png"

# Description: Choices & labels for player forms

height_choices = [
    (72, "6'0"),
    (73, "6'1"),
    (74, "6'2"),
    (75, "6'3"),
    (76, "6'4"),
    (77, "6'5"),
    (78, "6'6"),
    (79, "6'7"),
    (80, "6'8"),
    (81, "6'9"),
    (82, "6'10"),
    (83, "6'11"),
    (84, "7'0")
]
position_choices = [
    ("PG", "Point Guard"),
    ("SG", "Shooting Guard"),
    ("SF", "Small Forward"),
    ("PF", "Power Forward"),
    ("C", "Center"),
]
badge_upgrade_choices = [
    (0, "Current"),
    (1, "Bronze"),
    (2, "Silver"),
    (3, "Gold"),
    (4, "Hall of Fame"),
]

attribute_categories = {
    "finishing": [
        "Driving Layup",
        "Post Control",
        "Draw Foul",
        "Shot Close",
        "Standing Dunk",
        "Driving Dunk",
    ],
    "shooting": [
        "Post Fadeaway",
        "Post Hook",
        "Mid Range Shot",
        "Three Point Shot",
        "Free Throw",
        "Shot Iq",
    ],
    "defense": [
        "Defensive Rebound",
        "Offensive Rebound",
        "Interior Defense",
        "Perimeter Defense",
        "Block",
        "Steal",
        "Shot Contest",
        "Lateral Quickness",
    ],
    "playmaking": [
        "Hands",
        "Ball Control",
        "Passing Iq",
        "Passing Vision",
        "Passing Accuracy",
    ],
    "physical": [
        "Speed",
        "Acceleration",
        "Vertical",
        "Strength",
        "Speed With Ball",
    ],
}
badge_categories = {
    "finishing": [
        "Acrobat",
        "Aerial Wizard",
        "Backdown Punisher",
        "Bully",
        "Dream Shake",
        "Drop Stepper",
        "Fast Twitch",
        "Fearless Finisher",
        "Giant Slayer",
        "Limitless Takeoff",
        "Masher",
        "Post Spin Technician",
        "Posterizer",
        "Pro Touch",
        "Rise Up",
        "Slithery",
    ],
    "shooting": [
        "Agent 3",
        "Amped",
        "Blinders",
        "Catch and Shoot",
        "Claymore",
        "Corner Specialist",
        "Deadeye",
        "Green Machine",
        "Guard Up",
        "Limitless Range",
        "Middy Magician",
        "Slippery Off Ball",
        "Space Creator",
        "Volume Shooter",
    ],
    "defense": [
        "Anchor",
        "Ankle Braces",
        "Challenger",
        "Chase Down Artist",
        "Clamps",
        "Glove",
        "Interceptor",
        "Menace",
        "Off Ball Pest",
        "Pick Dodger",
        "Post Lockdown",
        "Pogo Stick",
        "Work Horse",
        "Brick Wall",
        "Boxout Beast",
        "Rebound Chaser",
    ],
    "playmaking": [
        "Ankle Breaker",
        "Bail Out",
        "Break Starter",
        "Clamp Breaker",
        "Killer Combos",
        "Dimer",
        "Floor General",
        "Handles for Days",
        "Hyperdrive",
        "Mismatch Expert",
        "Needle Threader",
        "Post Playmaker",
        "Quick First Step",
        "Special Delivery",
        "Unpluckable",
        "Vice Grip",
    ],
}

# Description: Initials methods for models

def get_default_attributes():
    return initial_attributes


def get_default_badges():
    return initial_badges


def get_default_history():
    return initial_history


def get_default_settings():
    return initial_settings


def get_default_limits():
    return initial_limits


def get_default_hotzones():
    return initial_hotzones