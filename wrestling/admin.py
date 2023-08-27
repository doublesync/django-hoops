# Django imports
from django.contrib import admin
from django.db.models.fields.json import JSONField

# Third party imports
from jsoneditor.forms import JSONEditor

# Model imports
from .models import Team
from .models import Wrestler
from .models import Show

# Override the default JSONField widget with the JSONEditor widget
class MyAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {"widget": JSONEditor},
    }


# Register your models here.
admin.site.register(Team, MyAdmin)
admin.site.register(Wrestler, MyAdmin)
admin.site.register(Show, MyAdmin)