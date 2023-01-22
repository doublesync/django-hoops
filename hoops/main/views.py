from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required

import os
import json

from dotenv import load_dotenv
load_dotenv()

import main.discord.auth as discord_auth

# Create your views here.
@login_required(login_url="/login/discord/")
def home(request):
    return HttpResponse("Hello, world. You're at the main index.")

def login(request):
    return HttpResponse("Hello, world. This is the login page.")

def login_discord(request):
    discord_auth_url = os.environ.get("DISCORD_AUTH_URL")
    return redirect(discord_auth_url)

def login_discord_redirect(request):
    code = request.GET.get('code')
    user = discord_auth.exchange_code(code)
    discord_user = authenticate(request, user=user)
    discord_user = list(discord_user).pop()
    django_login(request, discord_user, backend="main.authorize.DiscordBackend")
    return redirect(home)

@login_required(login_url="/login/discord/")
def logout(request):
    django_logout(request)
    return redirect("/login/discord/")