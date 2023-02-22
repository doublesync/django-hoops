game_friendly = (lambda a: (a - 25) * 3)
user_friendly = (lambda a: (a / 3) + 25)

convert_to_height = lambda x: str(int(x // 12)) + "'" + str(int(x % 12))
