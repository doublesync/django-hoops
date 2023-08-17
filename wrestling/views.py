from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'wrestling/index.html')

# Wrestler views
def wrestler_create(request):
    return render(request, 'wrestling/wrestler_create.html')

def wrestler_profile(request, wrestler_id):
    return render(request, 'wrestling/wrestler_profile.html')

def wrestler_upgrade(request, wrestler_id):
    return render(request, 'wrestling/wrestler_upgrade.html')

# Roster views
def wrestling_roster(request):
    return render(request, 'wrestling/wrestling_roster.html')

# Titles views
def wrestling_titles(request):
    return render(request, 'wrestling/wrestling_titles.html')

def wrestling_title_history(request, title_id):
    return render(request, 'wrestling/wrestling_title_history.html')

# Shows views
def wrestling_shows(request):
    return render(request, 'wrestling/wrestling_shows.html')

# HTMX views
