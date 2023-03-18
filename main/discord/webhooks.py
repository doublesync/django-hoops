from discord_webhook import DiscordWebhook, DiscordEmbed

default_webhook_url = "https://discord.com/api/webhooks/1086530634740158495/OAa8TpMTlBQ93itkGrV3K-qQJCzs8PAjKS6-w0MRhslgmV-Hphbpal6VP_WeHcRYtEoz"
default_webhook_msg = "Webhook test message"


def send_webhook(url=default_webhook_url, title="", message=""):
    webhook = DiscordWebhook(url=url)
    webhook_embed = DiscordEmbed(title=title, description=message, color="03b2f8")
    webhook.add_embed(webhook_embed)
    webhook.execute()
