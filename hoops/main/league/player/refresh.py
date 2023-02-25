# This script is used to refresh the player's contract
# information, salary, free agency status, etc.
from ...models import Offer

def resetContract(player):
    # Reset the contract details
    player.contract_details.contract_year = 1
    player.contract_details.contract_length = 1
    player.contract_details.year_one_salary = 0
    player.contract_details.year_two_salary = 0
    player.contract_details.year_three_salary = 0
    player.contract_details.player_option = False
    player.contract_details.team_option = False
    player.contract_details.no_trade_clause = False
    player.contract_details.no_cut_clause = False
    # Save the contract details
    player.contract_details.save()

def createOffer(player, choice, ntc, ncc):
    # Create a new offer
    offer = Offer(
        offer_player=player,
        offer_team=player.current_team,
        offer_length=1,
        year_one_salary=player.year_one_salary,
        year_two_salary=player.year_two_salary,
        year_three_salary=player.year_three_salary,
        player_option=False,
        team_option=False,
        no_trade_clause=ntc,
        no_cut_clause=ncc,
        player_choice=choice
    )
    # Save the offer
    offer.save()

def updateContract(player):
    # Validations
    if (player.free_agent) or not (player.contract_details):
        return False
    # Update the player's contract
    player.contract_details.contract_year += 1
    player.years_played += 1
    # Gather the needed contract details
    ntc = player.contract_details.no_trade_clause
    ncc = player.contract_details.no_cut_clause
    po = player.contract_details.player_option
    to = player.contract_details.team_option
    # Change free agency status if necessary
    if (player.contract_details.contract_year > 3):
        # Reset the contract
        resetContract(player)
        # Make sure the player is a free agent
        player.free_agent = True
        # Reset the contract
        if (po):
            createOffer(player=player, choice=True, ntc=ntc, ncc=ncc)
        elif (to):
            createOffer(player=player, choice=False, ntc=ntc, ncc=ncc)
            player.free_agent = False
        print(f"✅ Contract updated! {player.first_name} {player.last_name} is now a free agent!")
    else:
        print(f"✅ Contract updated! {player.first_name} {player.last_name} is still under contract with the {player.current_team.name}!")
    # Save the contract details
    player.contract_details.save()
    player.save()
    # Return the player
    return player