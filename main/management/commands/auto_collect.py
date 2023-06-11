from django.utils import timezone
from ...models import Player
from ...models import DiscordUser
from ...league import config as league_config
from ...league.user import notify as hoops_user_notify
from ...discord import webhooks as hoops_webhooks
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        # Auto collect/pay these players
        league_users = DiscordUser.objects.all()
        for discord_user in league_users:
            # Check if the user has been paid already
            last_reward = discord_user.last_reward
            user_players = Player.objects.filter(discord_user=discord_user)
            if not last_reward or timezone.now().day != last_reward.day:
                for player in user_players:
                    if discord_user and discord_user.auto_collect_rewards:
                        # Pay the player their rewards
                        if player.salary >= league_config.free_agent_salary:
                            player.cash += player.salary
                        else:
                            player.cash += league_config.free_agent_salary
                        player.save()
                        # Notify the user
                        hoops_user_notify.notify(
                            user=discord_user,
                            message=f"Your player {player.first_name} {player.last_name} has auto collected their daily salary of ${player.salary}.",
                        )
                        # Discord webhook
                        hoops_webhooks.send_webhook(url="cash", title="✅ Auto Collect Players Paid", message="All auto collect players have been paid their contracts.")
                        # Send error message
                        self.stdout.write(
                            self.style.SUCCESS(f"Successfully auto collected for {player.first_name} {player.last_name}")
                        )
                        # Update the last reward date
                        discord_user.last_reward = timezone.now()
                        discord_user.save()
                    else:
                        # Send error message
                        self.stdout.write(
                            self.style.ERROR(f"Failed to auto collected for {player.first_name} {player.last_name}")
                        )
