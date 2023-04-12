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
from django.template.loader import render_to_string
from django.utils import timezone

# Model imports
from .models import Player
from .models import Team
from .models import Coupon
from .models import Transaction
from .models import TradeOffer

# Form imports
from .forms import PlayerForm
from .forms import UpgradeForm

# Custom imports
from .discord import auth as discord_auth
from .discord import webhooks as discord_webhooks
from .league import config as league_config

# Custom packages
import copy
import json
import datetime

from .league.player import upgrade as hoops_player_upgrade
from .league.player import create as hoops_player_create
from .league.player import physicals as hoops_player_physicals
from .league.player import export as hoops_player_export
from .league.extra import convert as hoops_extra_convert
from .league.teams import trade as hoops_team_trade

# .ENV file import
import os, json
from dotenv import load_dotenv

load_dotenv()


# Create your views here.
def home(request):
    current_user = request.user
    context = {
        "title": "Home",
        "current_user": current_user,
        "players": [],
    }
    # Send players to home page
    if current_user.is_authenticated:
        try:
            players = Player.objects.filter(discord_user=current_user)
            for p in players:
                context["players"].append(p)
        except ValueError:
            # If the user is still signed into an administration account
            redirect(logout)
    # Return the home page
    return render(request, "main/league/home.html", context)


def login(request):
    return HttpResponse("This is the login page.")


def login_discord(request):
    discord_auth_url = os.environ.get("DISCORD_AUTH_URL")
    return redirect(discord_auth_url)


def login_discord_redirect(request):
    try:
        # Get information from Discord
        code = request.GET.get("code")
        info = discord_auth.exchange_code(code)
        user = info[0]
        guilds = info[1]
        isInGuild = False
        # Check if the user is in the server
        for guild in guilds:
            if guild["id"] == os.environ.get("HOOPS_GUILD_ID"):
                isInGuild = True
                break
        # If the user is in the discord, create the user on the website
        if isInGuild:
            # Create the discord user
            discord_user = authenticate(request, user=user)
            discord_user = list(discord_user).pop()
            # Finally, log the user in
            django_login(request, discord_user, backend="main.authorize.DiscordBackend")
            # Send a success message
            messages.error(request, "You have successfully logged in!")
        else:
            # If the user isn't in the discord, redirect them to the home page with an error
            messages.error(request, "You aren't in the hoopsim discord server!")
    except:
        # Sometimes the user will be redirected to this page without a code
        messages.error(request, "Something went wrong while logging you in, try again!")
    # Redirect the user to the home page
    return redirect(home)


def logout(request):
    django_logout(request)
    messages.error(request, "You have successfully logged out!")
    return redirect("/")


def player(request, id):
    # Check if the player exists
    plr = Player.objects.get(pk=id)
    if not plr:
        return HttpResponse("Sorry, this player doesn't exist!")
    # Get transaction history & total earnings in past week (cash_taken, cash_given, paycheck)
    transactions = Transaction.objects.filter(player=plr)
    week_earnings = 0
    # If date is in the past week, add/subtract to/from week_earnings
    for t in transactions:
        if t.date > timezone.now() - datetime.timedelta(days=7):
            if t.transaction_type == "cash_taken":
                week_earnings -= t.amount
            elif t.transaction_type == "cash_given":
                week_earnings += t.amount
    # Initialize the context
    context = {
        # Page information
        "title": f"{plr.first_name} {plr.last_name}",
        "player": plr,
        "badgeEmojis": {0: "🚫", 1: "🟫", 2: "🌫️", 3: "🟨", 4: "🟪"},
        # Attribute categories
        "playmaking_attributes": league_config.attribute_categories["playmaking"],
        "shooting_attributes": league_config.attribute_categories["shooting"],
        "physical_attributes": league_config.attribute_categories["physical"],
        "defense_attributes": league_config.attribute_categories["defense"],
        "finishing_attributes": league_config.attribute_categories["finishing"],
        # Badge categories
        "finishing_badges": league_config.badge_categories["finishing"],
        "shooting_badges": league_config.badge_categories["shooting"],
        "playmaking_badges": league_config.badge_categories["playmaking"],
        "defense_badges": league_config.badge_categories["defense"],
        # Playstyles
        "playstyles": league_config.playstyles,
        "playstyle1": [
            league_config.playstyles[plr.statics["playstyles"]["playstyle1"]],
            plr.statics["playstyles"]["playstyle1"],
        ],
        "playstyle2": [
            league_config.playstyles[plr.statics["playstyles"]["playstyle2"]],
            plr.statics["playstyles"]["playstyle2"],
        ],
        "playstyle3": [
            league_config.playstyles[plr.statics["playstyles"]["playstyle3"]],
            plr.statics["playstyles"]["playstyle3"],
        ],
        "playstyle4": [
            league_config.playstyles[plr.statics["playstyles"]["playstyle4"]],
            plr.statics["playstyles"]["playstyle4"],
        ],
        # Precalled methods
        "height_in_feet": hoops_extra_convert.convert_to_height(plr.height),
        "file": json.dumps(hoops_player_export.export_player(plr), indent=4),
        # Transaction history
        "week_earnings": week_earnings,
    }
    return render(request, "main/players/player.html", context)


@login_required(login_url="/login/discord/")
def upgrade_player(request, id):
    # Collect user & player information
    user = request.user
    # Check if the player exists
    player = Player.objects.get(pk=id)
    if not player:
        return HttpResponse("Sorry, this player doesn't exist!")
    # Check if the user has permission to upgrade this player
    if not player.discord_user == user:
        return HttpResponse("Sorry, you don't have permission to upgrade this player!")
    # Combine attributes & badges + convert to Django form format
    prefill_info = dict(player.attributes, **player.badges, **player.tendencies)
    # Convert primary & secondary attributes to Django form format
    js_primary_attributes = league_config.archetype_attribute_bonuses[
        player.primary_archetype
    ]
    js_secondary_attributes = league_config.archetype_attribute_bonuses[
        player.secondary_archetype
    ]
    js_trait_one_badges = league_config.trait_badge_unlocks[player.trait_one]
    js_trait_two_badges = league_config.trait_badge_unlocks[player.trait_two]
    # Have to remove the 'range' function from attribute prices or javascript shits the bed
    js_attribute_prices = copy.deepcopy(league_config.attribute_prices)
    for _, v in js_attribute_prices.items():
        v["range"] = 0
    # Initialize the context
    context = {
        # Context items
        "title": "Upgrade Player",
        "player": player,
        "upgrade_player_form": UpgradeForm(initial=prefill_info),
        # Badges & attributes
        "badge_attributes": prefill_info,
        "badge_prices": league_config.badge_prices,
        "attribute_prices": js_attribute_prices,
        "attribute_bonuses": league_config.archetype_attribute_bonuses,
        "primary_attributes": js_primary_attributes,
        "secondary_attributes": js_secondary_attributes,
        # Traits
        "trait_one_badges": js_trait_one_badges,
        "trait_two_badges": js_trait_two_badges,
        # Attribute categories
        "finishing_attributes": league_config.attribute_categories["finishing"],
        "shooting_attributes": league_config.attribute_categories["shooting"],
        "playmaking_attributes": league_config.attribute_categories["playmaking"],
        "defense_attributes": league_config.attribute_categories["defense"],
        "physical_attributes": league_config.attribute_categories["physical"],
        # Badge categories
        "finishing_badges": league_config.badge_categories["finishing"],
        "shooting_badges": league_config.badge_categories["shooting"],
        "playmaking_badges": league_config.badge_categories["playmaking"],
        "defense_badges": league_config.badge_categories["defense"],
        # Tendency categories
        "initial_tendencies": league_config.initial_tendencies,
    }
    return render(request, "main/players/upgrade.html", context)


@login_required(login_url="/login/discord/")
def create_player(request):
    # Collect user & player information
    user = request.user
    # Process the request (if it's a POST request)
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            response = hoops_player_create.validatePlayerCreation(
                user, form.cleaned_data
            )
            success = response[0]
            status = response[1]
            # If the form is valid, and the player creation succeeded, redirect to the player page
            if success == True:
                playerObject = hoops_player_create.createPlayer(user, form.cleaned_data)
                # Create a discord webhook
                discord_webhooks.send_webhook(
                    url="creation",
                    title="Player Creation",
                    message=f"**{playerObject.first_name} {playerObject.last_name}** has been created. [View profile?](https://hoopsim.com/player/{playerObject.id})",
                )
                # Redirect to the player page
                messages.success(request, "Player created successfully!")
                return redirect(player, id=playerObject.id)
            else:
                messages.error(request, status)
                return redirect(create_player)
        # If the form is invalid, or the player creation failed, redirect to the create player page
        return redirect(create_player)
    else:
        context = {"create_player_form": PlayerForm}
        return render(request, "main/players/create.html", context)


def players(request):
    context = {
        "title": "Players",
    }
    # Get the league players
    league_players = Player.objects.all()
    # Paginate the league players
    paginator = Paginator(league_players, 10)
    page_number = request.GET.get("page")
    context["page"] = paginator.get_page(page_number)
    # Return the players page
    return render(request, "main/players/players.html", context)


def upgrade_logs(request, id):
    # Check if the player exists
    player = Player.objects.get(pk=id)
    if not player:
        return HttpResponse("Sorry, this player doesn't exist!")
    # Get the upgrade logs
    logs = player.history_list.history["upgrade_logs"]
    logs.reverse()
    if player:
        context = {
            "name": f"{player.first_name} {player.last_name}",
            "logs": logs,
        }
        return render(request, "main/players/history.html", context)
    else:
        return HttpResponse("Sorry, this player doesn't exist!")


def cash_logs(request, id):
    # Check if the player exists
    player = Player.objects.get(pk=id)
    if not player:
        return HttpResponse("Sorry, this player doesn't exist!")
    # Get the upgrade logs if date is not older than two weeks
    one_week_ago = timezone.now() - datetime.timedelta(days=7)
    logs = Transaction.objects.filter(player=player, date__gte=one_week_ago).order_by(
        "-date"
    )
    if player:
        context = {
            "name": f"{player.first_name} {player.last_name}",
            "logs": logs,
        }
        return render(request, "main/players/cash_history.html", context)
    else:
        return HttpResponse("Sorry, this player doesn't exist!")


def team(request, id):
    team_object = Team.objects.get(pk=id)
    context = {
        "title": team_object.name,
        "team": team_object,
    }
    return render(request, "main/teams/team.html", context)


def teams(request):
    context = {
        "title": "Teams",
    }
    # Get the league teams
    league_teams = Team.objects.all()
    # Paginate the league teams
    paginator = Paginator(league_teams, 8)
    page_number = request.GET.get("page")
    context["page"] = paginator.get_page(page_number)
    # Return the players page
    return render(request, "main/teams/teams.html", context)


def trade(request):
    # Get the user
    user = request.user
    # Check if the user is a GM
    # Get first team user owns
    team = Team.objects.get(manager=user)
    if not team:
        return HttpResponse("Sorry, you don't have permission to view this page!")
    # Get sent & received trades (that are pending)
    sent_trades = TradeOffer.objects.filter(
        sender=team, accepted=False, finalized=False
    )
    received_trades = TradeOffer.objects.filter(
        receiver=team, accepted=False, finalized=False
    )
    # Trades that have been accepted (but not finalized)
    accepted_trades = TradeOffer.objects.filter(
        Q(sender=team) | Q(receiver=team), accepted=True, finalized=False
    )
    # Create the context
    context = {
        "title": "Trade",
        "user_team": team,
        "teams": Team.objects.all(),
        "sent_trades": sent_trades,
        "received_trades": received_trades,
        "accepted_trades": accepted_trades,
    }
    return render(request, "main/teams/trade.html", context)


def accept_trade(request, id):
    # Get some form data
    user = request.user
    # Get trade details
    trade_object = TradeOffer.objects.get(id=id)
    sender = trade_object.sender
    receiver = trade_object.receiver
    # Check if the user is a GM
    if not receiver.manager == user:
        messages.error(request, "❌ You don't have permission to accept this trade!")
        return redirect(home)
    # Check if user is sender
    if sender.manager == user:
        messages.error(request, "❌ You can't accept your own trade!")
        return redirect(trade)
    # Check if the trade is pending
    if trade_object.accepted == True:
        messages.error(request, "❌ This trade has already been accepted!")
        return redirect(trade)
    # Check if the trade is finalized
    if trade_object.finalized == True:
        messages.error(request, "❌ This trade has already been finalized!")
        return redirect(trade)
    # Accept the trade
    trade_object.accepted = True
    trade_object.save()
    # Redirect to the trade page
    messages.success(
        request, f"✅ Your trade has been accepted - we will finalize it soon!"
    )
    return redirect(trade)


def decline_trade(request, id):
    if request.method == "POST":
        # Get some form data
        user = request.user
        # Get trade details
        trade_object = TradeOffer.objects.get(id=id)
        receiver = trade_object.receiver
        # Check if the user is a GM
        if not receiver.manager == user:
            messages.error(request, "❌ You don't have permission to accept this trade!")
            return redirect(home)
        if trade_object.finalized == True:
            messages.error(request, "❌ This trade has already been finalized!")
            return redirect(trade)
        # Delete the trade & redirect to the trade page
        trade_object.delete()
        messages.success(request, "✅ You have declined this trade!")
        return redirect(trade)


def trade_panel(request):
    # Get the user
    user = request.user
    # Check if user can approve trades
    if not user.can_approve_trades:
        return HttpResponse("Sorry, you don't have permission to view this page!")
    # Get pending trades
    pending_trades = TradeOffer.objects.filter(accepted=True, finalized=False)
    # Create the context
    context = {
        "title": "Trade Panel",
        "pending_trades": pending_trades,
    }
    # Return the trade panel page
    return render(request, "main/teams/trade_panel.html", context)


def daily_reward(request):
    # Get the current date
    user = request.user
    # Get the last date the daily rewards were given out
    last_reward = user.last_reward
    # If the daily rewards haven't been given out today, give them out
    if not last_reward:
        # Give the user their daily rewards
        # Update the user's last reward date
        pass
    else:
        # Check if the last reward was given out today
        # If it was, return an error
        # If it wasn't, give the user their daily rewards
        # and update the user's last reward date
        pass


def upgrades_pending(request):
    # Collect user & player information
    user = request.user
    if not user.can_update_players:
        return HttpResponse("Sorry, you don't have permission to view this page!")
    else:
        # Get the user's pending upgrades
        upgrades = Player.objects.filter(upgrades_pending=True)
        files = {}
        # Iterate through the players who have pending upgrades
        for player in upgrades:
            game_file = hoops_player_export.export_player(player)
            json_dump = json.dumps(game_file, indent=4)
            files[f"({player.id}) {player.first_name} {player.last_name}"] = [
                json_dump,
                player.id,
            ]
        # Return the pending upgrades page
        return render(request, "main/players/pending.html", {"files": files})


def mock_builder(request):
    # Check if the tag is in the list of position starting attributes
    context = {
        "title": "Archetypes & Traits",
        "info": league_config.position_starting_attributes["PG"],
        "height_choices": league_config.height_choices,
        "archetype_choices": league_config.archetype_choices,
        "position_choices": league_config.position_choices,
        "trait_choices": league_config.trait_choices,
        "welcome_message": True,
    }
    # Return the build info page
    return render(request, "main/players/build-info.html", context)


@login_required(login_url="/login/discord/")
def coupons(request):
    context = {
        "title": "Coupons",
    }
    user = request.user
    # Get the user's players
    players = Player.objects.filter(discord_user=user)
    if players:
        # Add list of players to context
        context["player_list"] = players
        # Return the coupons page
        return render(request, "main/league/coupons.html", context)
    else:
        return HttpResponse("You don't have any players!")


def frivolities(request):
    context = {
        "title": "Frivolities",
    }
    # Find out how many total players, then how many in each position there are
    context["position_counts"] = {
        "Total": Player.objects.count(),
        "PG": Player.objects.filter(primary_position="PG").count(),
        "SG": Player.objects.filter(primary_position="SG").count(),
        "SF": Player.objects.filter(primary_position="SF").count(),
        "PF": Player.objects.filter(primary_position="PF").count(),
        "C": Player.objects.filter(primary_position="C").count(),
    }
    # Return the frivolities page
    return render(request, "main/league/frivolities.html", context)


# Reloadable form views
def add_player_cash(request):
    if request.method == "POST":
        user = request.user
        if user.can_update_players:
            # Get the player and amount
            id = request.POST.get("id")
            amount = request.POST.get("amount")
            reason = request.POST.get("reason")
            # Get the player
            player = Player.objects.get(pk=id)
            history_list = player.history_list.history
            # Add the cash to the player's account
            if player.cash + int(amount) > league_config.primary_currency_max:
                messages.error(
                    request,
                    f"A player can only have ${league_config.primary_currency_max} cash.",
                )
                return redirect("player", id=id)
            else:
                # Add the player's cash
                player.cash += int(amount)
                # Add new transaction (Transaction)
                transaction = Transaction(
                    transaction_type="cash_given",
                    amount=amount,
                    reason=reason,
                    giver=user,
                    player=player,
                    date=timezone.now(),
                )
                # Save the player & transaction
                player.save()
                transaction.save()
                # Send a webhook message
                discord_webhooks.send_webhook(
                    url="cash",
                    title="Cash Added",
                    message=f"**{user.discord_tag}** added **${amount}** to {player.first_name} {player.last_name}'s account.\n```{reason}```",
                )
                # Return the updated cash
                messages.success(request, f"Cash added, player now has ${player.cash}!")
                return redirect("player", id=id)
    else:
        messages.error(request, "Something went wrong!")
        return redirect("player", id=id)


def take_player_cash(request):
    if request.method == "POST":
        user = request.user
        if user.can_update_players:
            # Get the player and amount
            id = request.POST.get("id")
            amount = request.POST.get("amount")
            reason = request.POST.get("reason")
            # Get the player
            player = Player.objects.get(pk=id)
            # Take the cash from the player's account
            if player.cash - int(amount) < 0:
                messages.error(request, "A player cannot have negative cash.")
                return redirect("player", id=id)
            else:
                # Add the player's cash
                player.cash -= int(amount)
                # Add new transaction (Transaction)
                transaction = Transaction(
                    transaction_type="cash_taken",
                    amount=amount,
                    reason=reason,
                    giver=user,
                    player=player,
                    date=timezone.now(),
                )
                # Save the player & transaction
                player.save()
                transaction.save()
                # Send a webhook message
                discord_webhooks.send_webhook(
                    url="cash",
                    title="Cash Taken",
                    message=f"**{user.discord_tag}** took **${amount}** from {player.first_name} {player.last_name}'s account.\n```{reason}```",
                )
                # Return the updated cash
                messages.success(request, f"Cash taken, player now has ${player.cash}!")
                return redirect("player", id=id)
    else:
        messages.error(request, "Something went wrong!")
        return redirect("player", id=id)


def update_player_vitals(request, id):
    if request.method == "POST":
        # Get some form values/data
        user = request.user
        player = Player.objects.get(pk=id)
        # Vitals
        jersey = request.POST.get("jersey")
        cyberface = request.POST.get("cyberface")
        use_game = request.POST.get("use_game")
        # Playstyles
        playstyle1 = request.POST.get("playstyle1")
        playstyle2 = request.POST.get("playstyle2")
        playstyle3 = request.POST.get("playstyle3")
        playstyle4 = request.POST.get("playstyle4")
        # Database playstyles
        db_playstyle1 = player.statics["playstyles"]["playstyle1"]
        db_playstyle2 = player.statics["playstyles"]["playstyle2"]
        db_playstyle3 = player.statics["playstyles"]["playstyle3"]
        db_playstyle4 = player.statics["playstyles"]["playstyle4"]
        # Some form validations
        if not player.discord_user == user:
            messages.error(request, "You do not have permission to do that!")
            return redirect("player", id=id)
        if not jersey or not cyberface:
            messages.error(request, "Please fill out all fields!")
            return redirect("player", id=id)
        if int(jersey) > 99 or int(jersey) < 0:
            messages.error(request, "Please enter a valid jersey number! (0-99)")
            return redirect("player", id=id)
        # Check if int(cyberface) exists in database
        if Player.objects.filter(cyberface=int(cyberface)).exists():
            if int(cyberface) != 1 and int(cyberface) != player.cyberface:
                messages.error(request, "That cyberface already exists!")
                return redirect("player", id=id)
        # Check if changes were made (vitals & playstyles)
        if (
            player.jersey_number == int(jersey)
            and player.cyberface == int(cyberface)
            and str(player.use_game_tendencies) == use_game
            and playstyle1 == db_playstyle1
            and playstyle2 == db_playstyle2
            and playstyle3 == db_playstyle3
            and playstyle4 == db_playstyle4
        ):
            messages.error(request, "No changes were made!")
            return redirect("player", id=id)
        # Check if there are duplicate playstyles
        playstyle_list = [playstyle1, playstyle2, playstyle3, playstyle4]
        if len(playstyle_list) != len(set(playstyle_list)):
            messages.error(request, "You cannot have duplicate playstyles!")
            return redirect("player", id=id)
        # Update the player's vitals (if changed)
        if player.jersey_number != int(jersey):
            player.jersey_number = int(jersey)
        if player.cyberface != int(cyberface):
            player.cyberface = cyberface
        if str(player.use_game_tendencies) != use_game:
            if use_game == "True":
                player.use_game_tendencies = True
            else:
                player.use_game_tendencies = False
        # Update the player's play-styles (if changed)
        if playstyle1 != db_playstyle1 and playstyle1:
            player.statics["playstyles"]["playstyle1"] = playstyle1
        if playstyle2 != db_playstyle2 and playstyle2:
            player.statics["playstyles"]["playstyle2"] = playstyle2
        if playstyle3 != db_playstyle3 and playstyle3:
            player.statics["playstyles"]["playstyle3"] = playstyle3
        if playstyle4 != db_playstyle4 and playstyle4:
            player.statics["playstyles"]["playstyle4"] = playstyle4
        player.save()
        # Send a webhook message
        discord_webhooks.send_webhook(
            url="upgrade",
            title="Vital Update",
            message=f"**{user.discord_tag}** updated {player.first_name} {player.last_name}'s vitals.",
        )
        # Return the updated vitals
        messages.success(request, "Player vitals updated!")
        return redirect("player", id=id)


def update_player_pending_upgrades(request):
    if request.method == "POST":
        user = request.user
        if user.can_update_players:
            pending_players = Player.objects.filter(upgrades_pending=True)
            for player in pending_players:
                player.upgrades_pending = False
                player.save()
            return HttpResponse("✅ Success!")
    else:
        return HttpResponse("Invalid request!")


# Check views
def check_player_search(request):
    if request.method == "POST":
        search = request.POST.get("search")
        if search:
            # Check for players based on first and last name
            players = Player.objects.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(discord_user__discord_tag__icontains=search)
            )
            # Check if there were any players found
            if not players:
                return HttpResponse("<p class='text-danger'>No players found!</p>")
            # Render the player list fragment to string
            html = render_to_string(
                "main/ajax/player_list_fragment.html", {"page": players}
            )
            # Return the player list fragment
            return HttpResponse(html)
    else:
        return HttpResponse("Invalid request!")


def check_team_search(request):
    if request.method == "POST":
        search = request.POST.get("search")
        if search:
            # Check for teams based on name
            teams = Team.objects.filter(name__icontains=search)
            # Check if there were any teams found
            if not teams:
                return HttpResponse("<p class='text-danger'>No teams found!</p>")
            # Render the player list fragment to string
            html = render_to_string(
                "main/ajax/team_list_fragment.html", {"page": teams}
            )
            # Return the player list fragment
            return HttpResponse(html)
    else:
        return HttpResponse("Invalid request!")


def check_coupon_code(request):
    if request.method == "POST":
        # Get ID & coupon code
        id = int(request.POST.get("id"))
        code = request.POST.get("coupon")
        coupon = Coupon.objects.filter(code=code).first()
        # Check if ID & coupon exist
        if not id or not coupon:
            return HttpResponse(
                "<p id='coupon-result' class='mt-2 text-danger' style='font-size:12px;'>Invalid coupon code or identity!</p>"
            )
        # Get user & player
        user = request.user
        player = Player.objects.filter(id=id).first()
        # Check if ID & coupon exist
        if not player or not player.discord_user == user:
            return HttpResponse(
                "<p id='coupon-result' class='mt-2 text-danger' style='font-size:12px;'>You don't own this player!</p>"
            )
        history_list = player.history_list.history
        # Check if used_coupons exists, if it doesn't create it
        if not "used_coupons" in history_list:
            history_list["used_coupons"] = []
        used_coupons = history_list["used_coupons"]
        # Check if the coupon code has already been used
        if coupon.code in used_coupons:
            return HttpResponse(
                "<p id='coupon-result' class='mt-2 text-danger' style='font-size:12px;'>Coupon code already used!</p>"
            )
        # Check if the coupon code is one_use
        if coupon.one_use and coupon.used:
            return HttpResponse(
                "<p id='coupon-result' class='mt-2 text-danger' style='font-size:12px;'>Coupon code already used!</p>"
            )
        # Mark coupon as used & add player cash
        used_coupons.append(coupon.code)
        player.cash += coupon.amount
        coupon.used = True
        # Save the player & history list
        coupon.save()
        player.save()
        player.history_list.save()
        # Send a success webhook
        discord_webhooks.send_webhook(
            url="coupon",
            title="Coupon",
            message=f"{player.first_name} {player.last_name} successfully redeemed a coupon code worth ${coupon.amount}!\n```✅ Coupon: {coupon.name}```",
        )
        # Return the success message
        return HttpResponse(
            "<p id='coupon-result' class='mt-2 text-success' style='font-size:12px;'>Coupon code successfully redeemed!</p>"
        )


def check_starting_attributes(request):
    if request.method == "POST":
        # Get the form data
        position = request.POST.get("position")
        height = request.POST.get("height")
        weight = request.POST.get("weight")
        primary_archetype = request.POST.get("archetype1")
        secondary_archetype = request.POST.get("archetype2")
        trait1 = request.POST.get("trait1")
        trait2 = request.POST.get("trait2")
        # Define some variables
        height_limits = league_config.min_max_heights[position]
        weight_limits = league_config.min_max_weights[position]
        convert_height = hoops_extra_convert.convert_to_height
        # Check some validations first
        if not weight:
            return HttpResponse("❌ Weight is required!")
        if int(height) > height_limits["max"] or int(height) < height_limits["min"]:
            return HttpResponse(
                f"❌ Height must be between {convert_height(height_limits['min'])} and {convert_height(height_limits['max'])}!",
            )
        if int(weight) > weight_limits["max"] or int(weight) < weight_limits["min"]:
            return HttpResponse(
                f"❌ Weight must be between {weight_limits['min']} and {weight_limits['max']}!",
            )
        if trait1 == trait2:
            return HttpResponse("❌ Traits cannot be the same!")
        # Check what the starting attributes would be
        starting_attributes = {
            "height": int(height),
            "weight": int(weight),
            "primary_position": position,
            "attributes": copy.deepcopy(
                league_config.position_starting_attributes[position]
            ),
        }
        mock_player = hoops_player_physicals.setStartingPhysicals(
            starting_attributes, mock=True
        )
        player_attributes = mock_player["attributes"]
        # Add archetype bonuses
        primary_list = league_config.archetype_attribute_bonuses[primary_archetype]
        secondary_list = league_config.archetype_attribute_bonuses[secondary_archetype]
        for attribute in primary_list:
            player_attributes[attribute] += league_config.archetype_primary_bonus
        for attribute in secondary_list:
            player_attributes[attribute] += league_config.archetype_secondary_bonus
        # Format the attributes with primary/secondary/base tags
        mock_player_attributes = {"primary": {}, "secondary": {}, "base": {}}
        for attribute in player_attributes:
            if attribute in primary_list:
                mock_player_attributes["primary"][attribute] = player_attributes[
                    attribute
                ]
                continue
            elif attribute in secondary_list:
                mock_player_attributes["secondary"][attribute] = player_attributes[
                    attribute
                ]
                continue
            else:
                mock_player_attributes["base"][attribute] = player_attributes[attribute]
        # Add trait bonuses
        mock_player_badges = {}
        trait1_list = league_config.trait_badge_unlocks[trait1]
        trait2_list = league_config.trait_badge_unlocks[trait2]
        for badge in trait1_list:
            mock_player_badges[badge] = "[P]"
        for badge in trait2_list:
            # We don't want overlapping badges to be marked as secondary if they are also primary
            if not badge in trait1_list:
                mock_player_badges[badge] = "[S]"
        # Return the starting attributes
        context = {
            "title": "Archetypes & Traits",
            "header": position,
            "height_choices": league_config.height_choices,
            "primary_attributes": mock_player_attributes["primary"],
            "secondary_attributes": mock_player_attributes["secondary"],
            "base_attributes": mock_player_attributes["base"],
            "badges": mock_player_badges,
            "archetype_choices": league_config.archetype_choices,
            "position_choices": league_config.position_choices,
            "trait_choices": league_config.trait_choices,
            "welcome_message": False,
        }
        html = render_to_string("main/ajax/position_fragment.html", context)
        return HttpResponse(html)
    else:
        return HttpResponse("Invalid request!")


def check_position_count(request):
    if request.method == "POST":
        # Get the form data
        position = request.POST.get("position")
        player_type = request.POST.get("type")
        # Initialize the position position count
        position_count = 0
        # Get the position count
        if player_type == "unsigned":
            position_count = Player.objects.filter(
                current_team=None, primary_position=position
            ).count()
        elif player_type == "signed":
            position_count = Player.objects.filter(
                current_team__isnull=False, primary_position=position
            ).count()
        # Return the position count
        return HttpResponse(
            f"There are <b>{position_count}</b> players that play at this position."
        )
    else:
        return HttpResponse("Invalid request!")


def check_upgrade_validation(request):
    if request.method == "POST":
        # Find the player
        id = request.POST.get("id")
        player = Player.objects.get(id=id)
        if not player:
            return HttpResponse("❌ Player not found!")
        # Check the form data
        form = UpgradeForm(request.POST)
        if form.is_valid():
            # Remove unchanged attributes
            # So nothing is upgraded if the user doesn't change anything
            changed_data = {}
            cleaned_data = form.cleaned_data
            for k, v in cleaned_data.items():
                if k in player.attributes:
                    if int(v) > player.attributes[k]:
                        changed_data[k] = v
                elif k in player.badges:
                    if int(v) > player.badges[k]:
                        changed_data[k] = v
                elif k in player.tendencies:
                    if int(v) != player.tendencies[k]:
                        changed_data[k] = v
            # Attempt to upgrade the player
            response = hoops_player_upgrade.createUpgrade(player, changed_data)
            # Send a webhook to Discord
            discord_webhooks.send_webhook(
                url="upgrade",
                title="Player Upgrade",
                message=f"**{player.first_name} {player.last_name}** has attempted an upgrade. [View logs?](https://hoopsim.com/logs/upgrades/{player.id})\n```{response}```",
            )
            # Return to the player page
            return HttpResponse(response)
        else:
            return HttpResponse("❌ Invalid form data!")


def check_player_leaders(request):
    # Get the form data
    field = request.POST.get("field")
    # Get the player leaders for this field
    leaders = Player.objects.order_by(f"-{field}")[:10]
    # Create context & send back
    context = {
        "leaders": leaders,
        "field": field,
    }
    html = render_to_string("main/ajax/leaders_fragment.html", context)
    return HttpResponse(html)


def check_meta_leaders(request):
    # Get the form data
    meta = request.POST.get("meta")

    # Calculate player using each meta
    leaders = {}
    players = Player.objects.all()
    total_players = len(players)
    for player in players:
        if meta == "archetype":
            if not player.primary_archetype in leaders:
                leaders[player.primary_archetype] = [1, 0]
            else:
                leaders[player.primary_archetype][0] += 1
            if not player.secondary_archetype in leaders:
                leaders[player.secondary_archetype] = [0, 1]
            else:
                leaders[player.secondary_archetype][1] += 1
        elif meta == "trait":
            if not player.trait_one in leaders:
                leaders[player.trait_one] = [1, 0]
            else:
                leaders[player.trait_one][0] += 1
            if not player.trait_two in leaders:
                leaders[player.trait_two] = [0, 1]
            else:
                leaders[player.trait_two][1] += 1
        elif meta == "height":
            height = hoops_extra_convert.convert_to_height(player.height)
            if not height in leaders:
                leaders[height] = [1, 0]
            else:
                leaders[height][0] += 1
    # Add percentage to each meta (based on total players)
    for m in leaders:
        leaders[m].append(f"{leaders[m][0]}/{total_players}")
        leaders[m].append(f"{leaders[m][1]}/{total_players}")
    # Order the leaders dictionary before sending
    leaders = dict(sorted(leaders.items(), key=lambda item: item[1][0], reverse=True))
    # Create context & send back
    context = {
        "leaders": leaders,
        "meta_name": meta,
        "leaders": leaders,
    }
    html = render_to_string("main/ajax/meta_fragment.html", context)
    return HttpResponse(html)


def check_team_roster(request):
    if request.method == "POST":
        # Get the form data
        other_team = request.POST.get("other_team")
        # Get the team roster
        user_team_object = Team.objects.get(manager=request.user)
        other_team_object = Team.objects.get(id=other_team)
        # Send roster back
        context = {
            "title": "Trade",
            "user_team": user_team_object,
            "other_team": other_team_object,
            "teams": Team.objects.all(),
        }
        html = render_to_string("main/ajax/trade_team_fragment.html", context)
        return HttpResponse(html)


def check_trade_validation(request):
    # Get the form data
    user = request.user
    user_team_id = request.POST.get("user_team")
    other_team_id = request.POST.get("other_team")
    notes = request.POST.get("notes")
    user_team_ids = request.POST.getlist("user_team_players")
    other_team_ids = request.POST.getlist("other_team_players")
    # Validate the form data
    if not user_team_id or not other_team_id:
        return HttpResponse("❌ Invalid team data!")
    if not user_team_ids or not other_team_ids:
        return HttpResponse("❌ Invalid player data!")
    # Get the teams
    user_team = Team.objects.get(id=user_team_id)
    other_team = Team.objects.get(id=other_team_id)
    # Get the players
    user_team_players = Player.objects.filter(id__in=user_team_ids)
    other_team_players = Player.objects.filter(id__in=other_team_ids)
    # Check if the user is the manager of the user team
    if user_team.manager != user:
        return HttpResponse(f"❌ You are not the manager of the {user_team.name}!")
    # Check if the user team players exist
    if not user_team_players or not other_team_players:
        return HttpResponse("❌ Players weren't found!")
    # Check if the trade is valid
    trade_players = {
        "user_team": user_team_players,
        "other_team": other_team_players,
    }
    response = hoops_team_trade.validate_trade(
        user_team, other_team, trade_players, league_config.hard_cap
    )
    status = response[0]
    message = response[1]
    # Send back the response
    if status:
        # Check if a trade already exists between these teams
        existing_trade = TradeOffer.objects.filter(
            sender=user_team, receiver=other_team, finalized=False
        ).first()
        if existing_trade:
            return HttpResponse(f"❌ A trade already exists between these teams!")
        # Create a trade object
        offer = {"user_players": [], "other_players": []}
        for player in user_team_players:
            offer["user_players"].append(
                [
                    int(player.id),
                    f"{player.first_name} {player.last_name}",
                    player.salary,
                ]
            )
        for player in other_team_players:
            offer["other_players"].append(
                [
                    int(player.id),
                    f"{player.first_name} {player.last_name}",
                    player.salary,
                ]
            )
        trade_object = TradeOffer(
            offer=offer,
            sender=user_team,
            receiver=other_team,
            notes=notes,
        )  # Accepted, approved, and finalized will be set to False by default
        trade_object.save()
        # Return the response
        return HttpResponse(f"{message}<br>✅ Trade sent.")
    else:
        return HttpResponse(f"{message}")


def check_finalize_trade(request):
    if request.method == "POST":
        # Get some form data
        user = request.user
        decision = request.POST.get("decision")
        trade_id = request.POST.get("trade_id")
        # If user can approve trades
        if not user.can_approve_trades:
            return HttpResponse("Sorry, you don't have permission to view this page!")
        # Get trade details
        trade_object = TradeOffer.objects.get(id=int(trade_id))
        sender = trade_object.sender
        receiver = trade_object.receiver
        # Validate trade
        if trade_object.finalized:
            messages.error(
                request,
                f"❌ Trade between {sender.name} and {receiver.name} has already been finalized!",
            )
        # Check if the trade is pending
        if decision == "accept":
            # Check if the trade is valid
            user_players = Player.objects.filter(current_team=sender)
            other_players = Player.objects.filter(current_team=receiver)
            trade_players = {
                "user_team": [],
                "other_team": [],
            }
            # Make sure players are on original teams (easier to do here than in the validate_trade function)
            for player in user_players:
                for p in trade_object.offer["other_players"]:
                    if player.id == p[0]:
                        trade_object.delete()
                        return HttpResponse(
                            f"❌ {player.first_name} {player.last_name} is no longer on the {sender.name}!"
                        )
                else:
                    trade_players["user_team"].append(player)
            for player in other_players:
                for p in trade_object.offer["user_players"]:
                    if player.id == p[0]:
                        trade_object.delete()
                        return HttpResponse(
                            f"❌ {player.first_name} {player.last_name} is no longer on the {receiver.name}!"
                        )
                else:
                    trade_players["other_team"].append(player)
            # Check if the trade is valid
            response = hoops_team_trade.validate_trade(
                sender, receiver, trade_players, league_config.hard_cap
            )
            status = response[0]
            # If the trade is valid
            if status:
                # Finalize the trade
                trade_object.accepted = True
                trade_object.approved = True
                trade_object.finalized = True
                trade_object.save()
                # Send players to new teams
                for player in trade_object.offer["user_players"]:
                    player_object = Player.objects.get(id=player[0])
                    player_object.current_team = receiver
                    player_object.save()
                for player in trade_object.offer["other_players"]:
                    player_object = Player.objects.get(id=player[0])
                    player_object.current_team = sender
                    player_object.save()
                # Send discord webhook
                discord_webhooks.send_webhook(
                    url="trade",
                    title="✅ Trade Finalized",
                    message=f"**{sender.name}** received\n```{' + '.join([p[1] for p in trade_object.offer['other_players']])}```\n**{receiver.name}** receives\n```{' + '.join([p[1] for p in trade_object.offer['user_players']])}```\n{trade_object.notes}",
                )
            else:
                # Delete the trade & redirect to the trade_panel page
                trade_object.delete()
                # Send discord webhook
                discord_webhooks.send_webhook(
                    url="trade",
                    title="❌ Trade Vetoed",
                    message=f"**{sender.name}** received\n```{' + '.join([p[1] for p in trade_object.offer['other_players']])}```\n**{receiver.name}** receives\n```{' + '.join([p[1] for p in trade_object.offer['user_players']])}```\n{trade_object.notes}",
                )
        elif decision == "decline":
            # Delete the trade & redirect to the trade_panel page
            trade_object.delete()
            # Send discord webhook
            discord_webhooks.send_webhook(
                url="trade",
                title="❌ Trade Vetoed",
                message=f"**{sender.name}** received\n```{' + '.join([p[1] for p in trade_object.offer['other_players']])}```\n**{receiver.name}** receives\n```{' + '.join([p[1] for p in trade_object.offer['user_players']])}```",
            )
        # Reload trade list fragment
        context = {
            "title": "Trade Panel",
            "pending_upgrades": TradeOffer.objects.filter(
                accepted=True, finalized=False
            ),
        }
        html = render_to_string("main/ajax/trade_list_fragment.html", context)
        return HttpResponse(html)
