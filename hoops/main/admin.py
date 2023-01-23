from django.contrib import admin
from .models import DiscordUser
from .models import Player
from .models import FeatureList

# Register your models here.
admin.site.register(DiscordUser)
admin.site.register(Player)
admin.site.register(FeatureList)