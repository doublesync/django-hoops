from discord_webhook import DiscordWebhook, DiscordEmbed

default_webhook_url = "https://discord.com/api/webhooks/1086530634740158495/OAa8TpMTlBQ93itkGrV3K-qQJCzs8PAjKS6-w0MRhslgmV-Hphbpal6VP_WeHcRYtEoz"
default_webhook_msg = "Webhook test message"


def send_webhook(url=default_webhook_url, title="", message=""):
    # Create the webhook
    webhook = DiscordWebhook(url=url)
    # Create an embed
    webhook_embed = DiscordEmbed(title=title, description=message, color="03b2f8")
    webhook_embed.set_timestamp()
    webhook_embed.set_footer(text="Powered by hoopscord.com")
    # Add embed object to webhook
    webhook.add_embed(webhook_embed)
    # Send webhook
    webhook.execute()
