# Django imports
from django.contrib import admin
from django.db.models.fields.json import JSONField

# Third party imports
from jsoneditor.forms import JSONEditor

# Model imports
from .models import Poll
from .models import Choice

# Override the default JSONField widget with the JSONEditor widget
class MyAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {"widget": JSONEditor},
    }


# Register your models here.
admin.site.register(Poll, MyAdmin)
admin.site.register(Choice, MyAdmin)
