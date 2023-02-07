from django.contrib.auth.backends import BaseBackend
from .models import DiscordUser

class DiscordBackend(BaseBackend):
    
    def authenticate(self, request, user):
        find_user = DiscordUser.objects.filter(id=user["id"])
        if len(find_user) == 0:
            # Create new user (w/ custom manager)
            new_user = DiscordUser.objects.create_discord_user(user)
            return new_user
        return find_user
    
    def get_user(self, user_id):
        try:
            return DiscordUser.objects.get(pk=user_id)
        except DiscordUser.DoesNotExist:
            return None