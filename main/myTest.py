from .models import Player
from .league.player import upgrade


def main():
    p = Player.objects.get(pk=1)
    c = upgrade.attributeCost(p, "Driving Layup", 60, 99)

    print("Total Cost:" + str(c))


if __name__ == "__main__":
    main()
