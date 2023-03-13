import copy

game_friendly = lambda a: (a - 25) * 3
user_friendly = lambda a: (a / 3) + 25

convert_to_height = lambda x: str(int(x // 12)) + "'" + str(int(x % 12))


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
