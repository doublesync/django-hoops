from ..models import Player
from ..league.user import notify as hoops_user_notify


def auto_collect_rewards():
    league_players = Player.objects.all()
    for player in league_players:
        discord_user = player.discord_user
        if discord_user and discord_user.auto_collect_rewards:
            # Pay the player their rewards
            player.cash += player.salary
            player.save()
            # Notify the user
            hoops_user_notify.notify(
                user=discord_user,
                message=f"Your player {player.first_name} {player.last_name} has auto collected their weekly salary of ${player.salary}.",
            )
