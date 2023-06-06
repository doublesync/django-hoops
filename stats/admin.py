# Django imports
from django.contrib import admin

# Model imports
from stats.models import Statline
from stats.models import Game

# Register your models here.
admin.site.register(Statline)
admin.site.register(Game)
