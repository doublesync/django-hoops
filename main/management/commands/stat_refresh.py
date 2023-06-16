from main.discord import webhooks as hoops_webhooks
from stats.models import SeasonAverage
from stats.models import SeasonTotal
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Refreshes the stats for all players; updates averages and totals."
    def handle(self, *args, **options):
        # Refresh the stats for all players
        season_averages = SeasonAverage.objects.all()
        season_totals = SeasonTotal.objects.all()
        # Iterate through each
        for average in season_averages:
            average.save()
        for total in season_totals:
            total.save()
        # Send success message
        hoops_webhooks.send_webhook(
            url="upgrade",
            title="Stats Refreshed",
            message="All player stats have been refreshed.",
        )
        # Send console message
        self.stdout.write(
            self.style.SUCCESS(f"Successfully refreshed all player stats.")
        )