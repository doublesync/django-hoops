# Django imports
from django.contrib import admin

# Model imports
from .models import DiscordUser
from .models import Player
from .models import FeatureList
from .models import HistoryList
from .models import Team
from .models import Configuration
from .models import Contract
from .models import Season

# Register your models here.
admin.site.register(DiscordUser)
admin.site.register(Player)
admin.site.register(FeatureList)
admin.site.register(HistoryList)
admin.site.register(Team)
admin.site.register(Configuration)
admin.site.register(Contract)
admin.site.register(Season)
