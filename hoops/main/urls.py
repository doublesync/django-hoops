from django.urls import path
from . import views

urlpatterns = [
    path(route='', view=views.home, name='home'),
    path(route='login/', view=views.login, name='login'),
    path(route="login/discord/", view=views.login_discord, name="login_discord"),
    path(route="login/discord/redirect/", view=views.login_discord_redirect, name="login_discord_redirect")
]
