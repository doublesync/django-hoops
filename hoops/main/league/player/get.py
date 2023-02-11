from ...models import Player

def fetch(id: int):
    try:
        return Player.objects.get(pk=id)
    except Player.DoesNotExist:
        return False