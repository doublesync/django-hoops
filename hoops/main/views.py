from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse

import os
import json

from dotenv import load_dotenv
load_dotenv()

import main.discord.auth as discord_auth

# Create your views here.
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
    return JsonResponse(user)