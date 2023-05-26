import copy

from ..player import export as hoops_player_export

game_friendly = lambda a: (a - 25) * 3
user_friendly = lambda a: (a / 3) + 25

convert_to_height = lambda x: str(int(x // 12)) + "'" + str(int(x % 12))
convert_to_age = lambda x: str(2023 - x)


def format_years_played(years_played):
    format_age = hoops_player_export.format_age[0]
    birth_year = format_age[int(years_played)]
    return convert_to_age(int(birth_year))


def format_dict_for_django_forms(dictionary):
    dictionary = copy.deepcopy(dictionary)
    step_1 = {k.lower(): v for k, v in dictionary.items()}
    step_2 = {k.replace(" ", "_"): v for k, v in step_1.items()}
    return step_2


def format_list_for_django_forms(list):
    list = copy.deepcopy(list)
    step_1 = [x.lower() for x in list]
    step_2 = [x.replace(" ", "_") for x in step_1]
    return step_2


def format_dict_for_game(dictionary):
    dictionary = copy.deepcopy(dictionary)
    step_1 = {k.upper(): v for k, v in dictionary.items()}
    step_2 = {k.replace(" ", "_"): v for k, v in step_1.items()}
    return step_2
