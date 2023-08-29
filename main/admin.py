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
from .models import ContractOffer
from .models import Notification
from .models import Award

# Python imports
import requests

# Custom imports
from main.discord import webhooks as discord_webhooks

# Override the default JSONField widget with the JSONEditor widget
class MyAdmin(admin.ModelAdmin):

    formfield_overrides = {
        JSONField: {"widget": JSONEditor},
    }

    # def save_model(self, request, obj, form, change):
    #     # Get the original object from the database
    #     original_obj = self.model.objects.get(pk=obj.pk)

    #     # Compare the fields to find the changes
    #     changed_fields = []
    #     for field in obj._meta.fields:
    #         if getattr(original_obj, field.name) != getattr(obj, field.name):
    #             changed_fields.append(field.name)

    #     # Print the message with the updated fields
    #     changed_fields_str = ""
    #     for field in changed_fields:
    #         changed_fields_str += f"{request.user.username} | {obj} | {field} | {original_obj.__dict__[field]} -> **{obj.__dict__[field]}**\n"

    #     # Prepping a link using the PastebinAPI
    #     api_endpoint = "https://pastebin.com/api/api_post.php"
    #     data = {
    #         # ZW38KqwFTFvgvHUgcWE3cFV41ID-WHUW
    #         # omc_XJIUCPgz1QrHSxK55AaQ5juwJg-p
    #         "api_dev_key": "omc_XJIUCPgz1QrHSxK55AaQ5juwJg-p",
    #         "api_option": "paste",
    #         "api_paste_code": "N/A",
    #         "api_paste_expire_data": "1H",
    #         "api_paste_name": "N/A"
    #     }

    #     # Create a link using the PastebinAPI
    #     data["api_paste_code"] = changed_fields_str
    #     data["api_paste_name"] = "Admin Change Log"
    #     rq = requests.post(url=api_endpoint, data=data)
    #     link = rq.text

    #     # Send the webhook
    #     discord_webhooks.send_webhook(
    #         url="panel_logs",
    #         title="🔎 Panel Log",
    #         message=f"Admin {request.user.username} made changes to the {obj._meta.verbose_name} {obj}. \nChanged fields: \n{changed_fields_str} \n[View Change Log]({link})",
    #     )

    #     # Call the parent class's save_model method to actually save the object
    #     super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(DiscordUser, MyAdmin)
admin.site.register(Player, MyAdmin)
admin.site.register(HistoryList, MyAdmin)
admin.site.register(Team, MyAdmin)
admin.site.register(Coupon, MyAdmin)
admin.site.register(Transaction, MyAdmin)
admin.site.register(TradeOffer, MyAdmin)
admin.site.register(ContractOffer, MyAdmin)
admin.site.register(Notification, MyAdmin)
admin.site.register(Award, MyAdmin)
