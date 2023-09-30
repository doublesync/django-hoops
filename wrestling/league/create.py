# Model imports
from ..models import Wrestler
from ..models import Team
from ..models import Show



def validate_creation(form_data):
    # Check if the wrestler is within min/max weights
    # Check if the wrestler is within min/max heights
    pass

def create_wrestler(discord_user, form_data):
    # ❌ Validate the wrestler
    # ❌ Set wrestler attributes based on weightclass & archetype
    # ❌ Give the wrestler attribute points based on:
    #   weightclass, archetype, profession, & age
    new_wrestler = Wrestler(
        # Need to figure out which fields match for each other
        worker_name = form_data["worker_name"],
        twitch_handle = form_data["twitch_handle"],
        division = None,
        gimmick = None,
        brand = None,
        worker_disposition = None,
        size = None,
        gender = form_data["gender"],
        nationality = form_data["nationality"],
        ## overall = default,
        accolades = {},
        # Wrestler attribute fields
        ## total_xp = default,
        attributes = {},
        # Wrestler profile fields
        profession = None,
        wrestler_class = None,
        age = None,
        entrance = form_data["entrance"],
        victory = None,
        music = None,
        story = None,
        # Wrestler image fields
        profile_picture = None,
        payback_one_picture = None,
        payback_two_picture = None,
    )
    # Set the wrestler's starting attributes
    
    # Set the wrestler's bonus attribute points