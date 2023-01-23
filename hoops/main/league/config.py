
# Description : League configuration file

start_attribute = 170.0 # 65.0 (has to be 170 for 2KTools)
start_badge = 0

# Description : League configuration methods
# Quick Note: Django prefers a callable be used as a default value in a JSONField instead of an instance

def get_default_attributes():
    return {
        "fake_attribute0": start_attribute,
    }

def get_default_badges():
    return {
        "fake_badge0": start_badge,
    }

def get_default_permits():
    return {
        "fake_permit0": True,
    }