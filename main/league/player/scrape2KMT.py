# Custom imports
import requests
from bs4 import BeautifulSoup

# Main imports
from ...league import config as league_config

# Format tendency names to match 2KMT
format_tendencies = {
    # Defense tendencies
    "Pass Interception": "PASS_INTERCEPTION_TENDENCY",
    "Take Charge": "TAKE_CHARGE_TENDENCY",
    "Contest Shot": "CONTEST_SHOT_TENDENCY",
    "Foul": "FOUL_TENDENCY",
    "Hard Foul": "HARD_FOUL_TENDENCY",
    # Inside tendencies
    "Standing Dunk": "STANDING_DUNK_TENDENCY",
    "Driving Dunk": "DRIVING_DUNK_TENDENCY",
    "Flashy Dunk": "FLASHY_DUNK_TENDENCY",
    "Alley Oop": "ALLEY-OOP_TENDENCY",
    "Putback Dunk": "PUTBACK_TENDENCY",
    "Crash": "CRASH_TENDENCY",
    "Driving Layup": "DRIVING_LAYUP_TENDENCY",
    "Spin Layup": "SPIN_LAYUP_TENDENCY",
    "Hop Step Layup": "HOP_STEP_LAYUP_TENDENCY",
    "Euro Step Layup": "EURO_STEP_LAYUP_TENDENCY",
    "Floater": "FLOATER_TENDENCY",
    # Iso tendencies
    "Triple Threat Pump Fake": "TRIPLE_THREAT_PUMP_FAKE_TENDENCY",
    "Triple Threat Jab Step": "TRIPLE_THREAT_JAB_STEP_TENDENCY",
    "Triple Threat Idle": "TRIPLE_THREAT_IDLE_TENDENCY",
    "Triple Threat Shoot": "TRIPLE_THREAT_SHOOT_TENDENCY",
    "Setup With Sizeup": "SETUP_WITH_SIZEUP_TENDENCY",
    "Setup With Hesitation": "SETUP_WITH_HESITATION_TENDENCY",
    "No Setup Dribble": "NO_SETUP_DRIBBLE_TENDENCY",
    # Shooting tendencies
    "Step Through Shot": "STEP_THROUGH_SHOT_TENDENCY",
    "Shot Under Basket": "SHOT_UNDER_BASKET_TENDENCY",
    "Shot Close": "SHOT_CLOSE_TENDENCY",
    "Shot Close Middle": "SHOT_CLOSE_MIDDLE_TENDENCY",
    "Shot Close Left": "SHOT_CLOSE_LEFT_TENDENCY",
    "Shot Close Right": "SHOT_CLOSE_RIGHT_TENDENCY",
    "Shot Mid": "SHOT_MID-RANGE_TENDENCY",
    "Spot Up Shot Mid": "SPOT_UP_SHOT_MID-RANGE_TENDENCY",
    "Off Screen Shot Mid": "OFF_SCREEN_SHOT_MID-RANGE_TENDENCY",
    "Shot 3Pt": "SHOT_THREE_TENDENCY",
    "Spot Up Shot 3Pt": "SPOT_UP_SHOT_THREE_TENDENCY",
    "Off Screen Shot 3Pt": "OFF_SCREEN_SHOT_THREE_TENDENCY",
    "Stepback Jumper 3Pt": "STEPBACK_JUMPER_THREE_TENDENCY",
    "Stepback Jumper Mid": "STEPBACK_JUMPER_MID-RANGE_TENDENCY",
    "Contested Jumper Mid": "CONTESTED_JUMPER_MID-RANGE_TENDENCY",
    "Contested Jumper 3Pt": "CONTESTED_JUMPER_THREE_TENDENCY",
    "Spin Jumper": "SPIN_JUMPER_TENDENCY",
    "Transition Pull Up 3Pt": "TRANSITION_PULL_UP_THREE_TENDENCY",
    "Drive Pull Up 3pt": "DRIVE_PULL_UP_THREE_TENDENCY",
    "Drive Pull Up Mid": "DRIVE_PULL_UP_MID-RANGE_TENDENCY",
    "Use Glass": "USE_GLASS_TENDENCY",
    "Crash": "CRASH_TENDENCY",
    "Spot Up Shot Mid": "SPOT_UP_SHOT_MID-RANGE_TENDENCY",
    # Post tendencies
    "Post Up": "POST_UP_TENDENCY",
    "Post Shimmy Shot": "POST_SHIMMY_SHOT_TENDENCY",
    "Post Face Up": "POST_FACE_UP_TENDENCY",
    "Post Back Down": "POST_BACK_DOWN_TENDENCY",
    "Post Aggressive Backdown": "POST_AGGRESSIVE_BACKDOWN_TENDENCY",
    "Shoot From Post": "SHOOT_FROM_POST_TENDENCY",
    "Post Hook Left": "POST_HOOK_LEFT_TENDENCY",
    "Post Hook Right": "POST_HOOK_RIGHT_TENDENCY",
    "Post Fade Left": "POST_FADE_LEFT_TENDENCY",
    "Post Fade Right": "POST_FADE_RIGHT_TENDENCY",
    "Post Hop Shot": "POST_HOP_SHOT_TENDENCY",
    "Post Step Back Shot": "POST_STEP_BACK_SHOT_TENDENCY",
    "Post Drive": "POST_DRIVE_TENDENCY",
    "Post Spin": "POST_SPIN_TENDENCY",
    "Post Drop Step": "POST_DROP_STEP_TENDENCY",
    "Post Hop Step": "POST_HOP_STEP_TENDENCY",
    "Post Up And Under": "POST_UP_AND_UNDER_TENDENCY",
    # Freelance tendencies
    "Shoot": "SHOT_TENDENCY",
    "Roll Vs. Pop": "ROLL_VS._POP_TENDENCY",
    "Transition Spot Up": "TRANSITION_SPOT_UP_TENDENCY",
    "Iso Vs. Elite Defender": "ISO_VS._ELITE_DEFENDER_TENDENCY",
    "Iso Vs. Good Defender": "ISO_VS._GOOD_DEFENDER_TENDENCY",
    "Iso Vs. Average Defender": "ISO_VS._AVERAGE_DEFENDER_TENDENCY",
    "Iso Vs. Poor Defender": "ISO_VS._POOR_DEFENDER_TENDENCY",
    "Play Discipline": "PLAY_DISCIPLINE_TENDENCY",
    # Passing tendencies
    "Dish To Open Man": "DISH_TO_OPEN_MAN_TENDENCY",
    "Flashy Pass": "FLASHY_PASS_TENDENCY",
    "Alley-Oop": "ALLEY-OOP_PASS_TENDENCY",
    # Drive tendencies
    "Drive": "DRIVE_TENDENCY",
    "Spot Up Drive": "SPOT_UP_DRIVE_TENDENCY",
    "Off Screen Drive": "OFF_SCREEN_DRIVE_TENDENCY",
    "Drive Right": "DRIVE_RIGHT_TENDENCY",
    "Driving Crossover": "DRIVE_CROSSOVER_TENDENCY",
    "Driving Spin": "DRIVE_SPIN_TENDENCY",
    "Driving Step Back": "DRIVING_STEP_BACK_TENDENCY",
    "Driving Half Spin": "DRIVING_HALF_SPIN_TENDENCY",
    "Driving Double Crossover": "DRIVING_DOUBLE_CROSSOVER_TENDENCY",
    "Driving Behind The Back": "DRIVING_BEHIND_THE_BACK_TENDENCY",
    "Driving Dribble Hesitation": "DRIVING_DRIBBLE_HESITATION_TENDENCY",
    "Driving In And Out": "DRIVING_IN_AND_OUT_TENDENCY",
    "No Driving Dribble Move": "NO_DRIVING_DRIBBLE_MOVE_TENDENCY",
    "Attack Strong On Drive": "ATTACK_STRONG_ON_DRIVE_TENDENCY",
}

# Check if the URL given is valid
def check_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False

# Fetch tendencies from 2KMT and return as a dictionary
def scrape(url):
    # Check if the URL is valid
    if not check_url(url):
        return None
    # Try to scrape the tendencies
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        tendency_list = soup.select_one("#tendencies")
        tendencies = tendency_list.select(".attribute")
        tendency_dict = {}
        for tendency in tendencies:
            scrape_player_name = soup.find('h1').text.strip()
            tendency_value = tendency.find('span').text.strip()
            tendency_name = tendency.contents[-1].strip().title()
            if tendency_name in format_tendencies:
                tendency_dict[format_tendencies.get(tendency_name)] = tendency_value
        # Check for missing tendencies
        for tendency, _ in league_config.initial_tendencies.items():
            if tendency not in tendency_dict:
                tendency_dict[tendency] = 25
        # Return the tendency information
        return [scrape_player_name, tendency_dict]
    except:
        return None