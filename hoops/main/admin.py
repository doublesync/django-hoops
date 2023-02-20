# Django imports
from django.contrib import admin
from django.db.models.fields.json import JSONField

# Third party imports
from jsoneditor.forms import JSONEditor

# Model imports
from .models import DiscordUser
from .models import Player
from .models import FeatureList
from .models import HistoryList
from .models import Team
from .models import Configuration
from .models import Contract
from .models import Season
from .models import HeightLimit
from .models import WeightLimit
from .models import PlayerOffers
from .models import TeamOffers

# Override the default JSONField widget with the JSONEditor widget
class MyAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }

# Register your models here.
admin.site.register(DiscordUser, MyAdmin)
admin.site.register(Player, MyAdmin)
admin.site.register(FeatureList, MyAdmin)
admin.site.register(HistoryList, MyAdmin)
admin.site.register(Team, MyAdmin)
admin.site.register(Configuration, MyAdmin)
admin.site.register(Contract, MyAdmin)
admin.site.register(Season, MyAdmin)
admin.site.register(HeightLimit, MyAdmin)
admin.site.register(WeightLimit, MyAdmin)
admin.site.register(PlayerOffers, MyAdmin)
admin.site.register(TeamOffers, MyAdmin)