from ...models import Player
from ...models import HistoryList
from ...models import FeatureList
from ...models import Contract
from ...models import PlayerOffers

from ...league import config as league_config
from ...league.player import limits as league_limits

max_players = league_config.max_players

def playerCount(user):
    return Player.objects.filter(discord_user=user).count()

def validatePlayerCreation(user, formData):
    # Check if the user has reached the max number of players
    if playerCount(user) >= max_players:
        return [False, "❌ You have reached the max number of players."]
    # If everything is good, create the player
    return [True, None]

def createPlayer(user, formData):
    # Create the player's relationship objects
    historyList = HistoryList.objects.create()
    featureList = FeatureList.objects.create()
    contractDetails = Contract.objects.create()
    playerOffers = PlayerOffers.objects.create()
    # Create the player
    newPlayer = Player.objects.create(
        # Customs
        first_name=formData["first_name"],
        last_name=formData["last_name"],
        weight=formData["weight"],
        height=formData["height"],
        primary_position=formData["primary_position"],
        secondary_position=formData["secondary_position"],
        jersey_number=formData["jersey_number"],
        # Relationships
        discord_user=user,
        contract_details=contractDetails,
        contract_offers=playerOffers,
        feature_list=featureList,
        history_list=historyList,
    )
    # Update the player's limits
    myLimits = league_limits.getPlayerLimits(newPlayer)
    updatedPlayer = myLimits[0]
    # Save the player
    historyList.save()
    featureList.save()
    contractDetails.save()
    playerOffers.save()
    updatedPlayer.save()
    # Return the player
    return newPlayer