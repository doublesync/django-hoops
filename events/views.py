# Django imports
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Sum
from django.template.loader import render_to_string
from django.utils import timezone
from django.views import View

# Main application imports
from main.models import Player

# Event application imports
from events.models import Event
from events.models import Entree
from events.forms import EventForm

# Event views
def index(request):
    # Create the context
    context = {
        "events": Event.objects.all(),
    }
    # Return the response
    return render(request, 'events/index.html', context)

def view_event(request, id):
    # Check if the event exists
    if not Event.objects.filter(id=id).exists():
        return HttpResponse("❌ That event does not exist.")
    # Create the context
    context = {
        "event": Event.objects.get(id=id),
        "entrees": Entree.objects.filter(event=id),
        "entree_count": Entree.objects.filter(event=id).count(),
        "player_list": Player.objects.filter(discord_user=request.user),
    }
    # Return the response
    return render(request, 'events/viewing/view_event.html', context)

def create_event(request):
    # Check permissions
    if not request.user.can_edit_events:
        return HttpResponse("❌ You do not have permission to create events.")
    # Create the context
    context = {
        "create_event_form": EventForm,
    }
    # Return the response
    return render(request, 'events/editing/create_event.html', context)

def edit_event(request, id):
    return HttpResponse("Editing event")

# AJAX views
def add_event(request):
    if request.method == "POST":
        # Check permissions
        if not request.user.can_edit_events:
            return HttpResponse("❌ You do not have permission to add events.")
        # Create the event
        title = request.POST.get("title")
        description = request.POST.get("description")
        spent_limit = request.POST.get("spent_limit")
        rookies_allowed = True if request.POST.get("rookies_allowed") else False
        free_agents_allowed = True if request.POST.get("free_agents_allowed") else False
        active_players_allowed = True if request.POST.get("active_players_allowed") else False
        use_spent_limit = True if request.POST.get("use_spent_limit") else False
        # Validate the event
        if not title or not description:
            return HttpResponse("❌ Please enter a title and description.")
        if use_spent_limit and not spent_limit:
            return HttpResponse("❌ Please enter a spent limit if you want to use one.")
        # Create & save the event
        event = Event(
            title=title,
            description=description,
            rookies_allowed=rookies_allowed,
            free_agents_allowed=free_agents_allowed,
            active_players_allowed=active_players_allowed,
            use_spent_limit=use_spent_limit,
            spent_limit=int(spent_limit),
        )
        event.save()
        # Return the success message (refresh page and clear form)
        messages.success(request, f"✅ Event added successfully! [#{event.id}]")
        response = HttpResponse()
        response['HX-Refresh'] = "true"
        return response

def add_entree(request):
    # Get some fields
    event_id = request.POST.get("event_id")
    id = request.POST.get("id")
    # Check for player & event
    if not Player.objects.filter(id=id).exists():
        return HttpResponse("❌ That player does not exist.")
    if not Event.objects.filter(id=event_id).exists():
        return HttpResponse("❌ That event does not exist.")
    # Get player & event
    player = Player.objects.get(id=id)
    event = Event.objects.get(id=event_id)
    # Check if user owns player
    if not player.discord_user == request.user:
        return HttpResponse("❌ You do not own that player.")
    # Check if player is already entered
    if Entree.objects.filter(player=player, event=event).exists():
        return HttpResponse("❌ You have already entered that event.")
    # Check if event is full
    if Entree.objects.filter(event=event).count() >= event.max_entrees:
        return HttpResponse("❌ That event is full.")
    # Find player eligibility statuses
    is_rookie = False
    is_free_agent = False
    is_active_player = False
    if player.years_played <= 1:
        is_rookie = True
    if player.current_team == None:
        is_free_agent = True
    if player.current_team and player.current_team.plays_in_main_league:
        is_active_player = True
    # Check if player is eligible
    if not event.rookies_allowed and is_rookie:
        return HttpResponse("❌ That event does not allow rookies.")
    if not event.free_agents_allowed and is_free_agent:
        return HttpResponse("❌ That event does not allow free agents.")
    if not event.active_players_allowed and is_active_player:
        return HttpResponse("❌ That event does not allow active players.")        
    # Add the entree
    entree = Entree(
        player=player,
        event=event,
    )
    entree.save()
    # Return the success message (refresh page and clear form)
    return HttpResponse("✅ Player added to event successfully!")

def remove_entree(request):
    return HttpResponse("Leaving event")