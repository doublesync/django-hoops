from main.league import config as league_config
from main.models import Player
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Resets primary/secondary attributes & badges for a player to re-integrate."
    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='The ID of the player to reset.')
    def handle(self, *args, **options):
        player_id = options['id']
        # Attempt to find the player
        try:
            player = Player.objects.get(pk=player_id)
        except Player.DoesNotExist:
            raise CommandError(f"Player with ID {player_id} does not exist.")
        # Change the player's attributes
        player.primary_attributes = None
        player.secondary_attributes = None
        player.primary_badges = None
        player.secondary_badges = None
        player.cash += player.spent
        player.spent = 0
        player.attributes = league_config.position_starting_attributes[player.primary_position]
        for badge, _ in player.badges.items():
            player.badges[badge] = 0
        # Save the player
        player.save()
        self.stdout.write(self.style.SUCCESS(f"{player.first_name} {player.last_name} has been reset."))
