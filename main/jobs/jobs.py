from django.utils import timezone
from ..models import Player
from ..league.user import notify as hoops_user_notify
from ..discord import webhooks as hoops_webhooks


def auto_collect_rewards():
    league_players = Player.objects.all()
    for player in league_players:
        discord_user = player.discord_user
        if discord_user and discord_user.auto_collect_rewards:
            # Check if the player has been paid already
            last_reward = discord_user.last_reward
            if not last_reward or timezone.now().day != last_reward.day:
                # Pay the player their rewards
                player.cash += player.salary
                player.save()
                # Update the last reward date
                discord_user.last_reward = timezone.now()
                discord_user.save()
                # Notify the user
                hoops_user_notify.notify(
                    user=discord_user,
                    message=f"Your player {player.first_name} {player.last_name} has auto collected their daily salary of ${player.salary}.",
                )
                # Discord webhook
                hoops_webhooks.send_webhook(url="cash", title="✅ Auto Collect Players Paid", message="All auto collect players have been paid their contracts.")
            else:
                # Notify the user
                hoops_user_notify.notify(
                    user=discord_user,
                    message=f"Attempted to auto-collect payments {player.first_name} {player.last_name}, but they have already collected their daily salary of ${player.salary}.",
                )
