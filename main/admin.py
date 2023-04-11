# Django imports
from django.contrib import admin
from django.db.models.fields.json import JSONField

# Third party imports
from jsoneditor.forms import JSONEditor

# Model imports
from .models import DiscordUser
from .models import Player
from .models import HistoryList
from .models import Team
from .models import Coupon
from .models import Transaction
from .models import TradeOffer


# Override the default JSONField widget with the JSONEditor widget
class MyAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {"widget": JSONEditor},
    }


# Register your models here.
admin.site.register(DiscordUser, MyAdmin)
admin.site.register(Player, MyAdmin)
admin.site.register(HistoryList, MyAdmin)
admin.site.register(Team, MyAdmin)
admin.site.register(Coupon, MyAdmin)
admin.site.register(Transaction, MyAdmin)
admin.site.register(TradeOffer, MyAdmin)
