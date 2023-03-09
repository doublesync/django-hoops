# # This script is used to refresh the player's contract
# # information, salary, free agency status, etc.
# from ...models import Offer
# from ...league import config as league_config


# def resetContract(player):
#     # Reset the contract details
#     player.contract_details.contract_year = 1
#     player.contract_details.contract_length = 1
#     player.contract_details.year_one_salary = 0
#     player.contract_details.year_two_salary = 0
#     player.contract_details.year_three_salary = 0
#     player.contract_details.player_option = False
#     player.contract_details.team_option = False
#     player.contract_details.no_trade_clause = False
#     player.contract_details.no_cut_clause = False
#     # Save the contract details
#     player.contract_details.save()


# def optionOffer(player, choice, ntc, ncc):
#     # Create a new offer
#     offer = Offer(
#         offer_player=player,
#         offer_team=player.current_team,
#         offer_length=1,
#         year_one_salary=player.year_one_salary,
#         year_two_salary=player.year_two_salary,
#         year_three_salary=player.year_three_salary,
#         player_option=False,
#         team_option=False,
#         no_trade_clause=ntc,
#         no_cut_clause=ncc,
#         player_choice=choice,
#     )
#     # Save the offer
#     offer.save()


# def playerOffer(player, team, length, y1, y2, y3, po, to, ntc, ncc):
#     # Validations
#     if not (player.free_agent):
#         return [False, "❌ Player is not a free agent."]
#     if (
#         (y1 > league_config.max_salary)
#         or (y2 > league_config.max_salary)
#         or (y3 > league_config.max_salary)
#     ):
#         return [False, "❌ One of your salaries is too high."]
#     if (
#         (y1 < league_config.min_salary)
#         or (y2 < league_config.min_salary)
#         or (y3 < league_config.min_salary)
#     ):
#         return [False, "❌ One of your salaries is too low."]
#     if (po) and (to):
#         return [False, "❌ A player can't have both a player option and a team option."]
#     if (y3 > 0) and (y2 <= 0):
#         return [
#             False,
#             "❌ A player can't have a third year salary without a second year salary.",
#         ]
#     if (length) > 3:
#         return [False, "❌ A player can't have a contract longer than three years."]
#     # Create a new offer
#     offer = Offer(
#         offer_player=player,  # The player that is signing the offer
#         offer_team=team,  # The team that the player is signing with
#         offer_length=length,  # Self-explanatory
#         year_one_salary=y1,  # Self-explanatory
#         year_two_salary=y2,  # Self-explanatory
#         year_three_salary=y3,  # Self-explanatory
#         player_option=po,  # Can the player pick up the option?
#         team_option=to,  # Can the team pick up the option?
#         no_trade_clause=ntc,  # Can the player veto a trade?
#         no_cut_clause=ncc,  # Can the player veto a team release?
#         player_choice=True,  # The player is always the one who chooses (in this case)
#     )
#     # Save the offer
#     offer.save()


# def updateContract(player):
#     # Validations
#     if (player.free_agent) or not (player.contract_details):
#         return False
#     # Update the player's contract
#     player.contract_details.contract_year += 1
#     player.years_played += 1
#     # Gather the needed contract details
#     ntc = player.contract_details.no_trade_clause
#     ncc = player.contract_details.no_cut_clause
#     po = player.contract_details.player_option
#     to = player.contract_details.team_option
#     # Change free agency status if necessary
#     if player.contract_details.contract_year > 3:
#         # Reset the contract
#         resetContract(player)
#         # Make sure the player is a free agent
#         player.free_agent = True
#         # Reset the contract
#         if po:
#             optionOffer(player=player, choice=True, ntc=ntc, ncc=ncc)
#         elif to:
#             optionOffer(player=player, choice=False, ntc=ntc, ncc=ncc)
#             player.free_agent = False
#         print(
#             f"✅ Contract updated! {player.first_name} {player.last_name} is now a free agent!"
#         )
#     else:
#         print(
#             f"✅ Contract updated! {player.first_name} {player.last_name} is still under contract with the {player.current_team.name}!"
#         )
#     # Save the contract details
#     player.contract_details.save()
#     player.save()
#     # Return the player
#     return player
