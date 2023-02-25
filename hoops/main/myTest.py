from .models import Player
from .league.player import refresh

def run():
    player = Player.objects.get(pk=2)
    updatedPlayer = refresh.updateContract(player)
    if updatedPlayer: 
        updatedPlayer.save()
    else:
        print("Player is not eligible for a contract update.")