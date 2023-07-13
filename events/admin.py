# Django imports
from django.contrib import admin
from django.db.models.fields.json import JSONField

# Third party imports
from jsoneditor.forms import JSONEditor

# Model imports
from .models import Event
from .models import Entree

# Override the default JSONField widget with the JSONEditor widget
class MyAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {"widget": JSONEditor},
    }


# Register your models here.
admin.site.register(Event, MyAdmin)
admin.site.register(Entree, MyAdmin)
