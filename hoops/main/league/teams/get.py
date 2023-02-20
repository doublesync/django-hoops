from ...models import Team

def fetch(id: int):
    try:
        return Team.objects.get(pk=id)
    except Team.DoesNotExist:
        return False