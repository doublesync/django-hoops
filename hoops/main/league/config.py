# Title : League configuration file
# Description : A configuration file for the league.

# Description : League configuration variables
# Description : Attribute, badge & upgrade configuration
start_attribute = 65
start_badge = 0
attribute_cost = 0 
badge_cost = 0

# Description : League configuration variables
# Description : Contract configuration (salary)
# Quick Note : The x * 1000 is just for readability.
contract_salary_min = (10 * 1000) # 100,000
contract_salary_rook = (250 * 1000) # 250,000
contract_salary_max = (100 * 1000) # 1,000,000
# Description : Contract configuration (years/length)
contract_years_min = 1
contract_years_rook = 2
contract_years_max = 3

# Description : League configuration variables
# Description : Currency configuration
primary_currency_name = "cash"
primary_currency_start = 1000
secondary_currency_name = "gems"
secondary_currency_start = 0

# Description : League configuration variables
# Description : Player configuration
player_weight_min = 170
player_weight_max = 300

# Description : League configuration variables
# Description : Initial database field configuration (for new players)
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
    "Passing IQ": start_attribute,
    "Passing Vision": start_attribute,
    "Passing Accuracy": start_attribute,
    "Defensive Rebound": start_attribute,
    "Offensive Rebound": start_attribute,
    "Standing Dunk": start_attribute,
    "Driving Dunk": start_attribute,
    "Shot IQ": start_attribute,
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
initial_features = {}
initial_history = {}
initial_contract = {}
initial_settings = {}
# Description : Initial database field configuration (for new teams)
initial_team_logo = "https://cdn.simplystamps.com/media/catalog/product/5/8/5802-n-a-stock-stamp-hcb.png"

# Description : League configuration variables
# Description : Choice lists (for forms)
height_choices = [("69", "5'9"), ("70", "5'10"), ("71", "5'11"), ("72", "6'0"), ("73", "6'1"), ("74", "6'2"), ("75", "6'3"), ("76", "6'4"), ("77", "6'5"), ("78", "6'6"), ("79", "6'7"), ("80", "6'8"), ("81", "6'9"), ("82", "6'10"), ("83", "6'11"), ("84", "7'0"), ("85", "7'1")]
position_choices = [("PG", "Point Guard"), ("SG", "Shooting Guard"), ("SF", "Small Forward"), ("PF", "Power Forward"), ("C", "Center")]
badge_upgrade_choices = [("Bronze", "Bronze"), ("Silver", "Silver"), ("Gold", "Gold"), ("Hall of Fame", "Hall of Fame")]

# Description : League configuration variables
# Description : Test configuration


# Description : League configuration methods
# Quick Note: Django prefers a callable be used as a default value in a JSONField initialization instead of an instance
def get_default_attributes(): return initial_attributes
def get_default_badges(): return initial_badges
def get_default_features(): return initial_features
def get_default_history(): return initial_history
def get_default_contract(): return initial_contract
def get_default_settings(): return initial_settings