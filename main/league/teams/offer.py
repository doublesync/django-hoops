from ...models import ContractOffer
from .. import config as league_config

def createOffer(team, player, years, salary, option, benefits, notes):
    # Check for existing offer
    existing_offer = ContractOffer.objects.filter(team=team, player=player)
    if existing_offer:
        existing_offer.delete()
    # Validate offer details
    if years < league_config.min_years:
        return "❌ Years are too low."
    if years > league_config.max_years:
        return "❌ Years are too high."
    if salary < league_config.min_salary:
        return "❌ Salary is too low."
    if salary > league_config.max_salary:
        return "❌ Salary is too high."
    # Create the offer
    offer = ContractOffer(
        team=team,
        player=player,
        years=years,
        salary=salary,
        option=option,
        benefits=benefits,
        notes=notes,
    )
    offer.save()
    # Return success message
    return "✅ Offer created successfully."