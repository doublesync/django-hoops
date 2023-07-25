from main.league import config as league_config
from main.league.player import physicals as player_physicals
from main.models import Player
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Resets primary/secondary attributes & badges for a player to re-integrate."
    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='The ID of the player to reset.')
        parser.add_argument('type', type=str, help='The type of badge to add to the player.')
        parser.add_argument('badge', nargs='+', type=str, help='The badge(s) to add to the player.')
    def handle(self, *args, **options):
        # Grab some argument options
        player_id = options['id']
        badge_type = options['type']
        badge_str = ' '.join(options['badge'])
        # Attempt to find the player
        try:
            player = Player.objects.get(pk=player_id)
        except Player.DoesNotExist:
            raise CommandError(f"Player with ID {player_id} does not exist.")
        # Attempt to find the badge
        if not badge_str in league_config.initial_badges:
            raise CommandError(f"Badge {badge_str} does not exist.")
        else:
            # Add the badge to the player
            if not player.primary_badges or not player.secondary_badges:
                raise CommandError(f"Player {player.first_name} {player.last_name} does not have any primary or secondary badges.")
            else:
                if badge_type == 'primary':
                    if badge_str in player.primary_badges:
                        raise CommandError(f"Player {player.first_name} {player.last_name} already has the {badge_str} badge.")
                    else:
                        # Remove the badge from the secondary badges if it exists
                        if badge_str in player.secondary_badges:
                            player.secondary_badges.remove(badge_str)
                        player.primary_badges.append(badge_str)
                elif badge_type == 'secondary':
                    if badge_str in player.secondary_badges or badge_str in player.primary_badges:
                        raise CommandError(f"Player {player.first_name} {player.last_name} already has the {badge_str} badge.")
                    else:
                        player.secondary_badges.append(badge_str)
        # Save the player
        player.upgrades_pending = True
        # Update the player's physical attributes
        updated_player = player_physicals.setStartingPhysicals(player)
        # Save the player
        updated_player.save()
        self.stdout.write(self.style.SUCCESS(f"{player.first_name} {player.last_name} has been updated successfully (added {badge_str})."))
