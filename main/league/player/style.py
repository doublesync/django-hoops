import copy
import json

# Path to the data
data_path = 'main/league/looyh/player.json'

# Load the data
file = open(data_path)
data = json.load(file)

# Define each category
vitals = data["VITALS"]
gear = data["SHOES/GEAR"]
accessories = data["ACCESSORIES"]
signature = data["SIGNATURE"]

# Define the categories list
categories = {
    "VITALS": {"template_index": 0, "data": vitals}, 
    "SHOES/GEAR": {"template_index": 5, "data": gear}, 
    "ACCESSORIES": {"template_index": 6, "data": accessories}, 
    "SIGNATURE": {"template_index": 7, "data": signature}
}

# Allowing the user to change the data
equippables = {}
classes = {}

# Iterate through each category (this is vital to make sure the class list includes all classes)
for name, category in categories.items():
    # Iterating through each key and adding to equippables (dict) or classes (list)
    for key in category["data"]:
        # Check if the key even has an info section
        if ("info" not in key):
            continue
        # If the key is not a class (it's something that can be equipped)
        if (key["type"] != "class"):
            # Point towards relative class, or self if there is no relative class
            relative_class = key["info"]["class"] if "class" in key["info"] else key["name"]
            equippables[key["name"]] = {"relative_class": relative_class, "category": category["data"]}
        else:
        # If the key is a class (a list of options for things that can be equipped)
            classes[key["name"]] = key

# Function that finds the dictionary entry that has 'name' of 'name' parameter
def find_entry(category, name):
    for entry in category:
        # Check if the entry is a string
        if (type(entry) == str):
            continue
        # Check if the entry matches the name parameter
        if (entry["name"].lower() == name.lower()):
            return entry
    return None

# Function that finds the options for a specific class
def find_class_options(class_):
    if (class_ in classes):
        # Check if the class has options
        if ("options" in classes[class_]["info"]):
            return classes[class_]["info"]["options"]
        else:
            raise Warning(f"{class_} does not have options")

# A function that should help with usage on the hoopsim website
def compile_options():
    option_list = {}
    for name, info in equippables.items():
        # Define some information
        class_category = info["category"][0]
        # Check what type of equippable is being iterated through
        if info["relative_class"] == name:
            class_ = find_entry(info["category"], info["relative_class"])
            class_options = class_["info"]["options"]
        else:
            class_ = classes[info["relative_class"]]
            class_options = class_["info"]["options"]
        # Add the class options to the option list
        option_list[name] = {"category": class_category, "options": class_options}
    # Convert the option list to a dictionary of tuples (for Django)
    for name, info in option_list.items():
        info["options"] = [(option["value"], option["name"]) for option in info["options"]]
        info["options"].insert(0, ("Vacant", "Vacant"))
        info["options"].insert(1, ("Remove", "Remove"))
    # Return the 'option_list' dictionary
    return option_list

# A function that validtes style changes
def validate_styles(player, form_data):
    # Add the styles to the player
    for field, value in form_data.items():
        if (value == "Vacant"):
            continue
        elif (value == "Remove"):
            if field in player.styles:
                del player.styles[field]
        else:
            field_category = equippables[field]["category"]
            player.styles[field] = {"category": field_category[0], "value": str(value)} 
    # Save the player
    player.save()
    # Return success message
    return [True, "✅ Styles successfully updated!"]

# write_file = open("main/league/looyh/styles.json", "w")
# write_file.write(json.dumps(compile_options(), indent=4))

# # Take user input
# template = [
#     {
#         "module": "PLAYER",
#         "tab": "VITALS",
#         "data": {},
#     },
#     {
#         "module": "PLAYER",
#         "tab": "SHOES/GEAR",
#         "data": {},
#     },
#     {
#         "module": "PLAYER",
#         "tab": "ACCESSORIES",
#         "data": {},
#     },
#     {
#         "module": "PLAYER",
#         "tab": "SIGNATURE",
#         "data": {},
#     },
# ]

# # Print category choices
# print("Categories:")
# for name, info in categories.items():
#     print("-", name)
# user_category = categories[input("\nEnter a category:\n")]

# # Iterate through each equippable in the users chosen category and ask for user input
# for item, info in equippables.items():
#     # Check if the equippable is in the users chosen category
#     if (info["category"] == user_category["data"]):
#         # Define some information
#         class_ = info["relative_class"]
#         category = info["category"]
#         # If the class is itself, then we must use 'find_entry'
#         # If the class is not itself, then we must use 'classes'
#         if (class_ == item):
#             class_item = find_entry(category, class_)
#         else:
#             class_item = classes[class_]
#         # Check if the class has options
#         if ("options" in class_item["info"]):
#             # Find the class options
#             options = class_item["info"]["options"]
#             # Print the class options for the user to choose from
#             print(f"\n{class_} options:")
#             for option in options:
#                 print(f"({option['value']}) {option['name']}")
#         # Ask for user input
#         user_value = input(f"\nEnter a value for {item}:\n")
#         # Allow user to exit this process
#         if (user_value != "exit"):
#             template_index = user_category["template_index"]
#             template[template_index]["data"][item] = (user_value)
#         else:
#             break

# # Print the test file the user made by entering values for equippables
# print(json.dumps(template, indent=4))