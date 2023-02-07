from django import forms
from .league import config as league_config

class PlayerForm(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=16)
    last_name = forms.CharField(label="Last Name", max_length=16)
    height = forms.ChoiceField(label="Height", choices=league_config.height_choices)
    weight = forms.IntegerField(label="Weight", min_value=league_config.player_weight_min, max_value=league_config.player_weight_max)
    primary_position = forms.ChoiceField(label="Primary Position", choices=league_config.position_choices)
    secondary_position = forms.ChoiceField(label="Secondary Position", choices=league_config.position_choices)
    jersey_number = forms.IntegerField(label="Jersey Number", min_value=0, max_value=99)

class UpgradeForm(forms.Form):
    # Attributes
    driving_layup = forms.IntegerField(label="Driving Layup", min_value=league_config.start_attribute, max_value=99)
    post_fadeaway = forms.IntegerField(label="Post Fadeaway", min_value=league_config.start_attribute, max_value=99)
    post_hook = forms.IntegerField(label="Post Hook", min_value=league_config.start_attribute, max_value=99)
    post_control = forms.IntegerField(label="Post Control", min_value=league_config.start_attribute, max_value=99)
    draw_foul = forms.IntegerField(label="Draw Foul", min_value=league_config.start_attribute, max_value=99)
    shot_close = forms.IntegerField(label="Shot Close", min_value=league_config.start_attribute, max_value=99)
    mid_range_shot = forms.IntegerField(label="Mid Range Shot", min_value=league_config.start_attribute, max_value=99)
    three_point_shot = forms.IntegerField(label="Three Point Shot", min_value=league_config.start_attribute, max_value=99)
    free_throw = forms.IntegerField(label="Free Throw", min_value=league_config.start_attribute, max_value=99)
    ball_control = forms.IntegerField(label="Ball Control", min_value=league_config.start_attribute, max_value=99)
    passing_iq = forms.IntegerField(label="Passing IQ", min_value=league_config.start_attribute, max_value=99)
    passing_vision = forms.IntegerField(label="Passing Vision", min_value=league_config.start_attribute, max_value=99)
    passing_accuracy = forms.IntegerField(label="Passing Accuracy", min_value=league_config.start_attribute, max_value=99)
    defensive_rebound = forms.IntegerField(label="Defensive Rebounding", min_value=league_config.start_attribute, max_value=99)
    offensive_rebound = forms.IntegerField(label="Offensive Rebounding", min_value=league_config.start_attribute, max_value=99)
    standing_dunk = forms.IntegerField(label="Standing Dunk", min_value=league_config.start_attribute, max_value=99)
    driving_dunk = forms.IntegerField(label="Driving Dunk", min_value=league_config.start_attribute, max_value=99)
    shot_iq = forms.IntegerField(label="Shot IQ", min_value=league_config.start_attribute, max_value=99)
    hands = forms.IntegerField(label="Hands", min_value=league_config.start_attribute, max_value=99)
    interior_defense = forms.IntegerField(label="Interior Defense", min_value=league_config.start_attribute, max_value=99)
    perimeter_defense = forms.IntegerField(label="Perimeter Defense", min_value=league_config.start_attribute, max_value=99)
    block = forms.IntegerField(label="Block", min_value=league_config.start_attribute, max_value=99)
    steal = forms.IntegerField(label="Steal", min_value=league_config.start_attribute, max_value=99)
    shot_contest = forms.IntegerField(label="Shot Contest", min_value=league_config.start_attribute, max_value=99)
    lateral_quickness = forms.IntegerField(label="Lateral Quickness", min_value=league_config.start_attribute, max_value=99)
    speed = forms.IntegerField(label="Speed", min_value=league_config.start_attribute, max_value=99)
    speed_with_ball = forms.IntegerField(label="Speed With Ball", min_value=league_config.start_attribute, max_value=99)
    acceleration = forms.IntegerField(label="Acceleration", min_value=league_config.start_attribute, max_value=99)
    vertical = forms.IntegerField(label="Vertical", min_value=league_config.start_attribute, max_value=99)
    strength = forms.IntegerField(label="Strength", min_value=league_config.start_attribute, max_value=99)
    # Badges
    acrobat = forms.ChoiceField(label="Acrobat", choices=league_config.badge_upgrade_choices)
    aerial_wizard = forms.ChoiceField(label="Aerial Wizard", choices=league_config.badge_upgrade_choices)
    backdown_punisher = forms.ChoiceField(label="Backdown Punisher", choices=league_config.badge_upgrade_choices)
    bully = forms.ChoiceField(label="Bully", choices=league_config.badge_upgrade_choices)
    dream_shake = forms.ChoiceField(label="Dream Shake", choices=league_config.badge_upgrade_choices)
    drop_stepper = forms.ChoiceField(label="Drop Stepper", choices=league_config.badge_upgrade_choices)
    fast_twitch = forms.ChoiceField(label="Fast Twitch", choices=league_config.badge_upgrade_choices)
    fearless_finisher = forms.ChoiceField(label="Fearless Finisher", choices=league_config.badge_upgrade_choices)
    giant_slayer = forms.ChoiceField(label="Giant Slayer", choices=league_config.badge_upgrade_choices)
    limitless_takeoff = forms.ChoiceField(label="Limitless Takeoff", choices=league_config.badge_upgrade_choices)
    masher = forms.ChoiceField(label="Masher", choices=league_config.badge_upgrade_choices)
    post_spin_technician = forms.ChoiceField(label="Post Spin Technician", choices=league_config.badge_upgrade_choices)
    posterizer = forms.ChoiceField(label="Posterizer", choices=league_config.badge_upgrade_choices)
    pro_touch = forms.ChoiceField(label="Pro Touch", choices=league_config.badge_upgrade_choices)
    rise_up = forms.ChoiceField(label="Rise Up", choices=league_config.badge_upgrade_choices)
    slithery = forms.ChoiceField(label="Slithery", choices=league_config.badge_upgrade_choices)
    agent_threes = forms.ChoiceField(label="Agent 3", choices=league_config.badge_upgrade_choices)
    amped = forms.ChoiceField(label="Amped", choices=league_config.badge_upgrade_choices)
    blinders = forms.ChoiceField(label="Blinders", choices=league_config.badge_upgrade_choices)
    catch_and_shoot = forms.ChoiceField(label="Catch and Shoot", choices=league_config.badge_upgrade_choices)
    claymore = forms.ChoiceField(label="Claymore", choices=league_config.badge_upgrade_choices)
    corner_specialist = forms.ChoiceField(label="Corner Specialist", choices=league_config.badge_upgrade_choices)
    deadeye = forms.ChoiceField(label="Deadeye", choices=league_config.badge_upgrade_choices)
    green_machine = forms.ChoiceField(label="Green Machine", choices=league_config.badge_upgrade_choices)
    guard_up = forms.ChoiceField(label="Guard Up", choices=league_config.badge_upgrade_choices)
    limitless_range = forms.ChoiceField(label="Limitless Range", choices=league_config.badge_upgrade_choices)
    middy_magician = forms.ChoiceField(label="Middy Magician", choices=league_config.badge_upgrade_choices)
    slippery_off_ball = forms.ChoiceField(label="Slippery Off Ball", choices=league_config.badge_upgrade_choices)
    space_creator = forms.ChoiceField(label="Space Creator", choices=league_config.badge_upgrade_choices)
    volume_shooter = forms.ChoiceField(label="Volume Shooter", choices=league_config.badge_upgrade_choices)
    ankle_breaker = forms.ChoiceField(label="Ankle Breaker", choices=league_config.badge_upgrade_choices)
    bail_out = forms.ChoiceField(label="Bail Out", choices=league_config.badge_upgrade_choices)
    break_starter = forms.ChoiceField(label="Break Starter", choices=league_config.badge_upgrade_choices)
    clamp_breaker = forms.ChoiceField(label="Clamp Breaker", choices=league_config.badge_upgrade_choices)
    killer_combos = forms.ChoiceField(label="Killer Combos", choices=league_config.badge_upgrade_choices)
    dimer = forms.ChoiceField(label="Dimer", choices=league_config.badge_upgrade_choices)
    floor_general = forms.ChoiceField(label="Floor General", choices=league_config.badge_upgrade_choices)
    handles_for_days = forms.ChoiceField(label="Handles for Days", choices=league_config.badge_upgrade_choices)
    hyperdrive = forms.ChoiceField(label="Hyperdrive", choices=league_config.badge_upgrade_choices)
    mismatch_expert = forms.ChoiceField(label="Mismatch Creator", choices=league_config.badge_upgrade_choices)
    needle_threader = forms.ChoiceField(label="Needle Threader", choices=league_config.badge_upgrade_choices)
    post_playmaker = forms.ChoiceField(label="Post Playmaker", choices=league_config.badge_upgrade_choices)
    quick_first_step = forms.ChoiceField(label="Quick First Step", choices=league_config.badge_upgrade_choices)
    special_delivery = forms.ChoiceField(label="Special Delivery", choices=league_config.badge_upgrade_choices)
    unpluckable = forms.ChoiceField(label="Unpluckable", choices=league_config.badge_upgrade_choices)
    vice_grip = forms.ChoiceField(label="Vice Grip", choices=league_config.badge_upgrade_choices)
    anchor = forms.ChoiceField(label="Anchor", choices=league_config.badge_upgrade_choices)
    ankle_braces = forms.ChoiceField(label="Ankle Braces", choices=league_config.badge_upgrade_choices)
    challenger = forms.ChoiceField(label="Challenger", choices=league_config.badge_upgrade_choices)
    chase_down_artist = forms.ChoiceField(label="Chase Down Artist", choices=league_config.badge_upgrade_choices)
    clamps = forms.ChoiceField(label="Clamps", choices=league_config.badge_upgrade_choices)
    glove = forms.ChoiceField(label="Glove", choices=league_config.badge_upgrade_choices)
    interceptor = forms.ChoiceField(label="Interceptor", choices=league_config.badge_upgrade_choices)
    menace = forms.ChoiceField(label="Menace", choices=league_config.badge_upgrade_choices)
    off_ball_pest = forms.ChoiceField(label="Off Ball Pest", choices=league_config.badge_upgrade_choices)
    pick_dodger = forms.ChoiceField(label="Pick Dodger", choices=league_config.badge_upgrade_choices)
    post_lockdown = forms.ChoiceField(label="Post Lockdown", choices=league_config.badge_upgrade_choices)
    pogo_stick = forms.ChoiceField(label="Pogo Stick", choices=league_config.badge_upgrade_choices)
    work_horse = forms.ChoiceField(label="Work Horse", choices=league_config.badge_upgrade_choices)
    brick_wall = forms.ChoiceField(label="Brick Wall", choices=league_config.badge_upgrade_choices)
    boxout_beast = forms.ChoiceField(label="Boxout Beast", choices=league_config.badge_upgrade_choices)
    rebound_chaser = forms.ChoiceField(label="Rebound Chaser", choices=league_config.badge_upgrade_choices)